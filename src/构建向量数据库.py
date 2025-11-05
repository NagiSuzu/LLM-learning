#安装:pip install langchain-chroma
#因为deepseek 不支持嵌入模型（OpenAI应该可以，但我没买），所以用本地嵌入模型将文本向量化
#安装：pip install sentence-transformers
# Please install OpenAI SDK first: `pip3 install openai`
import os
from importlib.resources import contents

from langchain_chroma import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from langchain.chains import LLMChain
# from langchain_community.chains import LLMChain
from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langserve import add_routes
from sqlalchemy.testing.suite.test_reflection import metadata
from zai import ZhipuAiClient

#聊天机器人案例
# client = ChatOpenAI(
#     model = "deepseek-chat",
#     api_key=os.environ.get('sk-xxxxx'),
#     base_url="https://api.deepseek.com")
#设置代理和deepseek API
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# os.environ["OPENAI_API_KEY"] = "sk-xxxxx"

documents = [
    Document(
        page_content="狗是伟大的伴侣，以其忠诚和友好而闻名。",
        metadata={"source":"哺乳动物宠物文档"},
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
# 使用 智谱 的嵌入模型
embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    zhipuai_api_key="ZHIPUAI_API_KEY"
)

# 实例化一个向量空间
vector_store = Chroma.from_documents(documents,embedding=embeddings)

#相似度的查询:返回相似的分数，分数越低相似度越高
print(vector_store.similarity_search_with_score('咖啡猫'))