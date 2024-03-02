from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
    self.tickers = ["AAPL", "GOOGL"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        d = data["ohlcv"]
        qqq_stake = 0
        log(str(d))

        return TargetAllocation({"AAPL": 1, "GOOGL": 1})