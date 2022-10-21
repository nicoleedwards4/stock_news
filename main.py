import requests
import smtplib
import creds

my_gmail = creds.my_gmail
gmail_pw = creds.gmail_pw
my_yahoo = creds.my_yahoo

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = creds.STOCK_ENDPOINT
stock_api = creds.stock_api
NEWS_ENDPOINT = creds.NEWS_ENDPOINT
news_api = creds.news_api

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": news_api
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]

closing_yesterday = float(data_list[0]["4. close"])
closing_before_yesterday = float(data_list[1]["4. close"])

change = (closing_before_yesterday-closing_yesterday)/closing_before_yesterday
change_symbol = "🔺" if change > 0 else "🔻" if change < 0 else ""

if change < -.05 or change > .05:
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response.raise_for_status()
    news_data = response.json()["articles"][:3]
    for article in news_data:
        article_title = article["title"]
        article_description = article["description"]
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_gmail, password=gmail_pw)
            connection.sendmail(
                from_addr=my_gmail,
                to_addrs=my_yahoo,
                msg=f"{STOCK} {change_symbol}\n\nHeadline: {article_title}\nBrief: {article_description}")
