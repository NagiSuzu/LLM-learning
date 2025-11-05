# F:\myproject\LangchainDemo\src\demo_fastembed_schemeA.py
import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import FastEmbedEmbeddings



PROJECT_ROOT = r"F:\myproject"
HF_CACHE_DIR = os.path.join(PROJECT_ROOT, "hf_cache")
FASTEMBED_CACHE = os.path.join(HF_CACHE_DIR, "fastembed")
CHROMA_DB_DIR = os.path.join(PROJECT_ROOT, "chroma_db")

os.makedirs(FASTEMBED_CACHE, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

os.environ["HF_HOME"] = HF_CACHE_DIR
os.environ["HF_HUB_CACHE"] = os.path.join(HF_CACHE_DIR, "hub")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# 如需网络代理再打开
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

MODEL_NAME = "BAAI/bge-small-zh-v1.5"  # 来自你的支持列表

embedding = FastEmbedEmbeddings(
    model_name=MODEL_NAME,
    cache_dir=FASTEMBED_CACHE
)

vector_store = Chroma(
    collection_name="pets",
    embedding_function=embedding,
    persist_directory=CHROMA_DB_DIR
)

# 初次写入，避免空库
if vector_store._collection.count() == 0:
   documents = [
      Document(page_content="猫咖是一种提供咖啡并与猫互动的场所。", metadata={"source": "生活方式文档"}),
      Document(page_content="加菲猫是一只虚构的卡通猫，以贪吃、爱睡、讨厌星期一著称。", metadata={"source": "卡通猫文档"}),
      Document(page_content="猫是独立的动物，通常喜欢自己的空间。", metadata={"source": "哺乳动物宠物文档"}),
      Document(page_content="鹦鹉是聪明的鸟类，能够模仿人类的语言。", metadata={"source": "鸟类宠物文档"}),
]
   vector_store.add_documents(documents)
   vector_store.persist()

query = "咖啡猫"
results = vector_store.similarity_search_with_score(query, k=3)
print("🔎 查询问题：", query)
print("\n📚 相似内容匹配结果：\n")
for doc, score in results:
    print(f"内容：{doc.page_content}")
    print(f"来源：{doc.metadata.get('source', '未知')}")
    print(f"分数：{score}")
    print("-" * 50)
