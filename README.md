# Stock Price Alert with News and Notifications 📈📲

This Python script monitors stock price fluctuations and sends alerts when the price changes by 5% or more compared to the previous day. It also fetches the latest news articles related to the company and sends them as messages via SMS or WhatsApp using Twilio.

## Features
- Fetches daily stock prices using the [Alpha Vantage API](https://www.alphavantage.co/).
- Calculates percentage change between closing prices over two days.
- Sends stock alerts with directional arrows (🔺 or 🔻) indicating the trend.
- Retrieves the latest news articles about the company using the [News API](https://newsapi.org/).
- Delivers alerts and news summaries via:
  - SMS messages
  - WhatsApp messages

## Technologies Used
- **Python**: Core programming language.
- **Twilio API**: For sending SMS and WhatsApp notifications.
- **Alpha Vantage API**: For fetching stock market data.
- **News API**: For fetching relevant news articles.

## Prerequisites
1. Python 3.7 or higher
2. API Keys:
   - [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)
   - [News API Key](https://newsapi.org/docs/get-started)
   - [Twilio credentials (Account SID, Auth Token, phone numbers)](https://www.twilio.com)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stock-price-alert.git
   cd stock-price-alert

2. Install the required Python libraries:
   ```bash
   pip install requests twilio

3. Either create system ```ENV``` variables for these, or create a config.py file in the root directory:
   ```python
   # config.py
    twilio_account_sid = "your_twilio_account_sid"
    twilio_auth_token = "your_twilio_auth_token"
    twilio_sender_phone_number = "your_twilio_phone_number"
    twilio_whatsapp_sandbox_number = "your_twilio_whatsapp_number"
    recipient_phone_number = "recipient's_phone_number"
    alphavantageco_api_key = "your_alpha_vantage_api_key"
    newsapi_key = "your_news_api_key"

4. Set the stock and company name in the script, example shown below:
   ```python
   STOCK = "RIVN"  # Replace with your desired stock symbol
   COMPANY_NAME = "Rivian"  # Replace with the company name

## How to Run
1. Execute the script:
   ```bash
    python main.py

2. If the stock price fluctuates by 5% or more:
- A summary message will be sent to the recipient.
- The latest 3 news articles about the company will also be delivered.

## Example Output
### WhatsApp Alert:
    RIVN: 🔺 5.23%
    Headline: Rivian stock soars after quarterly results
    Brief: Rivian announced stronger-than-expected revenue for Q4.
    Customization
    Headline: Rivian make announcement on expected deliveries
    Brief: Rivian announced that there will be 50,000 deliveries before the end of the quarter.
    Headline: Rivian stock ratings updated by multiple monitoring agencies
    Brief: After the announcements today, here is how the RIVN stock has been graded. 

## Customization
- Stock Symbol: Modify the STOCK variable for your preferred stock.
- Company Name: Change COMPANY_NAME to fetch relevant news articles.
- Notification Type: Use send_sms_message() for SMS or send_whatsapp_message() for WhatsApp.

## License
This project is licensed under the [GNU General Public Use v3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Acknowledgments
- [Alpha Vantage](https://www.alphavantage.co) for stock market data.
- [News API](https://newsapi.org) for news articles.
- [Twilio](https://www.twilio.com) for SMS/WhatsApp services.

## Affiliation
This code is part of the Udemy course "100 Days of Code: The Complete Python Pro Bootcamp" by Dr. Angela Yu and AppBrewery.