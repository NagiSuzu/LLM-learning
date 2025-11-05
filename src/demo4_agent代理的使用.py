import os

from langchain_core.messages import HumanMessage
# from langchain.chains import LLMChain
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import chat_agent_executor, create_react_agent

from langserve import add_routes



client = ChatOpenAI(
    model = "deepseek-chat",
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com")

# result = client.invoke([HumanMessage(content='北京的天气怎么样')])
# print(result.content)

# LangChain内置了一个工具，可以轻松使用Tavily搜索引擎作为工具
search = TavilySearch(max_results=2) #max_results=2:只返回两个值
# print(search.invoke('北京的天气怎么样'))

# 让模型绑定工具
tools = [search]
# model_with_tools =client.bind_tools(tools)

#模型可以自动推理：是否需要调用工具去完成用户的答案
# resp = model_with_tools.invoke([HumanMessage(content='中国的首都是哪个城市')])
#
# print(f'Model_Result_Content:{resp.content}')
# print(f'Tools_Result_Content:{resp.tool_calls}')
#
# resp2 = model_with_tools.invoke([HumanMessage(content='北京的天气怎么样')])
#
# print(f'Model_Result_Content:{resp2.content}')
# print(f'Tools_Result_Content:{resp2.tool_calls}')

#  创建代理

# agent = create_react_agent(client, tools)

resp = client.invoke([HumanMessage(content='中国的首都是哪个城市')])
print(resp.content)

resp2 = client.invoke([HumanMessage(content='北京的天气怎么样')])
print(resp2.content)