import os
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI

# 初始化模型
client = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 初始化搜索工具
search = TavilySearch(max_results=2)


def smart_assistant(question):
    """手动实现工具调用逻辑"""
    print(f"用户问题: {question}")

    # 第一步：让模型判断是否需要搜索
    judgment_prompt = f"""
    请分析以下问题是否需要联网搜索最新信息来回答：
    问题：{question}

    如果问题涉及实时信息、最新新闻、当前天气、股票价格等需要最新数据的内容，请回复"SEARCH: 搜索关键词"。
    如果问题基于常识、历史事实、通用知识等不需要最新数据的内容，请直接回答。

    请直接给出回复：
    """

    judgment = client.invoke([HumanMessage(content=judgment_prompt)])
    response = judgment.content

    print(f"模型判断: {response}")

    if response.startswith("SEARCH:"):
        # 需要搜索
        search_query = response.replace("SEARCH:", "").strip()
        print(f"执行搜索: {search_query}")

        try:
            search_result = search.invoke(search_query)
            print(f"搜索结果类型: {type(search_result)}")
            print(f"搜索结果: {search_result}")

            # 处理搜索结果 - 将字典转换为字符串
            if isinstance(search_result, dict):
                # 如果是字典，提取有用的信息
                search_text = ""
                for key, value in search_result.items():
                    search_text += f"{key}: {value}\n"
                search_text = search_text[:500]  # 限制长度
            elif isinstance(search_result, list):
                # 如果是列表，连接所有元素
                search_text = "\n".join(str(item) for item in search_result[:5])  # 只取前5个
                search_text = search_text[:500]
            else:
                # 如果是字符串，直接使用
                search_text = str(search_result)[:500]

            print(f"处理后的搜索结果: {search_text}")

            # 结合搜索结果生成最终回答
            final_prompt = f"""
            用户问题：{question}
            搜索关键词：{search_query}
            搜索结果：{search_text}

            请根据以上信息，用中文给出完整、准确的回答：
            """

            final_response = client.invoke([HumanMessage(content=final_prompt)])
            return final_response.content

        except Exception as e:
            return f"搜索时出现错误: {e}"
    else:
        # 直接回答
        return response


# 测试
result1 = smart_assistant("中国的首都是哪个？")
print("最终回答1:", result1)
print("-" * 50)

result2 = smart_assistant("北京今天的天气怎么样？")
print("最终回答2:", result2)
print("-" * 50)

# 再测试一个需要搜索的问题
result3 = smart_assistant("今天的热门新闻有哪些？")
print("最终回答3:", result3)