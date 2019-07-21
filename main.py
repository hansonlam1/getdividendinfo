#the main script to try and get dividend information
from bs4 import BeautifulSoup
import requests
import time

tickers = ["EMA","CNR"]

for ticker in tickers:
    page_url = "http://ca.dividendinvestor.com/?symbol=" + ticker + "&submit=GO"
    print(page_url)
    page_response = requests.get(page_url, headers={'User-Agent':'Mozilla/5.0'},timeout = 5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    textContent = []
    for i in range(0,30):
        tablerows = page_content.find_all("tr")[i].text
        textContent.append(tablerows)

    print(textContent)
    #need to add code here to strip out the key info
    time.sleep(1) #wait a second between requests

#use the key info found