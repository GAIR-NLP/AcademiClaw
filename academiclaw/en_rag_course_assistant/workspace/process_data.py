import os
import time
from document_loader import DocumentLoader
from text_splitter import TextSplitter
from vector_store import VectorStore

from config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_DB_PATH


def main():
    if not os.path.exists(DATA_DIR):
        print(f"数据目录不存在: {DATA_DIR}")
        print("请创建数据目录并放入PDF、PPTX、DOCX或TXT文件")
        return

    # 运行控制参数（用于避免超时）
    max_docs = int(os.getenv("MAX_DOCS", "300"))
    max_chunks = int(os.getenv("MAX_CHUNKS", "2000"))
    time_budget = int(os.getenv("TIME_BUDGET_SEC", "900"))

    start_time = time.time()

    # 初始化组件
    loader = DocumentLoader(
        data_dir=DATA_DIR,
    )
    splitter = TextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    vector_store = VectorStore(db_path=VECTOR_DB_PATH)
    vector_store.clear_collection()

    # 加载文档
    documents = loader.load_all_documents()
    if not documents:
        print("未找到任何文档")
        return

    if max_docs > 0 and len(documents) > max_docs:
        documents = documents[:max_docs]
        print(f"已限制文档数: {len(documents)}")

    # 切分文档
    chunks = splitter.split_documents(documents)

    if max_chunks > 0 and len(chunks) > max_chunks:
        chunks = chunks[:max_chunks]
        print(f"已限制切分块数: {len(chunks)}")

    if time.time() - start_time > time_budget:
        print("达到时间预算上限，提前写入当前已生成的向量")

    # 存储到向量数据库
    vector_store.add_documents(chunks)
    
    print("\n数据处理完成！可以运行main.py开始对话")


if __name__ == "__main__":
    main()
