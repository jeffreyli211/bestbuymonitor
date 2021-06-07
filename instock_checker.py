import requests
import time
# import threading
# from threading import Thread, current_thread
# import multiprocessing
import webbrowser
import validators
import sys
from bs4 import BeautifulSoup as bs

def read_urls(filename):
    url_list = []
    f = open(filename, 'r')
    for line in f:
        url_list.append(line)
    return url_list

def in_stock(url):
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
    soup = bs(r.content, "html.parser")
    availability = soup.find_all('button', class_ ="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button")
    return len(availability) > 0

def stock_alert(url):
    webbrowser.open_new_tab(url)

def monitor(urls):
    # sold_out = True
    # while sold_out: 
    #     if in_stock(url):
    #         stock_alert(url)
    #         sold_out = False
    #     else:
    #         print("Item not yet in stock. Checking again in 10 seconds...")
    #         time.sleep(10)
    while len(urls) > 0:
        for i in range(len(urls)-1,-1,-1):
            if in_stock(urls[i]):
                url = urls.pop(i)
                stock_alert(url)
        if len(urls) > 0:
            print("Some items still not in stock. Checking again in 10 seconds...")
            print("Current list of monitors: ")
            for url in urls:
                print(url)
            time.sleep(10)
    print("All items have been checked and are now in stock.")

def is_url_valid(url):
    if validators.url(url) and "bestbuy" in url:
        return True
    return False
    

# ======================================== #

def main():
    URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")
    URL_list = [] #read_urls('test_list.txt')   # Used for testing purposes

    while URL != "Done" or len(URL_list) == 0:
        valid_url = is_url_valid(URL)
        if valid_url:
            URL_list.append(URL)
            URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")
        else:
            print("You have either not provided enough URLs or the URL provided is not valid.")
            URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")

    monitor(URL_list)

if __name__ == "__main__":
    main()