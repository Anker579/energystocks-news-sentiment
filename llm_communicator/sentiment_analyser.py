import requests

def analyse_sentiment(article: str, title: str) -> dict:
    response = requests.post(
       "http://localhost:8080/v1/chat/completions",
       json={
           "model": "local-model",
           "messages": [
               {
                   "role": "system",
                   "content": "You are a stock market news sentiment analysis assistant. You will be provided with fulltext news articles and you will provide for each article: a boolean of whether the article matches the title provided, the relevant stock symbols or companies, a sentiment score for each and your confidence level on a scale of 0 to 1 on the sentiment score for each. The sentiment score should be a number between -1 and 1, where -1 indicates very negative sentiment, 0 indicates neutral sentiment, and 1 indicates very positive sentiment. Your answer should be returned as a python dictionary. If the article does not match the title, return a sentiment score of 0 and an empty list of stock symbols or companies."
               },
               {
                   "role": "user",
                   "content": f"The fulltext article: {article}, the title: {title}."
               }
           ],
           "temperature": 0
       }
    )
    r = response.json()["choices"][0]["message"]["content"]
    #print(r)
    return r