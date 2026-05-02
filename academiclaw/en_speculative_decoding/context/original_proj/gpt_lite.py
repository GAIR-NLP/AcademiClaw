import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import time

class GPTConfig:
    def __init__(self, vocab_size=1000, n_embd=64, n_head=2, n_layer=4, block_size=128):
        self.vocab_size = vocab_size
        self.n_embd = n_embd
        self.n_head = n_head
        self.n_layer = n_layer
        self.block_size = block_size

class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.head_dim = config.n_embd // config.n_head
        assert self.n_embd % self.n_head == 0
        
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        self.register_buffer("bias", torch.tril(torch.ones(config.block_size, config.block_size))
                                     .view(1, 1, config.block_size, config.block_size))

    def forward(self, x, past_kv=None):
        B, T, C = x.size()
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)
        
        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)

        # KV-Cache 拼接逻辑
        if past_kv is not None:
            past_k, past_v = past_kv
            k = torch.cat([past_k, k], dim=2)
            v = torch.cat([past_v, v], dim=2)
            
        current_kv = (k, v)

        # Attention Calculation
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
        
        # Masking: 确保 T>1 时也能正确 mask
        total_len = k.size(2)
        causal_mask = self.bias[:, :, total_len-T:total_len, :total_len]
        att = att.masked_fill(causal_mask == 0, float('-inf'))
        
        att = F.softmax(att, dim=-1)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.c_proj(y), current_kv

class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln2 = nn.LayerNorm(config.n_embd)
        self.mlp = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.GELU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
        )

    def forward(self, x, past_kv=None):
        attn_out, current_kv = self.attn(self.ln1(x), past_kv)
        x = x + attn_out
        x = x + self.mlp(self.ln2(x))
        return x, current_kv

class GPTLite(nn.Module):
    def __init__(self, config, simulate_latency=False):
        super().__init__()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.n_embd)
        self.position_embedding = nn.Embedding(config.block_size, config.n_embd)
        self.blocks = nn.ModuleList([Block(config) for _ in range(config.n_layer)])
        self.ln_f = nn.LayerNorm(config.n_embd)
        self.head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        
        # [Benchmark 核心] 模拟延迟开关
        self.simulate_latency = simulate_latency
        # 每次 Forward 强制延迟 20ms，模拟大模型 Memory Bound
        self.latency_seconds = 0.02 

    def forward(self, idx, past_key_values=None):
        # idx: [Batch, SeqLen]
        device = idx.device
        b, t = idx.size()
        
        # 处理 Positional Embedding
        if past_key_values is not None:
            # 如果有 Cache，当前位置从 past_len 开始
            past_len = past_key_values[0][0].size(2)
            pos = torch.arange(past_len, past_len + t, dtype=torch.long, device=device)
        else:
            pos = torch.arange(0, t, dtype=torch.long, device=device)

        tok_emb = self.token_embedding(idx)
        pos_emb = self.position_embedding(pos)
        x = tok_emb + pos_emb
        
        new_past_key_values = []
        for i, block in enumerate(self.blocks):
            last_kv = past_key_values[i] if past_key_values is not None else None
            x, current_kv = block(x, past_kv=last_kv)
            new_past_key_values.append(current_kv)
            
        x = self.ln_f(x)
        logits = self.head(x)
        
        # [核心模拟逻辑]
        # 无论是串行生成(T=1) 还是 并行验证(T=5)
        # 我们假设这都是一次 Kernel Launch，耗时基本固定
        if self.simulate_latency:
            time.sleep(self.latency_seconds)

        return logits, new_past_key_values