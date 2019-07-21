#the main script to try and get dividend information
from bs4 import BeautifulSoup
import requests
import time

tickers = ["EMA"]
data = []

for ticker in tickers:
    page_url = "http://ca.dividendinvestor.com/?symbol=" + ticker + "&submit=GO"
    print(page_url)
    page_response = requests.get(page_url, headers={'User-Agent':'Mozilla/5.0'},timeout = 5)
    page_content = BeautifulSoup(page_response.content)
    
    tbl = page_content.find_all("table")[15] #div data is in the 16th table tag

    #go through each row then column
    rows = tbl.find_all("tr")  
    for row in rows:
        #get the columns in each row
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    print(data)
    #need to add code here to strip out the key info
    time.sleep(1) #wait a second between requests

#use the key info found

