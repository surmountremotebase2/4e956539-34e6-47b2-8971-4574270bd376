from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log
from pandas_market_calendars import get_calendar
import pandas as pd
import numpy as np


class TradingStrategy(Strategy):

    def __init__(self):
        self.last_trading_days = None
        self.market_open_dates = None
        self.date_fetched = False
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

    def get_alloc_dates_for_nth_trading_day(self, timestamps, n):
        _alloc_dates  = []
        prev_month = pd.to_datetime(timestamps[0]).month
        curr_month = None
        eothm = None
        day_counter = -32
        for dt in timestamps:
            day_counter = day_counter+1
            ts = pd.to_datetime(dt)
            curr_month = ts.month
            if (n != 21) and day_counter == n:
                _alloc_dates.append(ts)
            if curr_month == prev_month:
                eothm = ts 
                continue
            else:
                prev_month = curr_month
                day_counter = 1
                if n == 21:
                    _alloc_dates.append(eothm)
                if n == 1:
                    _alloc_dates.append(ts)
            
    
        _alloc_dates = pd.DatetimeIndex(_alloc_dates)
        return _alloc_dates

    def calculate_return(self, price_mx, days=21):
        tkrs = price_mx.columns
        res = pd.DataFrame(data=None, index=price_mx.index, columns=price_mx.columns)
        for tkr in tkrs:
            ts = price_mx.loc[~price_mx[tkr].isna(), tkr]
            res[tkr] = ts.pct_change(periods=days)
        res = res.ffill(axis=0)
        return res

    def check_realloc_date(self, realloc_dates, timestamp):
        if timestamp in realloc_dates:
            return True
        else:
            return False

    def get_data(self, data):
        tickers = list(data[0].keys())

        # log(str(tickers))

        dates = [list(entry.values())[0]['date'] for entry in data]

        # log(str(dates))

        ticker_values = {ticker: [entry[ticker]['close'] for entry in data] for ticker in tickers}

        df = pd.DataFrame(ticker_values, index=pd.to_datetime(dates))

        return df, dates

    def get_market_dates(self, start_date, end_date, exchange_name):
        
        self.market_open_dates = self.get_market_open_dates(start_date, end_date, exchange_name)

        self.last_trading_days = self.get_alloc_dates_for_nth_trading_day(self.market_open_dates, 21)
        
    def AAA_covariance(self, price_df, timestamp, symbols, method=None):
        ncor = 126  # days back for correlation calc
        nvol = 20   # days back for volatility calc
        ix = price_df.index.get_loc(timestamp)
        if ix < ncor + 1:
            return None
        else:
            df = price_df[symbols].iloc[ix-ncor-1:ix]  # 6 months PRICE history for symbols of interest
            ret = df.pct_change().iloc[1:]  # 6 months RETURNS history
            if method is None:
                corr = ret.corr()
                vol = ret.iloc[-nvol:].std()
                cov = corr * np.outer(vol, vol)
            else:  # pass mode argument to pypfopt
                cov = pypfopt.risk_models.risk_matrix(df, method=method)
            return cov

    def calculate_weights(self, cov_mx):
        num_assets = cov_mx.shape[0]
        ones = np.ones(num_assets)
        cov_inv = np.linalg.inv(cov_mx)
        
        denominator = ones.dot(cov_inv).dot(ones)
        numerator = cov_inv.dot(ones)
        
        weights = numerator / denominator
    
        return weights
    def round_weights(self, weights, thresh=0.02):
        weights = weights.copy() / weights.sum()  # make sure it sums to 1.0
        ix = weights < thresh
        adj = sum(weights[ix]) * weights[~ix] / weights[~ix].sum()
        out = pd.Series(index=weights.index, data=0.0)
        out[~ix] = weights[~ix] + adj
        return out

    def run(self, data):
        curr_allocation_dict = {i: 0 for i in self.tickers}

        d = data["ohlcv"]
    
        # log(str(data["holdings"]))

        if len(d) != 0:
            start_date = '2015-02-05'
            end_date = '2024-12-31'
            exchange_name = 'NYSE'

            if not self.date_fetched:
                self.get_market_dates(start_date, end_date, exchange_name)
                self.date_fetched = True

            data_df, dates = self.get_data(d)

            returns = self.calculate_return(data_df, days=126)

            returns = returns.drop(columns=['SPY'])

            timestamp = dates[-1]
    
            is_realloc_date = self.check_realloc_date(self.last_trading_days, timestamp)


            if is_realloc_date:
                curr_ret = returns.loc[timestamp]


                if sum(pd.notna(curr_ret)) >= 1:

                    top_n = curr_ret.nlargest(1)


                    total_keys = len(top_n)

                    cov_mx = self.AAA_covariance(data_df, timestamp, symbols=top_n.index.values,
                                        method=None)


                    wts = self.calculate_weights(cov_mx)


                    weights = self.round_weights(pd.Series(index=top_n.index.values.tolist(), data=wts))
                    
                    # log(str(weights))
                    for key in curr_allocation_dict:
                        if key in weights.index:
                            curr_allocation_dict[key] = float(weights[key])

                    # log(str(curr_allocation_dict))

                    return TargetAllocation(curr_allocation_dict)