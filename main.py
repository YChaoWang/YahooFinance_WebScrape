import time
import yfinancenews
import googledrive
import os


def main():
    start_time = time.time()  # Record the start time of the program

    try:
        target_stock = input("Input the stock name:").upper()
        news_count = int(input("Input the number of news items to scrape:"))
    except ValueError:
        print("Please input a valid number.")
        exit()

    # Create result directory if it does not exist
    if not os.path.exists("result"):
        os.makedirs("result")

    # Perform news scraping
    yfinancenews.scrape_news(target_stock, news_count)

    # Authenticate and upload files to Google Drive
    drive = googledrive.authenticate()
    googledrive.upload_files(drive)

    end_time = time.time()  # Record the end time of the program
    elapsed_time = end_time - start_time  # Calculate the program's execution time

    print(f"Program execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
