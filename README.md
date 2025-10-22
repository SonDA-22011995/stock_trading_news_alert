# 📈 Stock Price Change Notification System

This Python project automatically detects significant stock price changes, retrieves related news articles, and sends email notifications using a customizable HTML template.

---

## 🚀 Overview

The script performs the following main tasks:

1. **Set the reporting date** — choose which day’s data to analyze.  
2. **Load stock data** — either from a JSON file or directly from the API.  
3. **Detect significant price changes** — identify stocks that rise or fall by more than 1%.  
4. **Fetch related articles** — get the latest financial news about these stocks.  
5. **Send email notifications** — generate and send an HTML email report.

---

## 🧩 Code Structure

### 1. Importing modules
```python
import model
from utils import load_html, send_email
```
- `model.py`: Contains logic for API requests, data handling, and analysis.  
- `utils.py`: Provides helper functions to load HTML templates and send emails.

---

### 2. Setting the report date
```python
model.day_to_report(year=2025, month=10, day=18)
```
Defines the date of the stock report.

---

### 3. Loading stock data
```python
model.get_stock_data_from_json_file(file_path="./data/stock_interested_price_data.json")
```
Loads stock data from a local JSON file (used temporarily to avoid API rate limits).

> ⚠️ The Alpha Vantage API allows only **25 requests per day**, so a local JSON file is used for development/testing.

---

### 4. Detecting significant price changes
```python
def get_stock_significant_price_change():
    ...
get_stock_significant_price_change()
```
Detects stocks with a price change greater than or equal to **1%**.  
The results are stored in `model.stock_significant_price_change`.

---

### 5. Fetching related stock news
```python
def get_stock_article():
    ...
get_stock_article()
```
Fetches related articles for each stock that has shown significant price changes, using:
```python
model.get_stock_article_from_api(stock)
```
The articles are stored in `model.stock_articles`.

---

### 6. Sending email notifications
```python
def send_email_notification():
    ...
send_email_notification()
```
Generates an HTML email with placeholders replaced dynamically:
- `{{date}}` → Report date  
- `{{recipient_name}}` → Recipient’s name  
- Stock data: ticker, price change, direction (🔺/🔻), news headlines, links, etc.

Then, it sends the email via SMTP using Gmail settings in `model.config`.

---

## 📁 Folder Structure

```
project/
│
├── data/
│   ├── stock_interested_price_data.json
│   ├── email_template.html
│   └── notification.html
│
├── model.py
├── utils.py
└── main.py
```

---

## ⚙️ Configuration (config.json)

All credentials and API settings are stored in a JSON configuration file, typically named `config.json`:

```json
{
  "send_email": {
    "port": "587",
    "smtp_server": "smtp.gmail.com",
    "user_name": "YOUR_GMAIL_ADDRESS",
    "password": "YOUR_GMAIL_APP_PASSWORD",
    "sender_email": "YOUR_GMAIL_ADDRESS"
  },
  "alpha_vantage": {
    "endpoint": "https://www.alphavantage.co/query",
    "para": {
      "function": "TIME_SERIES_DAILY",
      "symbol": "",
      "outputsize": "compact",
      "datatype": "json",
      "apikey": "YOUR_API_KEY"
    }
  },
  "news": {
    "endpoint": "https://newsapi.org/v2/everything",
    "para": {
      "q": "",
      "apiKey": "YOUR_API_KEY"
    }
  }
}
```

### 🔑 Authentication Notes
- **Alpha Vantage**: Requires a free API key — register at [https://www.alphavantage.co](https://www.alphavantage.co).  
- **News API**: Requires a key from [https://newsapi.org](https://newsapi.org).  
- **Gmail SMTP**: Use an **App Password** (not your normal password) and enable “Less secure app access” if necessary.

---

## 📨 Example Email Output

The email report includes:
- Report date  
- Stocks with significant price changes (🔺 increase / 🔻 decrease)  
- Price change percentage  
- Closing price  
- Related news headlines with short summaries and article links  

---

## 🧠 Notes

- For development, the API calls can be replaced with local JSON data to avoid hitting rate limits.  
- To switch to live data, uncomment:
  ```python
  model.get_stock_data_from_api()
  ```
- Make sure your `config.json` is valid and contains all required keys.

---

## 🛠️ Future Improvements

- Support multiple recipients  
- Add configurable price-change thresholds  
- Store email logs for auditing  
- Add caching and retry mechanisms for APIs  

---

**Author:** Son Dao An  
**Date:** October 2025  
**Purpose:** Automated stock monitoring and email notification system.
