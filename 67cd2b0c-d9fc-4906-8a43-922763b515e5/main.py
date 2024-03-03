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

    def get_market_open_dates(start_date, end_date, exchange_name='NYSE'):

        calendar = get_calendar(exchange_name)
    
        # Generate the market open dates
        schedule = calendar.schedule(start_date=start_date, end_date=end_date)
    
        return schedule.index.tolist()

    def run(self, data):
        d = data["ohlcv"]

        start_date = '2024-01-01'
        end_date = '2024-12-31'
        exchange_name = 'NYSE'

        market_open_dates = get_market_open_dates(start_date, end_date, exchange_name)

        log(market_open_dates)
        log(str(d[-1]))
        allocation_dict = {i: 0 for i in self.tickers}
        if len(d) % 2 == 1:  
            log('buy') 
            allocation_dict = {"GOOGL": 0.1}
        else:
            log('sell')
            allocation_dict = {"GOOGL": 0.2}
        return TargetAllocation(allocation_dict)


