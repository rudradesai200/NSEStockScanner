import requests
import datetime
from typing import  List
from urllib.parse import quote_plus
import logging
logging.basicConfig(level=logging.INFO)

class DataFetcher:
    def _getCookie(self):
        resp = requests.get("https://www.nseindia.com", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })
        cookies = resp.cookies
        # cookies = "; ".join(key + "=" + val for key, val in cookies.items())
        return cookies

    def getCSV(self, symbol:str, date_start_off:int = 365, date_end_off:int = 0, updating:bool = False):
        logging.info(f"==== Fetching symbol {symbol}")
        def getDate(dayoff:int = 0):
            date = datetime.datetime.today() - datetime.timedelta(days=dayoff)
            return str(date.day) + '-' + (str(date.month) if date.month >= 10 else str('0' + str(date.month))) + '-' + str(date.year)

        url = "https://www.nseindia.com/api/historical/cm/equity"
        params = {
            "symbol": symbol,
            "series": "[\"EQ\"]",
            "from": getDate(date_start_off),
            "to": getDate(date_end_off),
            "csv": "True"
        }
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=" + quote_plus(symbol)
        }

        logging.debug(f"Trying to connect to url: {url}")

        resp = requests.get(url, params=params, headers= headers, cookies=self.cookies, timeout=10)
        content = resp.content
        if resp.status_code != 200:
            logging.error(f"Failed fetching data for {symbol}")
            return False

        if resp.content.startswith(b"{\"error\":true"):
            logging.error(f"Failed fetching data for {symbol} with {resp.content}")
            return False

        with open("../StockData/" + symbol + ".csv", "a") as fp:
            content = content.decode("utf-8-sig")
            lines = content.split("\n")

            if updating:
                lines = lines[1:]

            for line in lines:
                fp.write(line + "\n")

        logging.info(f"==== symbol {symbol} fetched")
        return True

    def fetch(self, symbols: List[str], num_years: int = 10):
        self.cookies = self._getCookie()
        print(self.cookies)
        year = 0
        for symbol in symbols:
            for year in range(num_years):
                if not (self.getCSV(symbol, (year+1)*365, year*365, (year != 0))):
                    break

if __name__ == "__main__":
    loader = DataFetcher()
    loader.fetch(["RELIANCE", "TATAMOTORS", "TATASTEEL", "HINDUNILVR", "COALINDIA", "IRCTC", "BHEL", "TITAN", "IEX", "AXISBANK"], num_years=10)
