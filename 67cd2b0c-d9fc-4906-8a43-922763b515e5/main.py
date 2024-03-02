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
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        log(str(data))
        if len(str(self.data)) % 2 == 0:
            log('hiii')
            allocation_dict = {i: 1 for i in self.tickers}
        else:
            log('byeee')
            allocation_dict = {i: 0 for i in self.tickers}

        return TargetAllocation(allocation_dict)