from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["AAPL", "GOOGL"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        d = data["ohlcv"]
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        log(str(allocation_dict))
        log(str(d))

        return TargetAllocation({"AAPL": 1, "GOOGL": 1})