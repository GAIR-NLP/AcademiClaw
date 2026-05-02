## Query

I am trying out a new project, omnilingual-asr, a multilingual speech recognition model open-sourced by Facebook. Project URL: https://github.com/facebookresearch/omnilingual-asr. I need to deploy this model on an Ascend (NPU) server. The lab's Ascend server has domain restrictions and cannot load models via the direct load_model method — it can only load models via checkpoint loading. The checkpoints are omniASR_CTC_300M.pt and omniASR_tokenizer.model, but omnilingual-asr does not provide a checkpoint-based loading method. Furthermore, the project depends on fairseq2, and fairseq2n does not support the Ascend platform (aarch64), nor does it support Windows — no precompiled packages are available for any platform.

Your tasks:
1) Configure omnilingual-asr and solve the fairseq2 installation problem so that `pip install omnilingual-asr` succeeds.
2) Implement checkpoint-based loading of the omniASR_CTC_300M.pt model. (Do this after setting up the environment. You must NOT load the model by downloading it from the network — the checkpoint is already provided in the workspace. The official omnilingual-asr project does not provide a checkpoint loading method; you need to learn how by searching the web, reading the fairseq2 code repository, and reading the original omnilingual-asr paper.) The parameter count must be exactly 325_494_996 (strict), with no missing or unexpected keys.
3) Build a simple speech recognition demo: input an English audio file (provided), output the recognized text (WER will be computed), and decode a text segment with the tokenizer (the result must exactly match the reference output).

## Context

Files:
- context/omniASR-CTC-300M.pt - Model checkpoint file
- context/omniASR_tokenizer.model - Tokenizer model file
- context/common_voice_en_444.wav - Test audio file
- context/context.md - Project URL, network domain whitelist, and other contextual information
