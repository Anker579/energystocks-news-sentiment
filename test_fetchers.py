from data.data_connector import NewsAPIConnector
from data.fulltext_retriever import get_fulltext
from data.article_processor import process_articles
from llm_communicator.sentiment_analyser import analyse_sentiment
from data.backend_client import  add_article, add_analysis, check_article
import json
import time
import subprocess

MODEL="Qwen/Qwen3-4B-GGUF:Q4_K_M"
PROMPT_VERSION="v1"

connector = NewsAPIConnector()

#print("\nMARKETAUX")
m_data = connector.get_marketaux(
        ["CCJ", "OKLO"]
    )[["title", "publisher", "matched_symbols","url", "provider_sentiment", "image_url",]]

#page_ft = get_fulltext(m_data["url"].iloc[0])
#print(page_ft)

#print("\nNEWSDATA")
IO_data = connector.get_newsdataio(
        query="nuclear energy"
    )[["title", "publisher", "url", "image_url",]]

#with open("newsdataio.json", "w") as f:
#    json.dump(IO_data.to_dict(orient="records"), f, indent=4
#    )
#
#with open("marketaux.json", "w") as f:
#    json.dump(m_data.to_dict(orient="records"), f, indent=4
#    )

#print("\nGDELT")
#print(0
#    connector.get_gdelt(
#        '"nuclear energy"'
#    )[["title", "publisher"]]
#)

#for i in range(len(m_data)):
#
#    url = m_data["url"].iloc[i]
#    title = m_data["title"].iloc[i]
#    publisher = m_data["publisher"].iloc[i]
#
#    print(f"\nChecking article {i + 1}/{len(m_data)}")
#    print(title)
#
#    check_result = check_article(url)
#
#    if check_result["exists"] and check_result["status"] == "analysed":
#        print("Already analysed - skipping")
#        continue
#
#    if check_result["exists"]:
#        article_id = check_result["article_id"]
#
#    else:
#        add_result = add_article(
#            url=url,
#            title=title,
#            publisher=publisher,
#            source_api="marketaux"
#        )
#
#        article_id = add_result["article_id"]
#
#    page_ft = get_fulltext(url)
#
#    start = time.perf_counter()
#
#    analysed_article = analyse_sentiment(
#        article=page_ft,
#        title=title
#    )
#
#    analysed_article = json.loads(analysed_article)
#
#    end = time.perf_counter()
#
#    print(f"LLM time: {end - start:.3f} seconds")
#
#    upload_result = add_analysis(
#        article_id=article_id,
#        analysis=analysed_article,
#        model=MODEL,
#        prompt_version=PROMPT_VERSION
#    )
#
#    print(upload_result)

process_articles(m_data, "marketaux")
process_articles(IO_data, "newsdataio")

subprocess.run([
    "afplay",
    "/System/Library/Sounds/Glass.aiff"
])