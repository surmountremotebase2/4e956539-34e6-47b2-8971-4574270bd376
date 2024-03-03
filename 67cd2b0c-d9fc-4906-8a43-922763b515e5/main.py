from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["XLP", "XLY", "XLE", "XLK", "XLV", "XLI", "XLC", "XLF", "XLU", "XLB"]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        d = data["ohlcv"]
        
        log(str(d[-1]))
        allocation_dict = {i: 0 for i in self.tickers}
        if len(d) % 2 == 1:  
            log('buy') 
            allocation_dict = {"GOOGL": 0.1}
        else:
            log('sell')
            allocation_dict = {"GOOGL": 0.2}
        return TargetAllocation(allocation_dict)