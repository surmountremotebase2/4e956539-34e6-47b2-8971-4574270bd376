from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["QQQ", "SQQQ"]

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        holdings = data["holdings"]
        data = data["ohlcv"]

        sqqq_stake = 0
        qqq_stake = 0

        qqq_bbands = BB("QQQ", data, 20, 1.4)
        qqq_ma = SMA("QQQ", data, 5)

        if len(data)<20:
            return TargetAllocation({})

        current_price = data[-1]["QQQ"]['close']

        if qqq_bbands is not None and current_price < qqq_bbands['lower'][-1] and qqq_ma[-1]>qqq_ma[-2]:
            log("going long")
            if holdings["QQQ"] >= 0:
                qqq_stake = min(1, holdings["QQQ"]+0.1)
            else:
                qqq_stake = 0.4
        elif qqq_bbands is not None and current_price > qqq_bbands['upper'][-1]:
            log("going short")
            if holdings["SQQQ"] >= 0:
                sqqq_stake = min(1, holdings["SQQQ"]+0.075)
            else:
                sqqq_stake = 0.2
        else:
            log("meh")
            qqq_stake = 0
            sqqq_stake = 0

        return TargetAllocation({"SQQQ": sqqq_stake, "QQQ": qqq_stake})