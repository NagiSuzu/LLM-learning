import gradio as gr
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# ==============================
# 初始化 LLM - 使用 DeepSeek
# ==============================
client = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.environ.get("OPENAI_API_KEY"),  # 请确保环境变量已设置
    base_url="https://api.deepseek.com"
)


# ==============================
# 猫娘角色扮演函数
# ==============================
def cat_girl_chat(message, history):
    """根据历史上下文生成猫娘对话"""
    messages = [{"role": "system", "content": "你是一个可爱的猫娘，请用可爱的语气回答。"}]

    # 将历史记录加入上下文
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    try:
        response = client.invoke(messages)
        return response.content
    except Exception as e:
        return f"出错啦：{str(e)}"


# ==============================
# 翻译函数
# ==============================
def text_translator(text, target_language):
    """文本翻译函数"""
    prompt_template = ChatPromptTemplate.from_messages([
        ('system', f'请将下面的内容翻译成{target_language}'),
        ('user', '{text}')
    ])
    chain = prompt_template | client | StrOutputParser()

    try:
        result = chain.invoke({'text': text, 'language': target_language})
        return result
    except Exception as e:
        return f"翻译出错：{str(e)}"


# ==============================
# 创建 Gradio 界面
# ==============================
with gr.Blocks(title="我的AI助手集合", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 我的AI助手 Demo")
    gr.Markdown("基于 LangChain + DeepSeek + Gradio 构建")

    # ---------------------------
    # 🐱 猫娘聊天模块
    # ---------------------------
    with gr.Tab("🐱 猫娘聊天"):
        gr.Markdown("## 和猫娘聊天吧！")

        chatbot = gr.Chatbot(
            label="猫娘",
            bubble_full_width=False,
            height=400
        )

        with gr.Row():
            msg = gr.Textbox(
                label="输入你的消息",
                placeholder="和猫娘说点什么吧...",
                lines=2,
                scale=4
            )
            send = gr.Button("✉️ 发送", variant="primary", scale=1)

        clear = gr.Button("🧹 清空对话")

        # ✅ 定义状态，保存历史
        state = gr.State([])

        # ---------------------------
        # 响应函数
        # ---------------------------
        def respond(message, chat_history):
            """生成回复并更新历史"""
            if not message.strip():
                return gr.update(value=""), chat_history, chat_history

            bot_message = cat_girl_chat(message, chat_history)
            chat_history.append((message, bot_message))
            return gr.update(value=""), chat_history, chat_history

        # ✅ 绑定事件（按回车 && 点击按钮 都可以触发）
        msg.submit(
            respond,
            inputs=[msg, state],
            outputs=[msg, chatbot, state]
        )

        send.click(
            respond,
            inputs=[msg, state],
            outputs=[msg, chatbot, state]
        )

        # ✅ 清空功能
        def clear_chat():
            return [], []

        clear.click(
            clear_chat,
            outputs=[chatbot, state],
            queue=False
        )

    # ---------------------------
    # 🌍 翻译模块
    # ---------------------------
    with gr.Tab("🌍 文本翻译"):
        gr.Markdown("## 多语言文本翻译")

        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="输入要翻译的文本",
                    placeholder="请输入要翻译的内容...",
                    lines=3
                )
                target_lang = gr.Dropdown(
                    choices=["英语", "日语", "韩语", "法语", "德语", "西班牙语"],
                    label="目标语言",
                    value="英语"
                )
                translate_btn = gr.Button("开始翻译", variant="primary")

            with gr.Column():
                output_text = gr.Textbox(
                    label="翻译结果",
                    lines=3,
                    interactive=False
                )

        translate_btn.click(
            text_translator,
            inputs=[input_text, target_lang],
            outputs=output_text
        )

    # ---------------------------
    # 📖 项目介绍
    # ---------------------------
    with gr.Tab("📖 项目介绍"):
        gr.Markdown("""
        ## 项目技术栈
        - **框架**: LangChain, Gradio  
        - **模型**: DeepSeek  
        - **功能**:  
            - 角色扮演聊天  
            - 多语言翻译  
            - Web界面交互  

        ## 我的收获
        - 熟悉 LangChain 链式调用  
        - 学会 Gradio 界面开发  
        - 掌握 API 集成和状态管理  
        """)

# ==============================
# 启动应用
# ==============================
if __name__ == "__main__":
    demo.launch(share=True)