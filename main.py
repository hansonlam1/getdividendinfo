#the main script to try and get dividend information
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

tickers = ["EMA"]
main_dict = {}

for ticker in tickers:
    ticker_dict = {}    #we will append the values for each ticker to a dictionary
    ticker_dict.clear() #clear it out for each ticker
    ticker_dict = ticker_dict.update({"ticker" : ticker })
    page_url = "http://ca.dividendinvestor.com/?symbol=" + ticker + "&submit=GO"
    page_response = requests.get(page_url, headers={'User-Agent':'Mozilla/5.0'},timeout = 5)
    page_content = BeautifulSoup(page_response.content)
    
    tbl = page_content.find_all("table")[15] #div data is in the 16th table tag
    rows = tbl.findChildren("tr")   #go through each row

    for row in rows:    #put everything into a dictionary
        cells = row.findChildren("td")
        for cell in cells:
            #we only want the rows with two values
            print(cell.string)  #build a dictionary to pass into a pandas dataframe later?

        #need to append the data to a list somehow

    #need to only grab the div dates
    #need to compare dates

    main_dict.update(ticker_dict)   #add the ticker dictionary to the main one
    time.sleep(1) #wait a second between requests