import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as scs
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

    def __init__(self)
      self.stocks = pd.read_csv('data/stock-list.csv')
      self.sectors = np.unique(self.stocks['sector'])
      self.industries = np.unique(self.stocks['industry'])
      self.symbols = np.unique(self.stocks['symbol'])
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

    # Initial dataframe using data for S&P 500 Index ETF
    def create_initial_spy_dataframe(start_date="2019-01-01", end_date=self.date_today):
      spy_data = yf.download("SPY", start=start_date, end=end_date)
      spy_data = spy_data[['Adj Close']]
      spy_data.rename(columns={'Adj Close': 'spy_close'}, inplace=True)
      return spy_data

    def add_symbol_data_to_dataframe(init_df, symbols, start_date="2019-01-01", end_date=datetime.date.today().isoformat()):
      for sym in symbols:
          data = yf.download(sym, start=start_date, end=end_date)
          init_df[f'{sym.lower()}_close'] = data['Adj Close']
      return init_df

    def calculate_beta_for_specific_time_range(init_df, symbols, window=30):
      pct_changes = init_df.pct_change()
      for sym in symbols:
        pct_changes[f'{sym.lower()}_beta'] = pct_changes.rolling(window).cov().unstack()['spy_close'][f'{sym.lower()}_close'] / pct_changes['spy_close'].rolling(window).var()
      return pct_changes

    def create_csv_for_data_frame(df, title):
      return df.to_csv(f'{title}')

    def plot_sector_betas_over_time(betas_df):
      fig, axs = plt.subplots(6, 2, figsize=(15, 35))
      fig.tight_layout()
      plt.subplots_adjust(hspace=.6)
      plt.xticks(fontsize=12)
      for sym, ax in zip(SECTOR_ETF_SYMBOLS.keys(), axs.flatten()):
        betas[f'{sym.lower()}_beta'].plot(ax=ax, title=SECTOR_ETF_SYMBOLS[sym])
      plt.savefig('beta_for_each_sector_since_2019.png')

#add_symbol_data_to_dataframe(spy_data, SECTOR_ETF_SYMBOLS.keys())
#calculate_beta_for_specific_time_range(spy_data, SECTOR_ETF_SYMBOLS.keys())
