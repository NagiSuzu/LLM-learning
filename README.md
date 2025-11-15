# LLM-learning
AI框架学习记录

25-11-15
demo5_构建rag
生产级对话 RAG 应用的标准方式，可以用于辅助阅读文献。检索器retriever也包含上下文的理解
是 LangChain 推荐的、用于构建真正有记忆的对话式 RAG 的模式。

##工作流程：
它引入了一个关键的中间步骤：问题重述。

###问题重述（核心步骤）：
当用户问 "到时去哪？" 时，这个问题不会直接送给 retriever。
它首先被送入一个特殊的子链 history_chain（由 create_history_aware_retriever 创建）。
这个子链使用 contextualize_q_system_prompt，结合 chat_history（例如：[("human", "什么时候报道"), ("ai", "...")]）和当前问题 "到时去哪？"。
LLM 的任务不是回答问题，而是生成一个独立的、包含上下文的新问题。例如，它可能会生成："那篇报道中提到的活动将在哪里举行？"。
###智能检索：
这个重述后的问题 "那篇报道中提到的活动将在哪里举行？" 被发送给 retriever。
现在检索器能轻松找到包含“地点”、“举办地”等信息的文档片段了，因为重述后的问题包含了所有必要的上下文。
###生成答案：
检索到的 context 和原始用户问题 "到时去哪？"（注意，这里用的是原始问题，让回答更自然）以及 chat_history 一起被送入最终的问答 chain1。
LLM 生成最终答案。
###RunnableWithMessageHistory 的作用：
这是一个“包装器”（Wrapper），它自动化了 chat_history 的管理。

不需要手动创建和传递 history 列表。
只需要提供一个 get_session_history 函数和一个 session_id。
RunnableWithMessageHistory 会在每次调用前后，自动从 store 中加载历史记录，并将新的对话对存入 store。这极大地简化了代码，使其更具可扩展性。
