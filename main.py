#the main script to try and get dividend information
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import tickerlist

maxdate = datetime.now() + timedelta(days=7)
tickers = tickerlist.TICKERLIST
main_df = pd.DataFrame()

for ticker in tickers:
    ticker_dict = {}    #we will append the values for each ticker to a dictionary
    ticker_dict.clear() #clear it out for each ticker
    ticker_dict = {"ticker" : ticker }
    page_url = "http://ca.dividendinvestor.com/?symbol=" + ticker + "&submit=GO"
    page_response = requests.get(page_url, headers={'User-Agent':'Mozilla/6.0'},timeout = 5)
    page_content = BeautifulSoup(page_response.content)
    tbl = page_content.find_all("table")[15] #div data is in the 16th table tag
    rows = tbl.findChildren("tr")   #go through each row
    for row in rows:
        cells = row.findAll("td")
        if len(cells) > 1:  #only want rows with two cells
            ticker_dict.update({cells[0].text.strip():cells[1].text.strip()})
    main_df = main_df.append(ticker_dict,ignore_index=True)
    print("Processing: " + ticker)
time.sleep(0.2) #throttle it a bit

#filter rows that do not have a div pay date
main_df = main_df.loc[main_df["Dividend Pay Date:"] != "None"]

main_df["Dividend Pay Date:"]=pd.to_datetime(main_df["Dividend Pay Date:"])
main_df["Dividend Ex Date:"]=pd.to_datetime(main_df["Dividend Ex Date:"])
main_df["Dividend Record Date:"]=pd.to_datetime(main_df["Dividend Record Date:"])

main_df = main_df[(main_df["Dividend Pay Date:"]<=maxdate) & (main_df["Dividend Pay Date:"] >= datetime.now())]
main_df.sort_values(by=["Dividend Pay Date:"], inplace=True, ascending=True)
main_df[["ticker","Dividend Pay Date:"]]