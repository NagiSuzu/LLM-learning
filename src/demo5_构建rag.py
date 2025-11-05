import os
#user agent
os.environ['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

from langchain_community.document_loaders import WebBaseLoader

# 简化版本，先确保基础功能可用
loader = WebBaseLoader(
    web_paths=['https://mp.weixin.qq.com/s?__biz=MzA4MTUyOTE1MQ==&mid=2653902724&idx=1&sn=08983ea1ff049e21230be240221ee9ff&chksm=858166432f68482a8591c8abc2e497bbe30e741e4f3a6b4cab9a2031353775325a71b8958b2e&scene=27']
)

docs = loader.load()

print(f"加载了 {len(docs)} 个文档")
for i, doc in enumerate(docs):
    print(f"文档 {i+1}:")
    print(f"内容长度: {len(doc.page_content)} 字符")
    print(f"元数据: {doc.metadata}")
    print("-" * 50)