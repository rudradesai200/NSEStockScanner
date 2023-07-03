from __future__ import annotations
import numpy as np
from copy import copy
import pandas as pd
from typing import List
import enum

class Verdict(enum.Enum):
    BUY = "buy"
    SELL = "sell"
    NEUTRAL = "neutral"
    CONFIRMED = "confirmed"
    UNDEFINED = "undefined"

colors = {
    3: '\033[92m [++] ',  # GREEN
    2: '\033[96m [+] ',  # light blue
    1: '\033[93m [o] ',  # YELLOW
    0: ' [i] ',  # Info
    -1: '\033[93m [o] ',  # YELLOW
    -2: '\033[95m [-] ',  # Magenta
    -3: '\033[91m [--] ',  # RED
    'RESET': '\033[0m',  # RESET COLOR
}

class Signal:
    def __init__(self, ticker: str, messages: List[str], strength: int, verdict: Verdict = Verdict.UNDEFINED):
        self.ticker = ticker
        self.messages = messages
        self.strength = strength
        self.verdict = verdict


    def print(self):
        color = colors[0]
        if(self.verdict == Verdict.BUY):
            color = colors[3]
        elif(self.verdict == Verdict.SELL):
            color = colors[-3]
        else:
            color = colors[0]

        print('='*10)
        print("Ticker: "+ self.ticker)
        print("Strength: "+str(self.strength))  
        print("Signal: "+color+str(self.verdict)+colors["RESET"])
        print("Messages: ")
        print("\n".join(self.messages))

    @classmethod
    def combine(cls, buy_signal:Signal, sell_signal:Signal, buy_threshold:int, sell_threshold:int) -> Signal:
        comb_signal = Signal(buy_signal.ticker, buy_signal.messages + sell_signal.messages, 0)

        if (buy_signal.verdict == Verdict.CONFIRMED) and ((sell_signal.verdict == Verdict.CONFIRMED)):
            comb_signal.strength = buy_signal.strength - sell_signal.strength
            if (comb_signal.strength > 0) and (buy_signal.strength >= buy_threshold):
                comb_signal.verdict = Verdict.BUY
            elif (comb_signal.strength < 0) and (sell_signal.strength >= sell_threshold):
                comb_signal.verdict = Verdict.SELL
            else:
                comb_signal.verdict = Verdict.NEUTRAL
        elif (buy_signal.strength >= buy_threshold) and (buy_signal.verdict == Verdict.CONFIRMED):
            comb_signal.verdict = Verdict.BUY
            comb_signal.strength = buy_signal.strength
        elif (sell_signal.strength >= sell_threshold) and (sell_signal.verdict == Verdict.CONFIRMED):
            comb_signal.verdict = Verdict.SELL
            comb_signal.strength = sell_signal.strength
        else:
            comb_signal.verdict = Verdict.NEUTRAL
            comb_signal.strength = buy_signal.strength - sell_signal.strength

        return comb_signal
    
