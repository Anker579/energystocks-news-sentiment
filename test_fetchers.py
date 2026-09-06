from data.data_connector import NewsAPIConnector
import json
from data.fulltext_retriever import get_fulltext

connector = NewsAPIConnector()

print("\nMARKETAUX")
m_data = connector.get_marketaux(
        ["CCJ", "OKLO"]
    )[["title", "publisher", "matched_symbols","url", "provider_sentiment", "image_url",]]

page_ft = get_fulltext(m_data["url"].iloc[0])
print(page_ft)

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