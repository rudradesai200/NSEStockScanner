# NSEStockScanner
- NSEStockScanner is a python script made to analyse NSE tickers on a technical basis currently.
- FundamentalAnalysis module and AIPrediction module will be added on a later stage.

## Setup
- Install required modules using `pip install -r requirements.txt`
- Use `DataFetcher` class from `DataFetcher.py` to fetch data.

## Fetching Data
- `DataFetcher.py` can be used for fetching data from the NSE website and storing it into `StockData` directory
- The fetched data is cleaned by `DataLoader` when loaded
- It contains the following columns for each ticker.
    - [`open`,`high`,`low`,`prevclose`,`ltp`,`close`,`vwap`,`52wh `,`52wl`,`volume`,`value`,`nooftrades`]
- The data is indexed by the date. All the above columns can be used directly in the signal configurations in place of the fields.

## Running Analysis
- After following the above steps, create a new config file or use the pre-existing one stored in `configs` directory.
- Edit the `analysis.py` file as per your use.
  
## Making your own Config
- Config directory has various scripts containing description of the indicator and the technical indications to be used. The general format along with fields is described below
- Generally, one can store 2 different sections for each configuration - `DataConfig` and `TickerConfig`

### DataConfig
- It contains information about the indicators to be added in the dataframe before analysis
- It requires a `field` tag containing a valid data columns described above.
- It supports following 5 indicators currently
    - `EMA` : Exponential Moving Average
        - Input: List of periods. Ex: `EMA`: [13, 52]
        - It can be accessed as `EMA13` or `EMA52`
    - `SMA` : Simple Moving Average
        - Input: List of periods. Ex: `SMA`: [200]
        - It can be accessed as `SMA200`
    - `RSI` : Relative Strength Index
        - Input: RSI Period. Ex: `RSI`: 14
        - It can be accessed as `RSI`
    - `BB`  : Bollinger Bands
        - Input: Dictionary with `ma` field representing Moving Average time and `stddev` field representing StdDeviation period
        - It can be accessed as `BBUpper`, `BBMedian`, `BBLower`, `BBNeck%`
    - `StochRSI` : Stochastic RSI
        - Input: Boolean
        - It can be accessed as `StochRSI`
    - `MACD` : Moving Average Convergence Divergence
        - Input: dict with `fast`, `slow` and `signal` period
        - It can be accessed as `macd`, `macd_histogram`, `macd_signal`
    - `OBV`: On Balance Volume
        - Input: Boolean
        - It can be accessed as `obv`
    - `EWO`: Elliot Wave Oscillator
        - Input: Boolean
        - It can be accessed as `ewo`

### TickerConfig
- It contains description of the signals for analysis.
- It requires `name` and `requiredDataLength` field. `requiredDataLength` represents the minimum required data for analysis
- `cutoff` field is auto evaluated based on the `score` provided in the confirmations, indicators and conditions. It can also be passed manually. Only symbols with `Severity` above `cutoff` will be present in the final recommendation.
- The configuration is divided into 3 sections
    - `conditions` : Represents signals that must be valid before analysis
    - `indicators` : Represents signals that indicate bullish movements. `Atleast` one indicator needs to be true for the ticker to pop up in final recommendation
    - `confirmations`: Represents signals that acts as a confimation. 
- Each signal is passed as a dictionary or a list of dictionary. Each dictionary must contain the following fields. List of dictionary will be `and`ed while evaluation
    - `type` : Type of signal out of the below available types
    - `color` : Color indicates sentiment for the signal ranging from -3 to +3, where +3 = GREEN and -3 = RED. 0 = Information (Neutral)
    - `score` : Score represents importance of this indicator, higher the importance more it contributes to the final `Severity` of the symbol.
- Currently, following signals types are supported along with their required parameters,
    - `comparePlus`: Signals true if `field1` is higher than `field2` in the last candle
        - Required fields - `field1:(str | num)` and `field2:(str | num)`
    - `compareMinus`: Signals true if `field1` is lower than `field2` in the last candle
        - Required fields - `field1:(str | num)` and `field2:(str | num)`
    - `rangePlus`: Signals true if `field1 >= field2` for the given `period` 
        - Required fields - `field1:(str | num)`, `field2:(str | num)` and `period:int`
    - `rangeMinus`: Signals true if `field1 <= field2` for the given `period` 
        - Required fields - `field1:(str | num):`, `field2:(str | num)` and `period:int`
    - `lastCrossOver`: Signals true if `field1` crossed `field2` in the given `period` 
        - Required fields - `field1:str`, `field2:str` and `period:int`
    - `rising`: Signals true if `field` is not decreasing for the given `period` 
        - Required fields - `field:str` and `period:int`
    - `falling`: Signals true if `field` is not increasing for the given `period` 
        - Required fields - `field:str` and `period:int`
    - `crossedFromAbove`: Signals true if `field1` crossed `field2` from above in the given `period`.
        - Required fields - `field1:(str | num)`, `field2:(str | num)` and `period:int`
    - `crossedFromBelow`: Signals true if `field1` crossed `field2` from below in the given `period`.
        - Required fields - `field1:(str | num)`, `field2:(str | num)` and `period:int`
    - `bullishDivergence`: Signals true if `field1` and `field2` had bullish divergence in the given `period`.
        - Required fields - `field1:str`, `field2:str` and `period:int`
    - `bearishDivergence`: Signals true if `field1` and `field2` had bearish divergence in the given `period`.
        - Required fields - `field1:str`, `field2:str` and `period:int`


## Contributing
- Please contact `rudrad200@gmail.com` before starting. 
- The main aim of this project is to create customizable and fast scripts to print and analyse various tickers.
- Other ideas are always welcome. 