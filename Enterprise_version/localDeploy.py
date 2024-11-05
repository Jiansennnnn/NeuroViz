import subprocess
import os

# 设置环境变量
os.environ["VLLM_USE_MODELSCOPE"] = "True"

# 构造命令
command = [
    "python", "-m", "vllm.entrypoints.openai.api_server",
    "--model", "qwen/Qwen-7B-Chat",
    "--dtype", "auto",
    "--api-key", "token-abc123",
    "--trust-remote-code",
    "--gpu-memory-utilization", "0.9",
    "--chat_template", "{%- if messages[0]['role'] == 'system' -%}    {%- set system_message = messages[0]['content'] -%}    {%- set messages = messages[1:] -%}{%- else -%}    {% set system_message = '' -%}{%- endif -%}{{ bos_token + system_message }}{%- for message in messages -%}    {%- if (message['role'] == 'user') != (loop.index0 % 2 == 0) -%}        {{ raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}    {%- endif -%}    {%- if message['role'] == 'user' -%}        {{ 'USER: ' + message['content'] + '\\n' }}    {%- elif message['role'] == 'assistant' -%}        {{ 'ASSISTANT: ' + message['content'] + eos_token + '\\n' }}    {%- endif -%}{%- endfor -%}{%- if add_generation_prompt -%}    {{ 'ASSISTANT:' }} {% endif %}"
]

# 执行命令
result = subprocess.run(command, capture_output=True, text=True)

# 输出执行结果
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)