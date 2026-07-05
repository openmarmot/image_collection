#!/usr/bin/env python3
import requests
import base64

IMAGE_URL = "http://10.11.0.58:8008/capture_image"
OPENAI_BASE = "http://10.12.0.51:8085/v1"

resp = requests.get(IMAGE_URL, timeout=15)
resp.raise_for_status()

b64 = base64.b64encode(resp.content).decode()

result = requests.post(
    f"{OPENAI_BASE}/chat/completions",
    json={
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    },
                ],
            }
        ],
    },
    timeout=60,
)
result.raise_for_status()

msg = result.json()["choices"][0]["message"]
print(msg.get("content") or msg.get("reasoning_content", ""))
