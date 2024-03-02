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
        
        if len(d) % 2 == 0:   
            allocation_dict_1 = {i: 1 for i in self.tickers}
        else:
            allocation_dict_2 = {i: 0 for i in self.tickers}

        return TargetAllocation({**allocation_dict_1, **allocation_dict_2})