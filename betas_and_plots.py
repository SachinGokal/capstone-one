import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as scs
import seaborn as sns
import datetime
import yfinance as yf
import pickle

class SectorBetasAndPlots:

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

    def __init__(self)
      self.stocks = pd.read_csv('data/stock-list.csv')
      self.sectors = np.unique(self.stocks['sector'])
      self.symbols = SECTOR_ETF_SYMBOLS.keys()
      self.industries = np.unique(self.stocks['industry'])
      self.date_today = datetime.date.today().isoformat()

    # General bar plot for seeing total number of securities that make up each sector
    def plot_for_stock_counts_by_sector():
      fig, ax = plt.subplots(figsize=(10, 7))
      stock_counts_by_sector = self.stocks.groupby(['sector']).count().reset_index()
      stock_counts_by_sector.rename(columns={'symbol': 'symbol_count'}, inplace=True)
      stock_counts_by_sector.plot(ax=ax, kind='bar', x='sector', y='symbol_count')
      plt.title("Total Stocks in each Sector", fontsize=18)
      plt.ylabel("Total", fontsize=14)
      plt.xlabel("Sector", fontsize=14)
      plt.xticks(fontsize=12)
      plt.savefig('total_stocks_per_sector.png')

    # Initial dataframe using data for S&P 500 Index ETF (SPY)
    def create_initial_spy_dataframe(start_date="2007-01-01", end_date=self.date_today):
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
    def calculate_betas(init_df, window=20, absvalue=True):
      pct_changes = init_df.pct_change()
      for sym in symbols:
        if absvalue == True:
          pct_changes[f'{sym.lower()}_beta'] = abs(pct_changes.rolling(window).cov().unstack()['spy_close'][f'{sym.lower()}_close'] / pct_changes['spy_close'].rolling(window).var())
        else:
          pct_changes[f'{sym.lower()}_beta'] = pct_changes.rolling(window).cov().unstack()['spy_close'][f'{sym.lower()}_close'] / pct_changes['spy_close'].rolling(window).var()
      return pct_changes

    def create_csv_for_data_frame(df, title):
      return df.to_csv(f'{title}')

    def plot_sector_betas_over_time(betas_df, title):
      fig, axs = plt.subplots(6, 2, sharey=True, figsize=(15, 35))
      fig.tight_layout()
      plt.subplots_adjust(hspace=.6)
      plt.xticks(fontsize=12)
      for sym, ax in zip(SECTOR_ETF_SYMBOLS.keys(), axs.flatten()):
        betas_df[f'{sym.lower()}_beta'].plot(
            ax=ax, title=SECTOR_ETF_SYMBOLS[sym])
        ax.axhline(y=1, color='r')
      plt.savefig(title)
      fig.delaxes(axs[-1, -1])

    def get_data_for_a_period(df, start_date, end_date):
      new_df = df.reset_index()
      new_df['Date'] = pd.to_datetime(new_df['Date'])
      mask = (new_df['Date'] > start_date) & (new_df['Date'] <= end_date)
      return new_df.loc[mask]

    # TODO: ADD MEAN FOR historical and recent data
    def t_test_for_symbol_betas(betas_df, historical_start):
      results = {}
      for sym in symbols:
        if sym == 'XLC' and historical_start < '2018-08-06':
          historical_start = '2018-08-06'
        col = f'{sym.lower()}_beta'
        historical = get_data_for_a_period(betas_df, historical_start, '2020-03-06')[col].values
        recent = get_data_for_a_period(betas_df, '2020-03-06', datetime.date.today().isoformat())[col].values
        results[sym] = scs.ttest_ind(historical, recent, equal_var=False)[1]
      return {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}

    def correlation_between_stocks_and_index(df, symbols):
      results = []
      for sym in symbols:
        col = f'{sym.lower()}_close'
        historical = get_data_for_a_period(df, '2018-08-06', '2020-03-06')
        historical_corr = historical['spy_close'].corr(historical[col])
        recent = get_data_for_a_period(df, '2020-02-21', datetime.date.today().isoformat())
        recent_corr = recent['spy_close'].corr(recent[col])
        results.append([sym, historical_corr, recent_corr])
      return results

    def plot_correlation_matrix(df):
      fig, ax = plt.subplots(figsize=(12, 12))
      df[IMPT_COLUMNS.keys()]
      corrMatrix = df.corr()
      sns.heatmap(corrMatrix, annot=True, ax=ax, vmin=-1, vmax=1,
                  xticklabels=IMPT_COLUMNS.values(), yticklabels=IMPT_COLUMNS.values())
      plt.show()
