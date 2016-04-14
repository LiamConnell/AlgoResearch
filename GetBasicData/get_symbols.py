from urllib.request import Request
from urllib.request import urlopen
import pytz
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
from pandas.io.data import DataReader


SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def scrape_list(site):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)

    table = soup.find('table', {'class': 'wikitable sortable'})
    sector_tickers = dict()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            sector = str(col[3].string.strip()).lower().replace(' ', '_')
            ticker = str(col[0].string.strip())
            if sector not in sector_tickers:
                sector_tickers[sector] = list()
            sector_tickers[sector].append(ticker)
    return sector_tickers


def main():
    ls = scrape_list(SITE)
    sdf = []
    for key in ls:
        for k in ls[key]:
            sdf.append(k)
    return sdf


if __name__ == "__main__":
    print(pd.DataFrame(main()))
