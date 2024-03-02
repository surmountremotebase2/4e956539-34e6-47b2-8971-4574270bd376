from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY", "QQQ", "AAPL", "GOOGL"]

    @property
    def assets(self):
        return self.tickers
        
    @property
    def interval(self):
        return "1day"

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        log(str(allocation_dict))
        log(str(d))
        log(str(len(d)))

        if len(d) % 2 == 0:
            allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        else:
            allocation_dict = {i: -(1/len(self.tickers)*3) for i in self.tickers}

        log(str(allocation_dict))
        return TargetAllocation(allocation_dict)