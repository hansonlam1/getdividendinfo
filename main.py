#the main script to try and get dividend information
from bs4 import BeautifulSoup
import requests
import time

tickers = ["EMA"]


for ticker in tickers:
    page_url = "http://ca.dividendinvestor.com/?symbol=" + ticker + "&submit=GO"
    print(page_url)
    page_response = requests.get(page_url, headers={'User-Agent':'Mozilla/5.0'},timeout = 5)
    page_content = BeautifulSoup(page_response.content)
    
    tbl = page_content.find_all("table")[15] #div data is in the 16th table tag
    rows = tbl.findChildren("tr")   #go through each row

    for row in rows:
        cells = row.findChildren("td")
        #consider shoving everything into a dictionary and filtering it for what I want later
        for cell in cells:
            print(cell.string)

        #need to append the data to a list somehow

    #need to only grab the div dates
    #need to compare dates

    time.sleep(1) #wait a second between requests