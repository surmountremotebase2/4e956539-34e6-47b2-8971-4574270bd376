from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log
from pandas_market_calendars import get_calendar
import pandas as pd

class TradingStrategy(Strategy):

    def __init__(self):
        self.i = 0
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

        
        if self.i == 0:
            self.i = 1
            log('if')
           
            return TargetAllocation({"GOOGL": 1})       
        else:
            log('else')
            
            return TargetAllocation({"GOOGL": data["holdings"]["GOOGL"]})
            # return TargetAllocation({"GOOGL": 1})



        
        