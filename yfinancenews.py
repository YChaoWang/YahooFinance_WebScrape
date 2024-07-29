from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import json


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def wait_for_new_elements(driver, previous_count):
    WebDriverWait(driver, 2).until(
        lambda d: len(
            d.find_elements(
                By.XPATH, './/li[contains(@class, "stream-item  yf-7rcxn")]'
            )
        )
        > previous_count
    )


target_stock = input("Input the stock name:").upper()
news_count = int(input("Input the number of news items to scrape:"))

# 設定網站和ChromeDriver路徑
website = f"https://finance.yahoo.com/quote/{target_stock}/news/"
path = "/Users/wangyichao/chromedriver-mac-arm64-3/chromedriver"

# 建立Service物件並傳入ChromeDriver路徑
service = Service(executable_path=path)

# 初始化Chrome WebDriver並傳入Service物件
driver = webdriver.Chrome(service=service)

# 開啟網站
driver.get(website)


news_title = []
upload_time = []
news_agencys = []
news_data = []  # json file containing news_title, upload_time, news_agencys
try:
    with tqdm(
        total=news_count, desc="Processing news items", dynamic_ncols=True, leave=True
    ) as pbar:
        while len(news_title) < news_count:
            container = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//ul[@class="stream-items x-large layoutCol1 yf-1x0cgbi"]',
                    )
                )
            )
            newses = driver.find_elements(
                By.XPATH, './/li[contains(@class, "stream-item  yf-7rcxn")]'
            )
            previous_count = len(newses)

            for news in newses:
                if len(news_title) >= news_count:
                    break

                title = news.find_element(
                    By.XPATH, './/h3[contains(@class, "clamp")]'
                ).text
                news_title.append(title)
                publishing_info = news.find_element(
                    By.XPATH,
                    './/div/div[contains(@class, "footer")]/div[contains(@class, "publishing")]',
                ).text
                # 分割 publishing_info 來獲取新聞機構和時間
                parts = publishing_info.split("•")
                news_agency = parts[0].strip()
                news_agencys.append(news_agency)
                time_info = parts[1].strip()
                upload_time.append(time_info)

                news_item = {
                    "title": title,
                    "news_agency": news_agency,
                    "time": time_info,
                }
                news_data.append(news_item)

                # 更新進度條
                pbar.update(1)
                pbar.set_postfix_str(f"{len(news_title)}/{news_count}")

                tqdm.write(f"title: {title}")
                tqdm.write(f"news_agency: {news_agency}")
                tqdm.write(f"time: {time_info}")
                tqdm.write("--------------------------------")

            if len(news_title) < news_count:
                # 滾動到底部加載更多新聞
                scroll_to_bottom(driver)
                # 等待新的元素加載
                wait_for_new_elements(driver, previous_count)

except Exception as e:
    print("Something went wrong:", e)

# 保存結果為 JSON 文件
output_file = f"{target_stock}_news.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print(f"News data saved to {output_file}")

# 讀取並打印 JSON 文件內容
with open(output_file, "r", encoding="utf-8") as f:
    json_data = json.load(f)
    print("JSON Data:")
    print(json.dumps(json_data, indent=4, ensure_ascii=False))

# 等待使用者輸入，保持瀏覽器開啟
input("Press Enter to close the browser...")

driver.quit()
