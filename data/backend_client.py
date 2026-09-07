import os
import requests
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://angush579.pythonanywhere.com/api"
API_KEY = os.getenv("ENERGY_API_KEY")


def check_article(url: str) -> dict:

    response = requests.get(
        f"{BASE_URL}/articles/check",
        params={"url": url}
    )

    return response.json()


def add_article(
    url: str,
    title: str,
    publisher: str,
    source_api: str,
    published_at=None
) -> dict:

    response = requests.post(
        f"{BASE_URL}/articles",
        headers={
            "X-API-Key": API_KEY
        },
        json={
            "url": url,
            "title": title,
            "publisher": publisher,
            "source_api": source_api,
            "published_at": published_at
        }
    )

    return response.json()


def add_analysis(
    article_id: int,
    analysis: dict,
    model: str,
    prompt_version: str
) -> dict:

    response = requests.post(
        f"{BASE_URL}/analyses",
        headers={
            "X-API-Key": API_KEY
        },
        json={
            "article_id": article_id,
            "model": model,
            "prompt_version": prompt_version,
            "title_match": analysis["title_match"],
            "stocks": analysis["stocks"]
        }
    )

    return response.json()