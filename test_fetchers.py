from data.data_connector import NewsAPIConnector
import json

connector = NewsAPIConnector()


print("\nMARKETAUX")
m_data = connector.get_marketaux(
        ["CCJ", "OKLO"]
    )[["title", "publisher", "matched_symbols"]]


print("\nNEWSDATA")
IO_data = connector.get_newsdataio(
        query="nuclear energy"
    )[["title", "publisher", "content"]]

with open("newsdataio.json", "w") as f:
    json.dump(IO_data.to_dict(orient="records"), f, indent=4
    )

with open("marketaux.json", "w") as f:
    json.dump(m_data.to_dict(orient="records"), f, indent=4
    )

#print("\nGDELT")
#print(
#    connector.get_gdelt(
#        '"nuclear energy"'
#    )[["title", "publisher"]]
#)