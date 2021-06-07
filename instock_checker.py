import requests
import time
import threading
from threading import Thread, current_thread
import webbrowser
import validators
import sys
from bs4 import BeautifulSoup as bs

def in_stock(url):
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
    soup = bs(r.content, "html.parser")
    availability = soup.find_all('button', class_ ="btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button")
    return len(availability) > 0

def stock_alert(url):
    webbrowser.open_new_tab(url)

def monitor(url):
    sold_out = True
    while sold_out: 
        if in_stock(url):
            stock_alert(url)
            sold_out = False
        else:
            print("Item not yet in stock. Checking again in 10 seconds...")
            time.sleep(10)

def is_url_valid(url):
    if validators.url(url) and "bestbuy" in url:
        return True
    return False
    

# ======================================== #

# URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")
# URL_list = []

# while URL != "Done" or len(URL_list) == 0:
#     valid_url = is_url_valid(URL)
#     if valid_url:
#         URL_list.append(URL)
#         URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")
#     else:
#         print("You have either not provided enough URLs or the URL provided is not valid.")
#         URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")


# while valid_url == False:
#     print("The URL provided is not a valid Best Buy link.")
#     URL = input("Provide a Best Buy link that you would like to monitor the stock of: ")
#     valid_url = is_url_valid(URL)

# sold_out = True
# while sold_out: 
#     if in_stock(URL_list[0]):
#         stock_alert(URL_list[0])
#         sold_out = False
#     else:
#         print("Not yet in stock. Checking again in 30 seconds...")
#         time.sleep(30)

# for link in URL_list:
#     t = threading.Thread(target=monitor, args=(link,))
#     t.start()

def main():
    URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")
    URL_list = []

    while URL != "Done" or len(URL_list) == 0:
        valid_url = is_url_valid(URL)
        if valid_url:
            URL_list.append(URL)
            URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")
        else:
            print("You have either not provided enough URLs or the URL provided is not valid.")
            URL = input("Provide a Best Buy product URL that you would like to monitor the stock of or type 'Done' when you are ready: ")

    monitor(URL_list[-1])

if __name__ == "__main__":
    main()