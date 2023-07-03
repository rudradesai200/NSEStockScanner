from datetime import datetime, timedelta

from CodeBase1.constants import symbols
from CodeBase1.DataLoader import DataLoader
from CodeBase1.TechnicalAnalysis import TechAnalysis, Signal, Verdict
from Strategies.Basic_1 import config
from tqdm import tqdm


def TickerAnalysis(ticker: str, config: dict, data = None, debug:bool = False) -> Signal:
    if data is None:
        # Load Data
        dataloader = DataLoader(config['IndicatorConfig'])
        data = dataloader.getTickerData(ticker,  config["GeneralConfig"]["interval"], config["GeneralConfig"]["period"])
        
        if data is None:
            print("Err2: Error in fetching data")
            return 
    
    # Run Analysis
    tech = TechAnalysis(ticker, data)
    buy_signal = tech.ConfirmVerdict(config['EntryConfig'], debug)
    tech = TechAnalysis(ticker, data)
    sell_signal = tech.ConfirmVerdict(config['ExitConfig'], debug)
    # Finalise signal
    return Signal.combine(buy_signal, sell_signal, config['GeneralConfig']['buy_threshold'], config['GeneralConfig']['sell_threshold'])




if __name__ == "__main__":
    TickerAnalysis("RELIANCE.NS", config).print()

    # for symbol in ["RELIANCE", "TATAMOTORS", "TATASTEEL", "HINDUNILVR", "COALINDIA", "IRCTC", "BHEL", "TITAN", "IEX", "AXISBANK"]:
        # TickerAnalysis(symbol, config).print()