# test_import.py
try:
    from langchain_community.document_loaders import WebBaseLoader

    print("✅ 成功导入 WebBaseLoader")

    # 测试创建实例
    loader = WebBaseLoader(["https://httpbin.org/html"])
    print("✅ 成功创建 WebBaseLoader 实例")

    # 测试加载
    docs = loader.load()
    print(f"✅ 成功加载文档，数量: {len(docs)}")

except ImportError as e:
    print(f"❌ 导入失败: {e}")
except Exception as e:
    print(f"❌ 其他错误: {e}")