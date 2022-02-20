from bs4 import BeautifulSoup
import requests

def scrap_coins(url, coins):
    response=requests.get(url,headers={
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
    })
    soup=BeautifulSoup(response.content, 'lxml')
    for item in soup.select('.simpTblRow'):
        coin = item.select('[aria-label=Symbol]')[0].get_text()
        coins.add(coin)

def scrap_yfinance():
    coins = set()
    for i in range(0,5):
        url = 'https://finance.yahoo.com/cryptocurrencies?count=100&offset=' + str(i * 100)
        scrap_coins(url, coins)
    return coins
