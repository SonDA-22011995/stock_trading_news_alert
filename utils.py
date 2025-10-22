import requests
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError
from pathlib import Path
import pandas
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def load_config(file_path: str):
    config_path = Path(file_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file is not found: {file_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)



def send_email(port, smtp_server, user_name,
               password, sender_email,
               receiver_email, html_template,
               subject = "Motivational quotes on mondays"
               ):

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the HTML part
    message.attach(MIMEText(html_template, "html"))

    # Send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(user_name, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def load_html(path):
    path = Path(path)
    if path.exists():
        html = path.read_text(encoding="utf-8")
        return html
    return ""

def load_csv_data(path):
    data = []
    path = Path(path)
    if path.exists():
       for index, row in pandas.read_csv(path).iterrows():
           data.append(row.to_dict())
    return data

def load_json_data(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File is not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def call_api(method, url, headers=None, params=None, data=None, json=None, timeout=10):
    """
    Hàm gọi API tổng quát bằng requests
    :param method: GET, POST, PUT, DELETE
    :param url: Endpoint API
    :param headers: dict - Header gửi kèm
    :param params: dict - Query string (?key=value)
    :param data: dict - Form data
    :param json: dict - JSON body
    :param timeout: Thời gian chờ tối đa (giây)
    :return: dict - Response JSON hoặc thông báo lỗi
    """
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            timeout=timeout
        )

        # Kiểm tra mã HTTP
        response.raise_for_status()

        # Nếu server trả về JSON
        try:
            return response.json()
        except ValueError:
            return {"message": "Response is not valid JSON", "raw_text": response.text}

    except HTTPError as e:
        return {"error": f"HTTP error occurred: {e}", "status_code": response.status_code}
    except ConnectionError:
        return {"error": "Connection error occurred"}
    except Timeout:
        return {"error": "Request timed out"}
    except RequestException as e:
        return {"error": f"Unexpected error: {e}"}

def is_change_by_percent(value1, value2, ratio):
    try:
        change_ratio = (value2 - value1) / value1
        return abs(change_ratio) >= ratio
    except ZeroDivisionError as e:
        print(f"The value1 is 0 {e}")
        return False

def change_by_percent(value1, value2):
    try:
        change_ratio = (value2 - value1) / value1
        return abs(change_ratio)
    except ZeroDivisionError as e:
        print(f"The value1 is 0 {e}")
        return 0

def is_increase_by_percent(value1, value2, ratio):
    try:
        return (value2 - value1)/value1 >= ratio
    except ZeroDivisionError as e:
        print(f"The value1 is 0 {e}")
        return False

def is_decrease_by_percent(value1, value2, ratio):
    try:
        return (value1 - value2)/value1 >= ratio
    except ZeroDivisionError as e:
        print(f"The value1 is 0 {e}")
        return False