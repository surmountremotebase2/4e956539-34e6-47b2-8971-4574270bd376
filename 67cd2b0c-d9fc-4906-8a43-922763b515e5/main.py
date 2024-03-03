from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log
from pandas_market_calendars import get_calendar
import pandas as pd

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["XLP", "XLY", "XLE", "XLK", "XLV", "XLI", "XLC", "XLF", "XLU", "XLB"]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def get_market_open_dates(self, start_date, end_date, exchange_name='NYSE'):
        calendar = get_calendar(exchange_name)
        schedule = calendar.schedule(start_date=start_date, end_date=end_date)

        return schedule.index.tolist()

    def last_trading_days_of_months(self, start_date, end_date, exchange_name='NYSE'):
        calendar = get_calendar(exchange_name)
        dates_range = pd.date_range(start=start_date, end=end_date, freq='D')

        last_trading_days = []
        for year_month in set((d.year, d.month) for d in dates_range):
            month_end = calendar.month_end(pd.Timestamp(year_month[0], year_month[1], 1))
            last_trading_day = calendar.previous_open(month_end).date()
            last_trading_days.append(last_trading_day)

        return last_trading_days

    def run(self, data):
        d = data["ohlcv"]

        start_date = '2024-01-01'
        end_date = '2024-12-31'
        exchange_name = 'NYSE'

        market_open_dates = self.get_market_open_dates(start_date, end_date, exchange_name)

        log('market_open_dates')
        log(str(market_open_dates))

        last_trading_days = self.last_trading_days_of_months(start_date, end_date, exchange_name)

        log('last trading dates')
        log(str(last_trading_days))
        
        log(str(d[-1]))
        allocation_dict = {i: 0 for i in self.tickers}
        if len(d) % 2 == 1:  
            log('buy') 
            allocation_dict = {"GOOGL": 0.1}
        else:
            log('sell')
            allocation_dict = {"GOOGL": 0.2}
        return TargetAllocation(allocation_dict)