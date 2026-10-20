# Energy Stocks News Sentiment Analysis

A Python-based project using a locally hosted Large Language Model (LLM) to analyse financial news and assess its potential impact on publicly traded companies in the nuclear energy sector. News articles are collected through external APIs, analysed for stock-specific sentiment, and stored in a MySQL database through a Flask API hosted on PythonAnywhere.

The aim is to develop a system for tracking news sentiment over time and investigating its relationship with stock price movements.

## Features
- Financial news retrieval using Marketaux and NewsData.io APIs.
- Configurable list of 18 monitored nuclear and energy-related stocks
- Full-text article extraction using Trafilatura
- Local LLM inference using a GGUF model served through llama.cpp
- Stock-specific analysis including:
  - Sentiment score (-1 to +1)
  - Confidence score (0 to 1)
  - Short explanation of the expected financial impact
- Structured JSON output with restrictions to monitored stocks
- Duplicate article detection to avoid repeated analysis
- REST API integration with a Flask backend and MySQL database
- Recording of model and prompt versions alongside analysis results
- API error handling and retry logic

## Project Structure
```text
energystocks-news-sentiment/
├── data/
│   ├── data_connector.py       # News API integrations
│   ├── article_processor.py    # Article processing pipeline
│   ├── fulltext_retriever.py   # Article text extraction
│   └── backend_client.py       # Flask API communication
├── llm_communicator/
│   ├── llm_inputs/
│   │   ├── monitored_stocks.json
│   │   └── system_input.txt
│   └── sentiment_analyser.py   # Local LLM inference
├── config.py                   # Model and prompt configuration
├── main.py                     # Main application entry point
└── requirements.txt            # Python dependencies
```

## Installation & Use

### Installation

Clone the repository and install the dependencies from `requirements.txt`.
The application requires API keys for [Marketaux](https://www.marketaux.com/) and [NewsData.io](https://newsdata.io/), along with access to the separately hosted Flask backend.
Save the following credentials in a `.env` file:

```text
MARKETAUX_API_TOKEN=...
NEWSDATAIO_API_TOKEN=...
ENERGY_API_KEY=...
```

A locally hosted LLM is also required. The application currently communicates with a llama.cpp server through an OpenAI-compatible API at `http://localhost:8080/v1/chat/completions`. The specific parameters for which model to use and some other details can be altered in config.py.

### Use

Edit `monitored_stocks.json` to configure the companies and stock tickers being analysed. The news sources and search parameters can be adjusted in `main.py`.

With the local LLM server and Flask backend running, the application is designed to:

1. Retrieve recent news articles relevant to the monitored stocks.
2. Check whether each article has already been analysed.
3. Extract the full article text and submit it to the local LLM.
4. Generate sentiment and confidence scores for relevant companies.
5. Upload the results to the MySQL database through the Flask API.

## Development

This app is still a work in progress. I plan to extend it to include aggregation of sentiment over time, visualising results through a dashboard, using the gdelt database to track past articles and allow back-testing, and comparing changes in news sentiment with stock price performance.
