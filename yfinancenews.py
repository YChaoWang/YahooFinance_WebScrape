from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import json
import os
from webdriver_manager.chrome import ChromeDriverManager


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


def scrape_news(target_stock, news_count):
    website = f"https://finance.yahoo.com/quote/{target_stock}/news/"
    print(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(website)

    news_title = []
    upload_time = []
    news_agencys = []
    news_data = []

    try:
        with tqdm(
            total=news_count,
            desc="Processing news items",
            dynamic_ncols=True,
            leave=True,
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

                    pbar.update(1)
                    pbar.set_postfix_str(f"{len(news_title)}/{news_count}")

                    tqdm.write(f"title: {title}")
                    tqdm.write(f"news_agency: {news_agency}")
                    tqdm.write(f"time: {time_info}")
                    tqdm.write("--------------------------------")

                if len(news_title) < news_count:
                    scroll_to_bottom(driver)
                    wait_for_new_elements(driver, previous_count)

    except Exception as e:
        print("Something went wrong:", e)

    output_file = f"result/{target_stock}_news.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

    print(f"News data saved to {output_file}")
    driver.quit()
