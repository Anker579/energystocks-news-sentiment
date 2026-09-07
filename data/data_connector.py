from __future__ import annotations
import time
import os
import pandas as pd
import requests
from dotenv import load_dotenv


class NewsAPIConnector:

    #load env variables
    def __init__(self):

        load_dotenv()

        self.marketaux_api_key = os.getenv("MARKETAUX_API_TOKEN")
        self.newsdata_api_key = os.getenv("NEWSDATAIO_API_TOKEN")

        self.session = requests.Session()

        self.timeout = 15

    #generic request function to be used for API's
    def _request(self, url, params, max_retries=3):

        for attempt in range(max_retries):
            
            try:

                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )

            except requests.RequestException as error:

                if attempt == max_retries - 1:
                    raise RuntimeError(
                        f"Request failed: {error}"
                    ) from error

                time.sleep(2 ** attempt)
                continue

            # Retry server errors
            if response.status_code >= 500:

                if attempt < max_retries - 1:

                    print(
                        f"Server returned "
                        f"{response.status_code}. "
                        f"Retrying..."
                    )

                    time.sleep(2 ** attempt)
                    continue

            # Give us much better information than
            # response.raise_for_status()
            if not response.ok:

                raise RuntimeError(
                    f"API request failed\n"
                    f"Status: {response.status_code}\n"
                    f"Endpoint: {url}\n"
                    f"Response: {response.text[:1000]}"
                )

            try:

                return response.json()

            except ValueError as error:

                raise RuntimeError(
                    f"API returned invalid JSON.\n"
                    f"Endpoint: {url}\n"
                    f"Response: {response.text[:1000]}"
                ) from error

        raise RuntimeError(
            "API request failed after retries."
        )

    #loads specified parameters into the correct format for newsdataio
    def get_newsdataio(
        self,
        query=None,
        symbol=None,
        language="en",
        size=10
    ):

        if self.newsdata_api_key is None:
            raise ValueError(
                "NEWSDATA_API_KEY is missing from .env"
            )

        params = {
            "apikey": self.newsdata_api_key,
            "language": language,
            "size": size,
        }

        if query is not None:
            params["q"] = query

        if symbol is not None:
            params["symbol"] = symbol

        data = self._request(
            "https://newsdata.io/api/1/market",
            params
        )

        articles = []

        for article in data.get("results", []):

            articles.append({
                "source_api": "newsdataio",

                "article_id": article.get("article_id"),

                "title": article.get("title"),

                "description": article.get("description"),

                "content": article.get("content"),

                "url": article.get("link"),

                "published_at": article.get("pubDate"),

                "publisher": (
                    article.get("source_name")
                    or article.get("source_id")
                ),

                "language": article.get("language"),

                "image_url": article.get("image_url"),

                "matched_symbols": article.get("symbol"),

                "provider_sentiment": article.get("sentiment"),
            })

        return pd.DataFrame(articles)

        #loads specified parameters into the correct format for marketaux
    def get_marketaux(
        self,
        symbols,
        language="en",
        limit=5
    ):

        if self.marketaux_api_key is None:
            raise ValueError(
                "MARKETAUX_API_KEY is missing from .env"
            )

        if isinstance(symbols, list):
            symbols = ",".join(symbols)

        params = {
            "api_token": self.marketaux_api_key,
            "symbols": symbols,
            "filter_entities": "true",
            "language": language,
            "limit": limit,
        }

        data = self._request(
            "https://api.marketaux.com/v1/news/all",
            params
        )

        articles = []

        for article in data.get("data", []):

            entities = article.get("entities", [])

            matched_symbols = []

            sentiments = []

            for entity in entities:

                if entity.get("symbol"):
                    matched_symbols.append(
                        entity["symbol"]
                    )

                sentiment = entity.get(
                    "sentiment_score"
                )

                if sentiment is not None:
                    sentiments.append(sentiment)

            if sentiments:
                average_sentiment = (
                    sum(sentiments)
                    / len(sentiments)
                )
            else:
                average_sentiment = None

            articles.append({
                "source_api": "marketaux",

                "article_id": article.get("uuid"),

                "title": article.get("title"),

                "description": article.get(
                    "description"
                ),

                "content": None,

                "url": article.get("url"),

                "published_at": article.get(
                    "published_at"
                ),

                "publisher": article.get("source"),

                "language": article.get("language"),

                "image_url": article.get(
                    "image_url"
                ),

                "matched_symbols": matched_symbols,

                "provider_sentiment":
                    average_sentiment,
            })

        return pd.DataFrame(articles)

    def get_gdelt(
        self,
        query,
        max_records=50,
        timespan="24h"
    ):

        if max_records > 250:
            raise ValueError(
                "GDELT max_records cannot exceed 250"
            )

        params = {
            "query": query,
            "mode": "ArtList",
            "format": "json",
            "maxrecords": max_records,
            "timespan": timespan,
            "sort": "DateDesc",
        }

        data = self._request(
            "https://api.gdeltproject.org/api/v2/doc/doc",
            params
        )

        articles = []

        for article in data.get("articles", []):

            articles.append({
                "source_api": "gdelt",

                "article_id": article.get("url"),

                "title": article.get("title"),

                "description": None,

                "content": None,

                "url": article.get("url"),

                "published_at": article.get(
                    "seendate"
                ),

                "publisher": article.get(
                    "domain"
                ),

                "language": article.get(
                    "language"
                ),

                "image_url": article.get(
                    "socialimage"
                ),

                "matched_symbols": None,

                "provider_sentiment": None,
            })

        return pd.DataFrame(articles)