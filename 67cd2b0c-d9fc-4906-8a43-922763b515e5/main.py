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
    
    # Generate all the dates between start_date and end_date
        dates_range = pd.date_range(start=start_date, end=end_date, freq='B')  # 'B' frequency considers only business days
    
    # Iterate over each month and find the last trading day
        last_trading_days = []
        previous_month = None
        for date in dates_range:
            if previous_month != (date.year, date.month):
            # If it's a new month, add the last trading day of the previous month
                if previous_month is not None:
                    last_trading_days.append(last_trading_day)
            # Reset the last trading day for the new month
                last_trading_day = None
                previous_month = (date.year, date.month)
        
            if calendar.is_session(date):
                last_trading_day = date
    
    # Add the last trading day of the last month
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


