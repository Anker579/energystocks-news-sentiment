from data.data_connector import NewsAPIConnector
from data.fulltext_retriever import get_fulltext
from llm_communicator.sentiment_analyser import analyse_sentiment
import json
import time
import subprocess

connector = NewsAPIConnector()

print("\nMARKETAUX")
m_data = connector.get_marketaux(
        ["CCJ", "OKLO"]
    )[["title", "publisher", "matched_symbols","url", "provider_sentiment", "image_url",]]

page_ft = get_fulltext(m_data["url"].iloc[0])
#print(page_ft)

print("\nNEWSDATA")
IO_data = connector.get_newsdataio(
        query="nuclear energy"
    )[["title", "publisher", "url", "image_url",]]

with open("newsdataio.json", "w") as f:
    json.dump(IO_data.to_dict(orient="records"), f, indent=4
    )

with open("marketaux.json", "w") as f:
    json.dump(m_data.to_dict(orient="records"), f, indent=4
    )

#print("\nGDELT")
#print(0
#    connector.get_gdelt(
#        '"nuclear energy"'
#    )[["title", "publisher"]]
#)

with open("page_ft.txt", "w") as f:
    f.write(page_ft)

start = time.perf_counter()

analysed_article = analyse_sentiment(
    article=page_ft,
    title=m_data["title"].iloc[0]
)

analysed_article = json.loads(analysed_article)

end = time.perf_counter()

elapsed = end - start

print(f"Time taken: {elapsed:.3f} seconds")

with open("analysed_article.json", "w") as f:
    json.dump(analysed_article, f, indent=4
    )

subprocess.run([
    "afplay",
    "/System/Library/Sounds/Glass.aiff"
])