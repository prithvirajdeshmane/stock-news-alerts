import config
import requests
from twilio.rest import Client

# Constants for directional arrows indicating stock movement
UP_ARROW = "\u25B2"  # Up arrow for positive stock movement
DOWN_ARROW = "\u25BC"  # Down arrow for negative stock movement

# Uncomment and update STOCK and COMPANY_NAME as needed
# STOCK = "TSLA"
# COMPANY_NAME = "Tesla Inc"

# Current stock and company being tracked
STOCK = "RIVN"
COMPANY_NAME = "Rivian"

# API endpoints for stock and news data
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Initialize Twilio client with credentials from the config file
client = Client(config.twilio_account_sid, config.twilio_auth_token)

def send_sms_message(body):
    """
    Send an SMS message using Twilio.
    :param body: The message content to be sent.
    """
    message = client.messages.create(
        from_=config.twilio_sender_phone_number,  # Sender's phone number
        body=body,  # Message content
        to=config.recipient_phone_number  # Recipient's phone number
    )
    # Print the message SID and status for debugging purposes
    print(message.sid, message.status)

def send_whatsapp_message(body):
    """
    Send a WhatsApp message using Twilio.
    :param body: The message content to be sent.
    """
    message = client.messages.create(
        from_=f"whatsapp:{config.twilio_whatsapp_sandbox_number}",  # Sender's WhatsApp number
        body=body,  # Message content
        to=f"whatsapp:{config.recipient_phone_number}"  # Recipient's WhatsApp number
    )
    # Print the message SID and status for debugging purposes
    print(message.sid, message.status)

## STEP 1: Fetch stock data from Alpha Vantage
# Compare stock prices between yesterday and the day before yesterday.
# Trigger action if the price change is 5% or greater.

def get_stock_data():
    """
    Fetch stock price data for the past two days.
    :return: List containing closing prices for the last two days.
    """
    # Parameters for Alpha Vantage API request
    params = {
        "function": "TIME_SERIES_DAILY",  # API function to get daily stock data
        "symbol": STOCK,  # Stock symbol
        "outputsize": "compact",  # Request compact data (last 100 data points)
        "apikey": config.alphavantageco_api_key,  # API key for authentication
    }
    # Send GET request to the stock API
    response = requests.get(STOCK_ENDPOINT, params=params)
    response.raise_for_status()  # Raise exception for HTTP errors
    # Parse the daily time series data from the response
    data = response.json().get("Time Series (Daily)", {})
    # Raise an error if insufficient data is available
    if len(data) < 2:
        raise ValueError("Insufficient stock data available.")
    # Extract closing prices for the last two days
    data_list = list(data.items())[:2]
    close_prices = [float(data_list[i][1]["4. close"]) for i in range(2)]
    return close_prices

def calculate_price_change(values):
    """
    Calculate the percentage change in stock price and determine its trend direction.
    :param values: List containing stock prices [yesterday, day before yesterday].
    :return: Absolute percentage change and direction (up/down arrow).
    """
    # Calculate the percentage change in price
    percentage_of_change = ((values[0] - values[1]) / values[1]) * 100
    # Determine direction of change
    trend = UP_ARROW if percentage_of_change > 0 else DOWN_ARROW
    return abs(percentage_of_change), trend

## STEP 2: Fetch news data from News API
def get_latest_news():
    """
    Fetch the latest news articles related to the company.
    :return: List of up to 3 news articles, or an empty list if no articles are available.
    """
    # Parameters for News API request
    params = {
        "language": "en",  # Language for news articles
        "q": COMPANY_NAME,  # Query term for fetching news about the company
    }
    # HTTP headers including auth token
    headers = {
        "X-Api-Key": config.newsapi_key # API key for authentication
    }
    # Send GET request to the news API
    response = requests.get(NEWS_ENDPOINT, params=params, headers=headers)
    response.raise_for_status()  # Raise exception for HTTP errors
    # Extract articles from the response
    articles = response.json().get("articles", [])
    return articles[:3] if articles else []

## Main execution logic
prices = get_stock_data()  # Fetch stock prices

# Check if the stock price increased or decreased 5% or more
if abs((prices[0] - prices[1]) / prices[1]) >= 0.05:
    # Calculate the price change percentage and its trend direction
    change_percentage, direction = calculate_price_change(prices)
    # Create a summary message for the stock movement
    summary_message = f"{STOCK}: {direction} {round(change_percentage, 2)}%"
    send_whatsapp_message(summary_message)  # Send the summary via WhatsApp

    # Fetch the latest news articles
    news_articles = get_latest_news()
    for article in news_articles:
        # Extract and format the headline and description of each article
        headline = article.get("title", "No title")
        description = article.get("description", "No description")
        news_message = f"Headline: {headline}\nBrief: {description}"
        send_whatsapp_message(news_message)  # Send each article via WhatsApp
