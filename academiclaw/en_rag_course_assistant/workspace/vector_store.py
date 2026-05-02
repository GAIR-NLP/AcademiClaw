import os
import hashlib
import math
from typing import List, Dict, Any

import chromadb
from chromadb.config import Settings
from openai import OpenAI
from tqdm import tqdm

from config import (
    VECTOR_DB_PATH,
    COLLECTION_NAME,
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OPENAI_EMBEDDING_MODEL,
    TOP_K,
)


class VectorStore:

    def __init__(
        self,
        db_path: str = VECTOR_DB_PATH,
        collection_name: str = COLLECTION_NAME,
        api_key: str = OPENAI_API_KEY,
        api_base: str = OPENAI_API_BASE,
    ):
        self.db_path = db_path
        self.collection_name = collection_name

        # 初始化OpenAI客户端（允许无 key）
        self.client = OpenAI(api_key=api_key or None, base_url=api_base or None)
        disable_emb = os.getenv("DISABLE_OPENAI_EMBEDDINGS", "0") == "1"
        # SII 接口通常不提供 embedding，检测到 SII base 时默认禁用
        if (api_base or "").find("opensii") >= 0:
            disable_emb = True
        self.use_openai = bool(api_key) and (not disable_emb)
        self._openai_disabled = False
        self.use_local_embedding = os.getenv("USE_LOCAL_EMBEDDING", "0") == "1"

        # 初始化ChromaDB
        os.makedirs(db_path, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(
            path=db_path, settings=Settings(anonymized_telemetry=False)
        )

        # 获取或创建collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name, metadata={"description": "课程材料向量数据库"}
        )

    def get_embedding(self, text: str) -> List[float]:
        """获取文本的向量表示

        TODO: 使用OpenAI API获取文本的embedding向量

        """
        text = (text or "").strip()
        if not text:
            return []
        # 1) OpenAI 优先（如有 key）
        if self.use_openai and (not self._openai_disabled):
            try:
                resp = self.client.with_options(timeout=5.0).embeddings.create(
                    model=OPENAI_EMBEDDING_MODEL, input=text
                )
                vec = resp.data[0].embedding
                if vec:
                    return list(vec)
            except Exception as e:
                self._openai_disabled = True
                print(f"OpenAI 嵌入失败，已禁用后续 OpenAI 嵌入: {e}")
        # 2) 可选本地模型（默认关闭，避免下载耗时）
        if self.use_local_embedding:
            try:
                from sentence_transformers import SentenceTransformer
                model_name = os.getenv(
                    "LOCAL_EMBEDDING_MODEL",
                    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                )
                embedder = SentenceTransformer(model_name)
                vec = embedder.encode([text])[0]
                return [float(x) for x in vec]
            except Exception as e:
                print(f"本地嵌入失败，回退哈希: {e}")
        # 3) 快速哈希向量（保证流程不阻塞）
        h = hashlib.sha256(text.encode("utf-8")).digest()
        arr = [(h[i % len(h)] / 255.0 - 0.5) for i in range(256)]
        norm = math.sqrt(sum(x * x for x in arr)) or 1.0
        return [float(x / norm) for x in arr]

    def add_documents(self, chunks: List[Dict[str, str]]) -> None:
        """添加文档块到向量数据库
        TODO: 实现文档块添加到向量数据库
        要求：
        1. 遍历文档块
        2. 获取文档块内容
        3. 获取文档块元数据
        5. 打印添加进度
        """
        if not chunks:
            print("无文档块可添加")
            return

        ids: List[str] = []
        documents: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        embeddings: List[List[float]] = []

        for idx, ch in enumerate(tqdm(chunks, desc="写入向量库", unit="块")):
            content = (ch.get("content") or "").strip()
            if not content:
                continue
            meta = {
                "filename": ch.get("filename", "unknown"),
                "filepath": ch.get("filepath", ""),
                "filetype": ch.get("filetype", ""),
                "page_number": int(ch.get("page_number", 0) or 0),
                "chunk_id": int(ch.get("chunk_id", idx) or idx),
                "images": ch.get("images", []),
            }
            emb = self.get_embedding(content)
            if not emb:
                continue
            fid = f"{meta.get('filepath','')}-{meta.get('page_number',0)}-{meta.get('chunk_id',0)}-{idx}"
            ids.append(fid)
            documents.append(content)
            metadatas.append(meta)
            embeddings.append(emb)

            if len(ids) >= 256:
                self.collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
                ids, documents, metadatas, embeddings = [], [], [], []

        if ids:
            self.collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

        print(f"已添加向量：{self.collection.count()} 条")

    def search(self, query: str, top_k: int = TOP_K) -> List[Dict]:
        """搜索相关文档

        TODO: 实现向量相似度搜索
        要求：
        1. 首先获取查询文本的embedding向量（调用self.get_embedding）
        2. 使用self.collection进行向量搜索, 得到top_k个结果
        3. 格式化返回结果，每个结果包含：
           - content: 文档内容
           - metadata: 元数据（文件名、页码等）
        4. 返回格式化的结果列表
        """
        emb = self.get_embedding(query)
        if not emb:
            return []
        try:
            res = self.collection.query(
                query_embeddings=[emb],
                n_results=top_k,
                include=["documents", "metadatas", "distances", "embeddings"],
            )
        except Exception as e:
            print(f"搜索失败: {e}")
            return []

        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        embs = (res.get("embeddings") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]

        out: List[Dict] = []
        for i in range(min(len(docs), top_k)):
            out.append(
                {
                    "content": docs[i],
                    "metadata": metas[i] if i < len(metas) else {},
                    "distance": dists[i] if i < len(dists) else None,
                    "embedding": embs[i] if i < len(embs) else None,
                }
            )
        return out

    def clear_collection(self) -> None:
        """清空collection"""
        self.chroma_client.delete_collection(name=self.collection_name)
        self.collection = self.chroma_client.create_collection(
            name=self.collection_name, metadata={"description": "课程向量数据库"}
        )
        print("向量数据库已清空")

    def get_collection_count(self) -> int:
        """获取collection中的文档数量"""
        return self.collection.count()
