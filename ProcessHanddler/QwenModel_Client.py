import os
from openai import OpenAI
from constant.model_constant import model_constant


class QwenClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=model_constant.DASHSCOPE_API_KEY,
            base_url=model_constant.BASE_URL
        )
        self.model = model_constant.QWEN_MODEL

    def send_request(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content

    def call_qwen_api(self, prompt):
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ]
        return self.send_request(messages)
