from utils import load_csv_data, call_api, load_json_data, is_change_by_percent, load_config, change_by_percent
from datetime import datetime
from datetime import timedelta


config = load_config("./data/config.json")


days = []
stock_interested_price_data = []
stock_significant_price_change = []
stock_articles = []

def day_to_report(year, month, day):
    global days
    today = datetime(year, month, day)
    days = [today - timedelta(days=i) for i in range(1,3)]

def get_stock_article_from_api(stock: dict):
    global stock_articles

    new_para_stock = config["news"]["para"]
    new_para_stock["q"] = stock.get("name")

    article_data = call_api(
        method="GET",
        url=config["news"]["endpoint"],
        params= new_para_stock
    )

    if len(article_data.get("articles")) > 0:
        article = {
            "code": stock.get("code"),
            "name": stock.get("name"),
            "articles" : article_data.get("articles")[:3]
        }

        stock_articles.append(article)

def get_stock_data_from_api():
    global stock_interested_price_data
    stock_interested_data = load_csv_data(path="./data/stock.csv")
    if len(stock_interested_data) > 0:
        for stock in stock_interested_data:
            alpha_vantage_para_stock = config["alpha_vantage"]["para"]
            alpha_vantage_para_stock["symbol"] = stock.get("code")

            stock_data = call_api(
                method="GET",
                url=config["alpha_vantage"]["endpoint"],
                params= alpha_vantage_para_stock
            )

            prices = {}
            for day in days:
                try:
                    prices[day.strftime("%Y-%m-%d")] = stock_data["Time Series (Daily)"][day.strftime("%Y-%m-%d")]
                except KeyError as e:
                    print(f"No stock market data is available on {e}")
                    prices[day.strftime("%Y-%m-%d")] = {}

            stock["prices"] = prices
            stock_interested_price_data.append(stock)

def get_stock_data_from_json_file(file_path):
    global stock_interested_price_data
    stock_interested_price_data =  load_json_data(file_path)

def has_significant_price_change(stock, ratio):
    prices = []
    for day in days:
        price = stock["prices"][day.strftime("%Y-%m-%d")]["4. close"] \
            if len(stock["prices"][day.strftime("%Y-%m-%d")]) > 0 else 0
        prices.append(price)
    if is_change_by_percent(value1=float(prices[1]), value2=float(prices[0]), ratio=ratio):
        print(f"{stock["name"]} has change")
        return change_by_percent(float(prices[1]),float(prices[0]))
    print(f"{stock["name"]} has not change much")
    return False

def get_close_price(stock):
    return stock["prices"][days[0].strftime("%Y-%m-%d")]["4. close"]

def is_up_trend(stock):
    return stock["prices"][days[0].strftime("%Y-%m-%d")]["4. close"] >= stock["prices"][days[1].strftime("%Y-%m-%d")]["4. close"]













