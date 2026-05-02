# Query 2

[Task Description]
You are an edge-side AI deployment engineer tasked with completing the full pipeline for mixed-precision quantization deployment of `Qwen2.5-1.5B-Instruct` in a MacBook environment. You need to handle environment setup (create a virtual environment and submit `requirements.txt`), resource preparation (download the original model yourself and manually convert the provided Parquet-format validation set `context/validation-00000-of-00001.parquet` to `validation.jsonl` format), and write a script to generate the mixed-precision `qwen_quantized.pth`.

[Context]
File list:
- `context/validation-00000-of-00001.parquet`: Raw validation data (needs conversion).
- `Qwen2.5-1.5B-Instruct`: Must be downloaded by the user.
