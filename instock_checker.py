import requests
import time
import webbrowser
import validators
import sys
from twilio_api import send_sms
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

def monitor(urls, phone_num = None):
    while len(urls) > 0:
        for i in range(len(urls)-1,-1,-1):
            if in_stock(urls[i]):
                url = urls.pop(i)
                if (phone_num != None):
                    send_sms(url, phone_num)
                    print()
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

def check_phone_number():
    phone_number = input("Please provide your valid phone number. Only include digits: ")
    number_check = input("You entered " + str(phone_number) + ". Is this number correct? Y/N ")

    while number_check.upper() != "Y" and number_check.upper() != "N":
        number_check = input("Invalid response. You entered " + str(phone_number) + ". Is this number correct? Y/N ")
    
    if number_check.upper() == "N":
        return check_phone_number()
    
    return phone_number

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

    alert_sms = input("Do you want to receive SMS alerts if an item is in stock? Y/N ")
    phone_number = None

    while alert_sms.upper() != "Y" and alert_sms.upper() != "N":
        alert_sms = input("Invalid response. Do you want to receive SMS alerts if an item is in stock? Y/N")

    if alert_sms.upper() == "Y":
        phone_number = check_phone_number()

    monitor(URL_list, phone_number)

if __name__ == "__main__":
    main()