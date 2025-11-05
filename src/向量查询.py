# F:\myproject\LangchainDemo\src\构建向量数据库.py

import os
from langchain_chroma import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_core.documents import Document

# --- 1. 准备文档数据 ---
documents = [
    Document(
        page_content="狗是伟大的伴侣，以其忠诚和友好而闻名。",
        metadata={"source": "哺乳动物宠物文档"},
    ),
    Document(
        page_content="猫是独立的动物，通常喜欢自己的空间",
        metadata={"source": "哺乳动物宠物文档"},
    ),
    Document(
        page_content="金鱼是初学者的流行宠物，需要相对简单的护理",
        metadata={"source": "鱼类宠物文档"},
    ),
    Document(
        page_content="鹦鹉是聪明的鸟类，能够模仿人类的语言",
        metadata={"source": "鸟类宠物文档"},
    ),
    Document(
        page_content="兔子是社交动物，需要足够的空间跳跃",
        metadata={"source": "哺乳动物宠物文档"},
    ),
]

# --- 2. 设置嵌入模型 ---
# 强烈建议从环境变量中读取 API Key，而不是硬编码
# 在运行前，请在命令行设置: set ZHIPUAI_API_KEY="你的真实密钥"
zhipuai_api_key = os.environ.get("ZHIPUAI_API_KEY")
if not zhipuai_api_key:
    raise ValueError("请设置环境变量 ZHIPUAI_API_KEY")

embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    zhipuai_api_key=zhipuai_api_key
)

# --- 3. 创建并填充向量数据库 ---
# 注意：如果本地已存在名为 "langchain_store" 的数据库，Chroma会直接加载它
# 如果你想强制重建，可以删除该文件夹或指定一个不同的名称
vector_store = Chroma.from_documents(documents, embedding=embeddings, persist_directory="./langchain_store")

# --- 4. 执行相似度查询 ---
query = "咖啡猫"
results = vector_store.similarity_search_with_score(query)

print(f"查询 '{query}' 的相似度结果：")
for doc, score in results:
    print(f"内容: {doc.page_content}")
    print(f"来源: {doc.metadata}")
    print(f"相似度分数: {score:.4f}\n")

