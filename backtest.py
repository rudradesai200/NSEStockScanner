from datetime import datetime, timedelta

from Analysis.constants import symbols
from Analysis.DataLoader import DataLoader
from Analysis.TechnicalAnalysis import TechAnalysis, Signal, Verdict
from Strategies.MA_RSI_Long import config
from analysis import TickerAnalysis
import os

def backTest(ticker: str, config: dict, test_period: int, capital: int, target_profit: int, stop_loss: int):

    sign = lambda x : (x // abs(x))

    # Load Data
    dataloader = DataLoader(config['IndicatorConfig'])
    data = dataloader.getTickerData(ticker)
    inventory = 0
    last_price = 0
    pnl = 0
    signals = 0

    if data is None:
        print("Err2: Error in fetching data")
        return

    for en in range(test_period):
        test_data = data[test_period-en:]
        curr_price = test_data.iloc[0]['close']
        signal = TickerAnalysis(ticker, config, test_data, True)
        if inventory != 0:
            curr_pnl = (inventory * (curr_price - last_price))
            change = (((curr_price - last_price) * 100 * sign(inventory))/last_price)

        if inventory != 0:
            if (change <= stop_loss) and (signal.verdict != Verdict.BUY):
                print(f"Stop loss hit on {test_data.iloc[0].name}: Loss {curr_pnl}")
                pnl += curr_pnl
                inventory = 0
            elif (change >= target_profit) and (signal.verdict != Verdict.BUY):
                print(f"Target acheived on {test_data.iloc[0].name}: Profit {curr_pnl}")
                pnl += curr_pnl
                inventory = 0
        elif (signal.verdict == Verdict.BUY):
            if (inventory < 0) and (config["GeneralConfig"]["type"] == "short"):
                signals += 1
                print(f"Covered Short on {test_data.iloc[0].name}: PnL {curr_pnl}")
                pnl += curr_pnl
                inventory = 0
            if (inventory == 0) and (config["GeneralConfig"]["type"] == "long"):
                signals += 1
                print(f"Added Long on {test_data.iloc[0].name}")
                inventory = ((capital + pnl) // curr_price)
                last_price = curr_price
        elif (signal.verdict == Verdict.SELL):
            if (inventory > 0) and (config["GeneralConfig"]["type"] == "long"):
                signals += 1
                print(f"Covered Long on {test_data.iloc[0].name}: PnL {curr_pnl}")
                pnl += curr_pnl
                inventory = 0
            if (inventory == 0) and (config["GeneralConfig"]["type"] == "short"):
                signals += 1
                print(f"Added Short on {test_data.iloc[0].name}")
                inventory = - ((capital + pnl) // curr_price)
                last_price = curr_price

    if (inventory != 0):
        print(f"Remaining inventory: {inventory}")

    print("Final PnL: ", pnl)
    return {
        "PnL": pnl,
        "Signals": signals,
    }

if __name__ == "__main__":

    capital = 100000
    period = 720
    target_profit = 10
    stop_loss = -5


    # backTest("TITAN", config, period, capital, target_profit, stop_loss)

    # Run on all symbols
    fp = open("TestResults/"+config["GeneralConfig"]["name"]+".txt", "w")
    fp.write("="*10 + "Summary" + "="*10 + "\n")
    fp.write(f"Capital: {capital}\n")
    fp.write(f"Test Period: {period}\n")
    fp.write(f"Target Profit: {target_profit}\n")
    fp.write(f"Stop Loss: {stop_loss}\n\n\n")

    for symbol in ["RELIANCE", "TATAMOTORS", "TATASTEEL", "HINDUNILVR", "COALINDIA", "IRCTC", "BHEL", "TITAN", "IEX", "AXISBANK"]:
        print("="*10, symbol)
        summary = backTest(symbol, config, period, capital, target_profit, stop_loss)
        print("="*10)

        fp.write("="*10 + symbol + "="*10 + "\n")
        fp.write(f"Pnl: {summary['PnL']}\nSignals: {summary['Signals']}\n\n")

    fp.close()