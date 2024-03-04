from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log
from pandas_market_calendars import get_calendar
import pandas as pd

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["GOOGL"]
        self.prev_allocation_dict = {i: 0 for i in self.tickers}

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers



    def run(self, data):
        curr_allocation_dict = {i: 0 for i in self.tickers}
        d = data["ohlcv"]

        log(str(data["holdings"]))
        log(str(d))

        i = 0
        if i == 0:
            return TargetAllocation({"GOOGL": 1})
            i = 1
        else:
            return TargetAllocation({"GOOGL": 0})
            # return TargetAllocation({"GOOGL": 1})



        
        