class TechAnalysis:

    def __init__(self, ticker: str, data: pd.DataFrame):
        if (ticker is None):
            print("No ticker provided")
        
        if (data is None):
            print("No data provided")
        
        self.ticker = ticker
        self.data = data
        self.strength = 0
        self.messages = []
        self.function_map = {
            "rangePlus": self.__rangeplus,
            "rangeMinus": self.__rangeminus,
            "lastCrossOver": self.__lastCrossOver,
            "rising": self.__rising,
            "falling": self.__falling,
            "comparePlus": self.__comparePlus,
            "compareMinus": self.__compareMinus,
            "hasMaxima": self.__hasMaxima,
            "hasMinima": self.__hasMinima,
            "crossedFromAbove": self.__crossedFromAbove,
            "crossedFromBelow": self.__crossedFromBelow,
            "bullishDivergence": self.__bullishDivergence,
            "bearishDivergence": self.__bearishDivergence,
        }

    def __addMsg(self, msg, color, score):
        """
        `color` is used to print colors while printing on terminal\n
        `score` is used to add to the severity level
        """
        self.strength += score
        # if (score >= self.buy_threshold) or (score <= self.sell_threhold):
        self.messages.append("\t"+colors[color] + msg + colors["RESET"])

    def __comparePlus(self, field1, field2, color=0, score=3) -> bool:
        """
        Checks if the latest `field1` value is greater than latest `field2` or `field2` value\n
        Ex: `EMA13` > `EMA52`
        """
        val1 = self.data[field1][0] if isinstance(field1, str) else field1
        val2 = self.data[field2][0] if isinstance(field2, str) else field2
        ans = (val1 > val2)
        if(ans):
            self.__addMsg(str(field1) + " above " + str(field2), color, score)
        return ans

    def __compareMinus(self, field1, field2, color=0, score=3) -> bool:
        """
        Checks if the latest `field1` value is lesser than latest `field2` or `field2` value\n
        Ex: `EMA13` < `EMA52`
        """
        val1 = self.data[field1][0] if isinstance(field1, str) else field1
        val2 = self.data[field2][0] if isinstance(field2, str) else field2
        ans = (val1 < val2)
        if(ans):
            self.__addMsg(str(field1) + " below "+str(field2), color, score)
        return ans

    def __lastCrossOver(self, field1, field2, period, color=0, score=0, offset=0) -> bool:
        """
        Checks if `field1` crossed `field2` in the last [offset, offset+period] periods. And prints the elapsed crossover time\n
        Ex: Did `EMA13` cross `EMA52` in the last 5 periods?
        """
        for i in range(offset, period+offset+1):
            if ((self.data[field1][i] > self.data[field2][i]) and (
                self.data[field1][i-1] < self.data[field2][i-1])):
                self.__addMsg(field1 + " crossed " + field2 +
                              " before " + str(i) + " periods", color, score)
                return True
        return False

    def __rangeplus(self, field1, field2, period, color=2, score=0) -> bool:
        """
        Checks if `field1` >= `field2` in the last `period` periods\n
        Ex: Did `EMA13` stayed above `EMA52` in the last 5 periods?
        """
        val1 = self.data[field1][:period] if isinstance(field1, str) else field1
        val2 = self.data[field2][:period] if isinstance(field2, str) else field2
        ans = (np.sum(val1 >= val2) == period)
        if(ans):
            self.__addMsg(str(field1) + " stayed above "+str(field2) +
                " in the last "+str(period)+" periods", color, score)
        return ans

    def __rangeminus(self, field1, field2, period, color=2, score=0) -> bool:
        """
        Checks if `field1` <= `field2` in the last `period` periods\n
        Ex: Did `EMA13` stayed above `EMA52` in the last 5 periods?
        """
        val1 = self.data[field1][:period] if isinstance(field1, str) else field1
        val2 = self.data[field2][:period] if isinstance(field2, str) else field2
        ans = (np.sum(val1 <= val2) == period)
        if(ans):
            self.__addMsg(str(field1) + " stayed below "+ str(field2) +
                " in the last "+str(period)+" periods", color, score)
        return ans

    def __checkInc(self, x: pd.Series) -> bool:
        for i in range(len(x)-1):
            if not (x[i] <= x[i+1]):
                return False
        return True

    def __checkDec(self, x: pd.Series) -> bool:
        for i in range(len(x)-1):
            if not (x[i] >= x[i+1]):
                return False
        return True

    def __rising(self, field, period, color=1, score=0):
        """
        Checks if `field` was rising in the last `period` periods.\n
        Ex: `EMA13` was rising in the last 5 periods
        """
        ans = self.__checkInc(self.data[field][:period])
        if(ans):
            self.__addMsg(field + " rising from the last " +
                str(period)+" periods", color, score)
        return ans

    def __falling(self, field, period, color=1, score=0):
        """
        Checks if `field` was falling in the last `period` periods.\n
        Ex: `EMA13` was falling in the last 5 periods
        """
        ans = self.__checkDec(self.data[field][:period])
        if(ans):
            self.__addMsg(field + " falling from the last " +
                str(period)+" periods", color, score)
        return ans

    def __hasMaxima(self, field, period, color=1, score=0):
        """
        Checks if `field` had its maxima in the last `period` periods\n
        Ex: `macd_histogram` has its maxima today
        """
        peak = np.argmax(self.data[field][:period])
        if peak == (period - 1):
            return False
        if peak == 0:
            return False
        if self.__checkInc(self.data[field][:peak]) and self.__checkDec(self.data[field][peak:peak+period]):
            self.__addMsg(field + " was at a maxima " +
                          str(peak+1) + " periods ago", color, score)
            return True
        else:
            return False

    def __hasMinima(self, field, period, color=1, score=0):
        """
        Checks if `field` had its minima in the last `period` periods\n
        Ex: `macd_histogram` has its minima today
        """
        peak = np.argmin(self.data[field][:period])
        if peak == (period - 1):
            return False
        if peak == 0:
            return False
        if self.__checkDec(self.data[field][:peak]) and self.__checkInc(self.data[field][peak:peak+period]):
            self.__addMsg(field + " was at a minima " +
                          str(peak+1) + " periods ago", color, score)
            return True
        else:
            return False

    def __crossedFromBelow(self, field1, field2, period, color=1, score=0):
        """
        Checkf is field1 crossed field2 from below in the given period
        Ex: `EMA13` crossed `EMA52` from below 3 days before
        """
        val1 = self.data[field1][:period] if isinstance(field1, str) else field1
        val2 = self.data[field2][:period] if isinstance(field2, str) else field2
        diff = val1 - val2
        if (diff[0] > 0) and (diff[-1] < 0) and (self.__checkDec(diff)):
            self.__addMsg(str(field1) + " crossed " +
                          str(field2) + " from below in " + str(period) + " periods", color, score)
            return True
        else:
            return False
    
    def __crossedFromAbove(self, field1, field2, period, color=1, score=0):
        """
        Checkf is field1 crossed field2 from above in the given period
        Ex: `EMA13` crossed `EMA52` from above 3 days before
        """
        val1 = self.data[field1][:period] if isinstance(field1, str) else field1
        val2 = self.data[field2][:period] if isinstance(field2, str) else field2
        diff = val1 - val2
        if (diff[0] < 0) and (diff[-1] > 0) and (self.__checkInc(diff)):
            self.__addMsg(str(field1) + " crossed " +
                          str(field2) + " from above in " + str(period) + " periods", color, score)
            return True
        else:
            return False
    
    def __bullishDivergence(self, field1, field2, period, color=1, score=0):
        """
        Checks if field1 gave lower peaks and field2 increased in the give period
        Ex: `close` and `RSI14` had a bullish divergence
        """
        peaks = []
        for i in range(1, period-1):
            if (self.data[field1][i] > self.data[field1][i-1]) and (self.data[field1][i] < self.data[field1][i+1]):
                peaks.append(i)
        
        for i in range(1, len(peaks)):
            if (self.data[field1][peaks[i]] < self.data[field1][peaks[i-1]]) and (self.data[field2][peaks[i]] > self.data[field2][peaks[i-1]]):
                self.__addMsg(f"Bullish divergence between {field1} and {field2} in ({self.data.iloc[peaks[i]].name} - {self.data.iloc[peaks[i-1]].name}) interval", color, score)
                return True
        
        return False
    
    def __bearishDivergence(self, field1, field2, period, color=1, score=0):
        """
        Checks if field1 gave higher peaks and field2 decreased in the give period
        Ex: `close` and `RSI14` had a bearish divergence
        """
        peaks = []
        for i in range(1, period-1):
            if (self.data[field1][i] > self.data[field1][i-1]) and (self.data[field1][i] < self.data[field1][i+1]):
                peaks.append(i)
        
        for i in range(1, len(peaks)):
            if (self.data[field1][peaks[i]] > self.data[field1][peaks[i-1]]) and (self.data[field2][peaks[i]] < self.data[field2][peaks[i-1]]):
                self.__addMsg(f"Bearish divergence between {field1} and {field2} in ({self.data.iloc[peaks[i]].name} - {self.data.iloc[peaks[i-1]].name}) interval", color, score)
                return True
        
        return False

    def __resolve(self, origconfig):
        config = copy(origconfig)
        if isinstance(config, dict):
            funcname = config.pop("type")
            if "negate" in config.keys():
                config.pop("negate")
                return not self.function_map[funcname](**config)
            else:
                return self.function_map[funcname](**config)
        elif isinstance(config, list):
            for conf in config:
                if not self.__resolve(conf):
                    return False
            return True
        else:
            print("Incorrect resolve passed - "+config)
            return False
    
    def ConfirmVerdict(self, config: dict, debug: bool = False) -> Signal:
        """
        Checks for verdict signals based on the configuration provided.\n
        Expects 3 fields : conditions, indicators, confirmations\n
        If all conditions are not met, indicators and confirmations won't be checked \n
        If all conditions are met and atleast one indicator is present, it will confirm the verdict\n
        Confirmations are added to the messages only if the ticker is confirmed\n
        """
        
        if 'indicators' not in config or not isinstance(config['indicators'], list):
            print("indicators field of list type in required in the config")
        if 'confirmations' not in config or not isinstance(config['confirmations'], list):
            print("confirmations field of list type in required in the config")
        
        self.strength = 0
        self.messages = []

        sig = Signal(self.ticker, [], 0, Verdict.UNDEFINED)

        verdict = False
        for indi in config['indicators']:
            verdict |= self.__resolve(indi)
        
        if verdict or debug:
            sig.verdict = Verdict.CONFIRMED
            for conf in config["confirmations"]:
                _ = self.__resolve(conf)

        sig.strength = self.strength
        sig.messages = self.messages
        
        return sig