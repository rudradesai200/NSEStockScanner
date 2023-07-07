import pandas as pd
import pandas_ta as ta
import yfinance

class DataLoader:
    def __init__(self, indicators_config: dict, data_dir: str = "StockData/"):
        self.data_dir = data_dir
        self.indicators_config = indicators_config

    def AddIndicator(self, data: pd.DataFrame):
        """
        Adds techincal indicators to the dataframe
        Supports `EMA`, `SMA`, `RSI`, `BB`, `EWO` and `StochRSI`
        """

        apply_col = data[self.indicators_config['field']]
        for val in self.indicators_config.get('EMA', []):
            data['EMA'+str(val)] = ta.ema(close=apply_col, length=val)
        for val in self.indicators_config.get('SMA', []):
            data['SMA'+str(val)] = ta.sma(close=apply_col, length=val)

        if 'RSI' in self.indicators_config.keys():
            data['RSI'] = ta.rsi(apply_col, self.indicators_config['RSI'])

        if 'BB' in self.indicators_config.keys():
            suffix = f"_{self.indicators_config['BB']['ma']}_{self.indicators_config['BB']['stddev']}.0"
            data[['BBLower', 'BBMedian', 'BBUpper']] = ta.bbands(
                apply_col, self.indicators_config['BB']['ma'], self.indicators_config['BB']['stddev'])[['BBL'+suffix, 'BBM'+suffix, 'BBU'+suffix]]
            data['BBNeck%'] = ((data["BBUpper"] - data["BBLower"]) * 100.0)/(data["BBMedian"])

        if 'StochRSI' in self.indicators_config.keys():
            data[['StochRSIFast', 'StochRSISlow']] = ta.stochrsi(apply_col)

        if 'MACD' in self.indicators_config.keys():
            macd_dict = self.indicators_config['MACD']
            data[['macd','macd_histogram','macd_signal']] = ta.macd(apply_col,macd_dict.get('fast',12),macd_dict.get('slow',26),macd_dict.get('signal',9))

        if 'OBV' in self.indicators_config.keys():
            data['obv'] = ta.obv(apply_col,data['volume'])

        if 'EWO' in self.indicators_config.keys():
            data['ewo'] = ta.sma(apply_col, '5') - ta.sma(apply_col, '35')

        return data

    def cleanData(self, data: pd.DataFrame):
        data.drop_duplicates(inplace=True)
        data.rename(columns=lambda x: str(x).replace(' ', '').replace('.', '').lower(), inplace=True)
        data.drop(columns=['series', "value"], inplace=True)
        # Remove ',' from all numerical values for converting it to float later on
        data = data.applymap(lambda x: str(x).replace(',', ''))

        # Convert given Date format to standard date format
        # pat = r"(?P<day>\d{2})-(?P<month>\w{3})-(?P<year>\d{4})"
        # dates = {"Jan": '01', "Feb": '02', "Mar": '03', "Apr": '04', "May": '05', "Jun": '06',
        #          "Jul": '07', "Aug": '08', "Sep": '09', "Oct": '10', "Nov": '11', "Dec": '12'}

        # def repl(m): return m.group('year') + '-' + dates[m.group('month')] + '-' + m.group('day')

        # Set date as the index
        # data['date'] = data['date'].str.replace(pat, repl, regex=True)
        data = data.set_index('date', drop=True)
        data = data.sort_index(ascending=True)
        # Convert all remaining values to float
        data = data.astype('float64')

        # Reverse the dataframe to keep recent prices at the top
        # data = data.iloc[::-1]
        return data

    def getTickerData(self, ticker: str, interval: str = "1d", period: str = "730d") -> pd.DataFrame:
        """
        Tries to load data from yfinance. If ticker not found, tries to load it from the files stored in `data_dir` and cleans it for easier access. Supports TEST.
        """
        # Load data from yfinance
        data = yfinance.Ticker(ticker if ticker.endswith(".NS") else ticker + ".NS").history(interval=interval, period=period)
        if data is None:
            print("yfinance didn't find the ticker. Trying to load the custom data from " + self.data_dir + ticker + ".csv")

            # Load data and remove [' ','.'] from column names
            data = pd.read_csv(self.data_dir + ticker + ".csv")

            # Clean data
            data = self.cleanData(data)
        else:
            # Clean yfinance data
            data.rename(columns=lambda x: str(x).replace(' ', '').replace('.', '').lower(), inplace=True)

        # Check for data length
        if len(data) < self.indicators_config['requiredDataLength']:
            print("Error: Not sufficient data")
            return None

        if data is not None:
            # Add indicators
            data = self.AddIndicator(data)

        return data.iloc[::-1]