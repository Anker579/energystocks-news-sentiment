import requests

response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "model": "local-model",
        "messages": [
            {
                "role": "user",
                "content": "Classify this article as bullish, bearish or neutral."
            }
        ],
        "temperature": 0
    }
)

print(response.json()["choices"][0]["message"]["content"])