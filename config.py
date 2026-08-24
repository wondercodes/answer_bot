import os


# ============================================================
# 当前使用的模型
#
# 可选：
#   deepseek
#   openai
#   kimi
#
# ============================================================

MODEL_PROVIDER = os.getenv(
    "ANSWER_MODEL",
    "deepseek"
)


# ============================================================
# API Keys
# ============================================================

DEEPSEEK_API_KEY = os.getenv(
    "DEEPSEEK_API_KEY"
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

KIMI_API_KEY = os.getenv(
    "KIMI_API_KEY"
)


# ============================================================
# 模型配置
# ============================================================

MODEL_CONFIG = {

    "deepseek": {
        "api_key": DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },

    "openai": {
        "api_key": OPENAI_API_KEY,
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4.1-mini",
    },

    "kimi": {
        "api_key": KIMI_API_KEY,
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
    },
}


# ============================================================
# 答题 Prompt
# ============================================================

SYSTEM_PROMPT = """
你是一个专业的技术面试和考试答题助手。

用户会提供一道或者多道题目。

你的任务是：

1. 准确理解题目。
2. 直接给出答案。
3. 如果是选择题，明确给出正确选项。
4. 如果是简答题，给出适合直接作答的答案。
5. 如果是 Linux、C、C++、嵌入式 Linux、
   Linux Driver、Kernel、网络、数据结构等问题，
   使用工程实践角度回答。
6. 如果需要代码，给出可以工作的代码。
7. 如果题目有多个小问，按照题号分别回答。
8. 不要重复题目。
9. 不要说“根据图片可以看到”。
10. 不要输出与答案无关的内容。

答案应该简洁、准确、适合直接复制。
"""