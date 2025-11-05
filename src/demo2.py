# Please install OpenAI SDK first: `pip3 install openai`
import os
from importlib.resources import contents
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.chains import LLMChain
from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langserve import add_routes
#聊天机器人案例
client = ChatOpenAI(
    model = "deepseek-chat",
    api_key=os.environ.get('sk-e9db8e390cbf4a2bbe48ed154479a427'),
    base_url="https://api.deepseek.com")

#定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个猫娘，请用{language}尽你所能回答全部问题'),
    MessagesPlaceholder(variable_name='my_msg')
])
#创建返回的数据解析器
# parser = StrOutputParser()
#得到链
chain = prompt_template | client

#保存历史聊天记录
store = {} #所有你用户的聊天记录都保存到store.key: sessionId,value:历史聊天记录对象

#此函数预期接收一个session_id并返回一个消息历史记录对象
def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


do_message = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key ='my_msg'#每次聊天时候发送msg的key
)

config = {'configurable':{'session_id':'zs123'} }#给当前会话定义一个sessionId

#第一轮
resp = do_message.invoke(
    {
        'my_msg': [HumanMessage(content='你好啊,我叫Nagi')],
        'language': '中文'
    },
    config = config
)

print(resp.content)

#第二轮
resp2 = do_message.invoke(
    {
        'my_msg': [HumanMessage(content='请问我的名字是什么')],
        'language': '中文'
    },
    config = config
)

print(resp2.content)

#第三轮: 返回的数据是流式的
for resp in do_message.stream(
    {
        'my_msg': [HumanMessage(content='请对我讲一个笑话')],
        'language': '中文'
    },
    config = config
):
#每次resp都是一个token
   print(resp.content,end='-')

print(store)
print(get_session_history('zs123'))
