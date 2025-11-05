# Please install OpenAI SDK first: `pip3 install openai`
# 安装 pip install langchain
# 安装 pip install langchain-openai
import os
# from langchain.chains import LLMChain
from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from langserve import add_routes

client = ChatOpenAI(
    model = "deepseek-chat",
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com")

msg = [
    {"role": "system", "content": "你是个猫娘，请用猫娘语气进行回答"},
    {"role": "user", "content": "介绍一下你自己"},
]
#定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '请将下面的内容翻译成{language}'),
    ('user', '{text}')
])
#创建返回的数据解析器
parser = StrOutputParser()
#得到链
chain = prompt_template | client  | parser
#直接使用chain来调用
result = client.invoke(msg)
print("猫娘的自我介绍：",result.content)
chain_result=chain.invoke({'language': 'en','text':'我今天下午还有一节课，不能出去玩了'})
print("翻译结果为：",chain_result)
#把程序部署成服务
#创建fastApi的应用
app = FastAPI(title='我的langchain服务',version='V1.0',description='使用langchain翻译任何语句')

add_routes(
    app,
    chain,
    path='/chainDemo'
)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)