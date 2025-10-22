import model
from utils import load_html, send_email

# Day to report
model.day_to_report(year=2025, month=10, day=18)
# Official, user model.py to call api
# model.get_stock_data_from_api()
# Temporary
# Use a JSON file instead of calling the API
# , because the API rate limit is 25 requests per day.
model.get_stock_data_from_json_file(file_path="./data/stock_interested_price_data.json")


def get_stock_significant_price_change():
    if len(model.stock_interested_price_data) > 0:
        for stock in model.stock_interested_price_data:
            if price_change := model.has_significant_price_change(stock=stock, ratio=0.01):
                stock["price_change"] = price_change
                model.stock_significant_price_change.append(stock)
    else:
        print("get_stock_significant_price_change: Does not work at all")
        return


get_stock_significant_price_change()

def get_stock_article():
    if len(model.stock_significant_price_change) > 0:
        for stock in model.stock_significant_price_change:
            model.get_stock_article_from_api(stock)
    else:
        print("get_stock_article: Does not work at all")
        return

get_stock_article()

def send_email_notification():
    if len(model.stock_articles) > 0:
        html_template = load_html(path="./data/email_template.html")
        html_template = html_template.replace("{{date}}", model.days[0].strftime("%d/%m/%Y"))
        html_template = html_template.replace("{{recipient_name}}", "Mr. Son Dao An")
        stock_item_list = ""
        stock_item = load_html(path="./data/notification.html")
        for stock in model.stock_significant_price_change:
            change_symbol = "🔺" if model.is_up_trend(stock) else "🔻"
            stock_article = [article for article in model.stock_articles if article.get("code") == stock.get("code")]
            for article in stock_article[0]["articles"]:
                stock_item_temp = stock_item
                stock_item_temp = stock_item_temp.replace("{{ticker}}", stock.get("code"))
                stock_item_temp = stock_item_temp.replace("{{change_symbol}}", change_symbol)
                stock_item_temp = stock_item_temp.replace("{{change_percent}}", f"{round(stock.get("price_change")*100,2)}%")
                stock_item_temp = stock_item_temp.replace("{{close_price}}", f"{model.get_close_price(stock)}")
                stock_item_temp = stock_item_temp.replace("{{headline}}", f"{article["title"]}")
                stock_item_temp = stock_item_temp.replace("{{brief}}", f"{article["content"]}")
                stock_item_temp = stock_item_temp.replace("{{article_url}}", f"{article["url"]}")
                
                stock_item_list += stock_item_temp

        html_template = html_template.replace("{{stock_item}}", stock_item_list)

        send_email(
            port=model.config["send_email"]["port"],
            smtp_server=model.config["send_email"]["smtp_server"],
            user_name=model.config["send_email"]["user_name"],
            password=model.config["send_email"]["password"],
            sender_email=model.config["send_email"]["sender_email"],
            receiver_email="sonda@biahalong.com",
            subject="Stock significant price change",
            html_template=html_template
        )
    else:
        print("get_stock_article: Does not work at all")
        return

send_email_notification()


