#!/usr/bin/env python3
"""测试 Anthropic API 是否有效"""
import os
import anthropic
from pathlib import Path

# 加载 .env 文件
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

from llm_generator import ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL, TEXT_MODEL

print(f"API Key 前缀: {ANTHROPIC_API_KEY[:20] if ANTHROPIC_API_KEY else 'None'}...")
print(f"API Key 长度: {len(ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else 0}")
print(f"Base URL: {ANTHROPIC_BASE_URL}")

if not ANTHROPIC_API_KEY:
    print("\n❌ 错误: 未找到 API Key!")
    print("请复制 .env.example 为 .env 并填写 ANTHROPIC_API_KEY")
    exit(1)

try:
    print("\n正在测试 API 连接...")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, base_url=ANTHROPIC_BASE_URL)

    message = client.messages.create(
        model=TEXT_MODEL,
        max_tokens=100,
        messages=[{"role": "user", "content": "回复'API 测试成功'"}]
    )

    print(f"\n✅ API 测试成功!")
    print(f"模型响应: {message.content[0].text}")

except anthropic.AuthenticationError as e:
    print(f"\n❌ 认证失败: API Key 无效")
    print(f"错误详情: {e}")

except anthropic.RateLimitError as e:
    print(f"\n❌ 速率限制: 请求过多或额度不足")
    print(f"错误详情: {e}")

except Exception as e:
    print(f"\n❌ 其他错误: {type(e).__name__}")
    print(f"错误详情: {e}")