import requests
import json
from pathlib import Path


INPUT_DIR = Path(__file__).parent / "llm_inputs"


def analyse_sentiment(article: str, title: str, monitored_stocks: dict) -> str:
    allowed_stocks = json.dumps(monitored_stocks)

    with open(INPUT_DIR / "system_input.txt", "r") as f:
        system_prompt = f.read()

    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
Allowed stocks:
{allowed_stocks}

Title:
{title}

Article:
{article}
"""
                }
            ],
            "temperature": 0
        }
    )

    r = response.json()["choices"][0]["message"]["content"]

    return r