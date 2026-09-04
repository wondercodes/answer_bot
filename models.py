import base64
from io import BytesIO
from openai import OpenAI

from config import (
    MODEL_PROVIDER,
    MODEL_CONFIG,
    SYSTEM_PROMPT,
)


class LLMError(Exception):
    pass


class LLMModel:

    def __init__(self):

        if MODEL_PROVIDER not in MODEL_CONFIG:
            raise ValueError(
                f"Unknown model provider: {MODEL_PROVIDER}"
            )

        config = MODEL_CONFIG[MODEL_PROVIDER]

        api_key = config["api_key"]

        if not api_key:
            raise ValueError(
                f"API key for {MODEL_PROVIDER} is not configured"
            )

        self.provider = MODEL_PROVIDER

        self.model = config["model"]

        self.client = OpenAI(
            api_key=api_key,
            base_url=config["base_url"]
        )

    def answer(self, question):

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],

                # 答题通常不需要太大的输出
                max_tokens=1500,

                # 降低随机性，提高答案稳定性
                temperature=0.2,
            )

            answer = response.choices[0].message.content

            if not answer:
                raise LLMError(
                    "Model returned empty answer"
                )

            return answer.strip()

        except Exception as e:

            raise LLMError(
                f"{self.provider} request failed: {e}"
            )

    @staticmethod
    def image_to_base64(image):
        """
        PIL.Image -> Base64 PNG
        """
        buffer = BytesIO()
        image.save(buffer, format="PNG")

        return base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

    def image_to_answer(self, image_path):

        try:

            image_data = self.image_to_base64(image_path)

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "请根据图片中的题目内容直接回答问题。"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}",
                                    "detail": "original"
                                }
                            }
                        ]
                    }
                ]
            )

            answer = response.choices[0].message.content

            if not answer:
                raise LLMError(
                    "Model returned empty answer"
                )

            return answer.strip()

        except Exception as e:

            raise LLMError(
                f"{self.provider} image request failed: {e}"
            )