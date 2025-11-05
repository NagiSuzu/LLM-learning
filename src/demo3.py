import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.prompts import ChatPromptTemplate, format_document
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

#from src.demo1 import prompt_template
#deepseek的模型
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
 raise RuntimeError("未检测到 API Key。请先在当前窗口执行: set DEEPSEEK_API_KEY=你的密钥 或 set OPENAI_API_KEY=你的密钥")
client = ChatOpenAI(
    model = "deepseek-chat",
    api_key=os.environ.get('sk-e9db8e390cbf4a2bbe48ed154479a427'),
    base_url="https://api.deepseek.com")

# 可选：如果你仍然需要代理用于其他网络请求，可以保留；与 FastEmbed 无关
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# ---------------------- 1. 准备示例文档 ----------------------
documents = [
    Document(page_content="狗是伟大的伴侣，以其忠诚和友好而闻名。", metadata={"source": "哺乳动物宠物文档"}),
    Document(page_content="猫是独立的动物，通常喜欢自己的空间。", metadata={"source": "哺乳动物宠物文档"}),
    Document(page_content="金鱼是初学者的流行宠物，需要相对简单的护理。", metadata={"source": "鱼类宠物文档"}),
    Document(page_content="鹦鹉是聪明的鸟类，能够模仿人类的语言。", metadata={"source": "鸟类宠物文档"}),
    Document(page_content="兔子是社交动物，需要足够的空间跳跃。", metadata={"source": "哺乳动物宠物文档"}),
]

# ---------------------- 2. 使用 FastEmbed 向量模型 ----------------------
# 注：FastEmbedEmbeddings 默认模型为 BAAI/bge-small-zh-v1.5（中文表现良好）
# 也可自定义：FastEmbedEmbeddings(model_name="BAAI/bge-base-zh-v1.5")
# embedding_model = FastEmbedEmbeddings()  # 中文推荐，免下载/免代理，CPU 快
print("初始化 FastEmbedEmbeddings（如首次运行，可能需要下载模型）...")
embedding_model = FastEmbedEmbeddings(model_name="qdrant/bge-small-zh-v1.5-onnx-q")
print("FastEmbed 初始化完成。")
# ---------------------- 3. 创建 Chroma 向量数据库 ----------------------
# 提示：首次运行会在本地内存中构建；若需持久化，可加 persist_directory="./chroma_db"
vector_store = Chroma.from_documents(documents, embedding=embedding_model)

# ---------------------- 4. 执行相似度检索 ----------------------
query = "咖啡猫"
results = vector_store.similarity_search_with_score(query, k=3)

# ---------------------- 5. 输出结果 ----------------------
print("🔎 查询问题：", query)
print("\n📚 相似内容匹配结果：\n")
for doc, score in results:
    print(f"内容：{doc.page_content}")
    print(f"来源：{doc.metadata.get('source', '未知')}")
    print(f"相似度分数：{score}")
    print("-" * 50)

#检索器 bind(k=1) 返回相似度最高的第一个
retriever = RunnableLambda(vector_store.similarity_search).bind(k=1)

# print(retriever.batch(['咖啡猫', '鲨鱼']))

#提示模板
message = """
使用提供的上下文仅回答这个问题
{question}
上下文：
{context}
"""

prompt_temp = ChatPromptTemplate.from_messages([('human',message)])

#RunnablePassthrough
chain = {'question': RunnablePassthrough(), 'context': retriever | RunnableLambda(format_docs),} | prompt_temp | client

resp = chain.invoke('请介绍一下猫？')

print(resp.content)