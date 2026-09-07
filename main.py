from data.data_connector import NewsAPIConnector
from data.article_processor import process_articles
import json

connector = NewsAPIConnector()

with open("llm_communicator/llm_inputs/monitored_stocks.json", "r") as f:
    monitored_stocks = json.load(f)

monitored_tickers = list(monitored_stocks.keys())

print("\nMARKETAUX")
m_data = connector.get_marketaux(
        monitored_tickers
    )[["title", "publisher", "matched_symbols","url", "provider_sentiment", "image_url",]]

print("\nNEWSDATAIO")
IO_data = connector.get_newsdataio(
        query="nuclear energy"
    )[["title", "publisher", "url", "image_url",]]
 
process_articles(m_data, "marketaux")
process_articles(IO_data, "newsdataio")