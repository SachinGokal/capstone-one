import numpy as np
import pandas as pd
import scipy.stats as scs
import datetime
import yfinance as yf

class BetasAndCorrelation:

    SECTOR_ETF_SYMBOLS = {
        'XLB': 'Materials',
        'XLC': 'Communication Services',
        'XLE': 'Energy',
        'XLF': 'Financials',
        'XLI': 'Industrials',
        'XLK': 'Information Technology',
        'XLP': 'Consumer Staples',
        'XLRE': 'Real Estate',
        'XLU': 'Utilities',
        'XLV': 'Health Care',
        'XLY': 'Consumer Discretionary'
    }

    IMPT_COLUMNS = {'spy_close': 'S&P',
                    'xlb_close': 'Materials',
                    'xlc_close': 'Communication Services',
                    'xle_close': 'Energy',
                    'xlf_close': 'Financials',
                    'xli_close': 'Industrials',
                    'xlk_close': 'Information Technology',
                    'xlp_close': 'Consumer Staples',
                    'xlre_close': 'Real Estate',
                    'xlu_close':  'Utilities',
                    'xlv_close': 'Health Care',
                    'xly_close': 'Consumer Discretionary'}

    HISTORICAL_STARTS = ['2020-02-06', '2019-12-06', '2019-03-06', '2015-03-06']

    def __init__(self)
      self.stocks = pd.read_csv('data/stock-list.csv')
      self.sectors = np.unique(self.stocks['sector'])
      self.symbols = SECTOR_ETF_SYMBOLS.keys()
      self.industries = np.unique(self.stocks['industry'])
      self.date_today = datetime.date.today().isoformat()

    # Initial dataframe using data for S&P 500 Index ETF (SPY)
    def create_initial_spy_dataframe(start_date="2007-01-01", end_date=datetime.date.today().isoformat()):
      spy_data = yf.download("SPY", start=start_date, end=end_date)
      spy_data = spy_data[['Adj Close']]
      spy_data.rename(columns={'Adj Close': 'spy_close'}, inplace=True)
      return spy_data

    def add_symbol_data_to_dataframe(init_df, start_date="2007-01-01", end_date=datetime.date.today().isoformat()):
      for sym in symbols:
          data = yf.download(sym, start=start_date, end=end_date)
          init_df[f'{sym.lower()}_close'] = data['Adj Close']
      return init_df

    # create a plot for recent and two year range
    def calculate_betas(init_df, window=20, absvalue=False):
      pct_changes = init_df.pct_change()
      for sym in symbols:
        if absvalue == True:
          pct_changes[f'{sym.lower()}_beta'] = abs(pct_changes.rolling(window).cov().unstack()['spy_close'][f'{sym.lower()}_close'] / pct_changes['spy_close'].rolling(window).var())
        else:
          pct_changes[f'{sym.lower()}_beta'] = pct_changes.rolling(window).cov().unstack()['spy_close'][f'{sym.lower()}_close'] / pct_changes['spy_close'].rolling(window).var()
      return pct_changes

    def t_test_for_symbol_betas(betas_df, historical_start):
      data = {'symbol': [], 'sector': [], 't_stat': [], 'p_value': [], 'significant?': [
      ], 'recent_average_beta': [], 'historical_average_beta': [], 'difference': []}
      for sym in symbols:
        if sym == 'XLC' and historical_start < '2018-08-06':
          historical_start = '2018-08-06'
        col = f'{sym.lower()}_beta'
        historical = get_data_for_a_period(
            betas_df, historical_start, '2020-03-06')[col].values
        recent = get_data_for_a_period(
            betas_df, '2020-03-06', '2020-04-08')[col].values
        t_stat = scs.ttest_ind(recent, historical, equal_var=False)[0]
        p_value = scs.ttest_ind(recent, historical, equal_var=False)[1]
        data['symbol'].append(sym)
        data['sector'].append(SECTOR_ETF_SYMBOLS[sym])
        data['t_stat'].append(t_stat)
        data['p_value'].append(p_value)
        data['significant?'].append(p_value < .025)
        data['recent_average_beta'].append(recent.mean())
        data['historical_average_beta'].append(historical.mean())
        data['difference'].append(recent.mean() - historical.mean())
      return pd.DataFrame(data

    def correlation_between_stocks_and_index(df):
      data = {'symbol': [], 'sector': [], 'recent_corr': [], 'one_month_corr': [], 'three_month_corr': [], 'one_year_corr': [], 'five_year_corr': []}
      for sym in symbols:
        data['symbol'].append(sym)
        data['sector'].append(SECTOR_ETF_SYMBOLS[sym])
        col = f'{sym.lower()}_close'

        recent = get_data_for_a_period(df, '2020-02-21', '2020-04-08')
        one_month = get_data_for_a_period(df, '2020-01-21', '2020-02-21')
        three_month = get_data_for_a_period(df, '2019-10-21', '2020-01-21')
        one_year = get_data_for_a_period(df, '2019-02-21', '2020-02-21')
        five_year = get_data_for_a_period(df, '2015-02-21', '2020-02-21')

        data['recent_corr'].append(recent['spy_close'].corr(recent[col]))
        data['one_month_corr'].append(one_month['spy_close'].corr(one_month[col]))
        data['three_month_corr'].append(three_month['spy_close'].corr(three_month[col]))
        data['one_year_corr'].append(one_year['spy_close'].corr(one_year[col]))
        data['five_year_corr'].append(five_year['spy_close'].corr(five_year[col]))

      return pd.DataFrame(data)

    def create_csv_for_data_frame(df, title):
      return df.to_csv(f'{title}')

    def get_data_for_a_period(df, start_date, end_date):
      new_df=df.reset_index()
      new_df['Date']=pd.to_datetime(new_df['Date'])
      mask=(new_df['Date'] > start_date) & (new_df['Date'] <= end_date)
      return new_df.loc[mask]

