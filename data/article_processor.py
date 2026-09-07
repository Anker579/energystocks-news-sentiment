import json
import time
import config

from data.backend_client import add_article, add_analysis, check_article
from data.fulltext_retriever import get_fulltext
from llm_communicator.sentiment_analyser import analyse_sentiment


MODEL = config.MODEL
PROMPT_VERSION = config.PROMPT_VERSION


def process_articles(data, source_api):

    for i in range(len(data)):

        url = data["url"].iloc[i]
        title = data["title"].iloc[i]
        publisher = data["publisher"].iloc[i]

        print(f"\nChecking article {i + 1}/{len(data)}")
        print(title)

        try:
            check_result = check_article(url)

            if (
                check_result["exists"]
                and check_result["status"] == "analysed"
            ):
                print("Already analysed - skipping")
                continue

            if check_result["exists"]:
                article_id = check_result["article_id"]

            else:
                add_result = add_article(
                    url=url,
                    title=title,
                    publisher=publisher,
                    source_api=source_api
                )

                article_id = add_result["article_id"]

            page_ft = get_fulltext(url)

            if not page_ft:
                print("Could not retrieve full text - leaving pending")
                continue

            #time how long the llm takes to process an article
            start = time.perf_counter()

            analysed_article = analyse_sentiment(
                article=page_ft,
                title=title
            )

            analysed_article = json.loads(analysed_article)

            end = time.perf_counter()

            print(f"LLM time: {end - start:.3f} seconds")

            upload_result = add_analysis(
                article_id=article_id,
                analysis=analysed_article,
                model=MODEL,
                prompt_version=PROMPT_VERSION
            )

            print(upload_result)

        except Exception as error:
            print(f"Failed to process article: {error}")
            continue