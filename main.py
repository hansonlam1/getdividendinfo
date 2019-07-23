#the main script to try and get dividend information
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from datetime import datetime, timedelta

maxdate = datetime.now() + timedelta(days=7)
tickers = pd.read_csv("https://web.tmxmoney.com/constituents_data.php?index=^TX60&index_name=S%26P%2FTSX+60+Index+%28CAD%29",skiprows=4)
tickers = tickers["Symbol"].tolist()
main_df = pd.DataFrame()

for ticker in tickers:
    ticker_dict = {}    #we will append the values for each ticker to a dictionary
    ticker_dict.clear() #clear it out for each ticker
    ticker_dict = {"ticker" : ticker }
    page_url = "http://ca.dividendinvestor.com/?symbol=" + ticker + "&submit=GO"
    page_response = requests.get(page_url, headers={'User-Agent':'Mozilla/5.0'},timeout = 5)
    page_content = BeautifulSoup(page_response.content)
    tbl = page_content.find_all("table")[15] #div data is in the 16th table tag

    rows = tbl.findChildren("tr")   #go through each row
    for row in rows:
        cells = row.findAll("td")
        if len(cells) > 1:  #only want rows with two cells
            ticker_dict.update({cells[0].text.strip():cells[1].text.strip()})
    main_df = main_df.append(ticker_dict,ignore_index=True)

time.sleep(0.3) #throttle it a bit

main_df["Dividend Pay Date:"]=pd.to_datetime(main_df["Dividend Pay Date:"])
main_df["Dividend Ex Date:"]=pd.to_datetime(main_df["Dividend Ex Date:"])
main_df["Dividend Record Date:"]=pd.to_datetime(main_df["Dividend Record Date:"])
main_df = main_df[main_df["Dividend Pay Date:"]<=maxdate]
main_df[["ticker","Dividend Ex Date:","Dividend Pay Date:"]]