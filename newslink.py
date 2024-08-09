from bs4 import BeautifulSoup
import requests
from datetime import datetime


def extract_date_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        content = result.text
        soup = BeautifulSoup(content, "lxml")
        datetime_string = soup.find("time").get("datetime")
        time_obj = datetime.fromisoformat(datetime_string[:-1])  # 去掉最后的 'Z'
        date_part = time_obj.date().isoformat()
        return date_part
    else:
        return None
