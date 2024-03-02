from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["GOOGL"]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        d = data["ohlcv"]
        
        log(str(d))
        allocation_dict = {i: 0 for i in self.tickers}
        if len(d) % 12 == 0:  
            log('buy 1') 
            allocation_dict = {i: 1 for i in self.tickers}
        else:
            log('sell')
            allocation_dict = {i: -1 for i in self.tickers}
        return TargetAllocation(allocation_dict)