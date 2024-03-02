from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["GOOGL"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        if len(self.tickers) % 2 == 0:
            allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        else:
            allocation_dict = {i: 0 for i in self.tickers}

        return TargetAllocation(allocation_dict)