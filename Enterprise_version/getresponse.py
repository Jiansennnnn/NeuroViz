import requests
import json


url = "http://127.0.0.1:8000/v1/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer token-abc123"
}
prompt = (
    "assistant: You are a helpful assistant"
    "user: 中国的首都是哪里"

)

data = {
    "model": "qwen/Qwen-7B-Chat",
    "prompt": prompt,  # 将对话历史传入prompt
    "max_tokens": 50,  # 增加生成的最大令牌数
    "temperature": 0.01
}

response = requests.post(url, headers=headers, data=json.dumps(data))
response = response.json()

text = response['choices'][0]['text']
match = re.search(r'：([^<]+)', text)

if match:
    result = match.group(1)  # 提取匹配的部分
    print(result)
else:
    print("没有找到匹配的内容")