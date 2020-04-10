import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

class Plots:

    def __init__(self):

    def plot_for_stock_counts_by_sector():
      fig, ax = plt.subplots(figsize=(10, 7))

      stock_counts_by_sector = self.stocks.groupby(
          ['sector']).count().reset_index()
      stock_counts_by_sector.rename(
          columns={'symbol': 'symbol_count'}, inplace=True)
      stock_counts_by_sector.plot(
          ax=ax, kind='bar', x='sector', y='symbol_count')

      plt.title("Total Stocks in each Sector", fontsize=18)
      plt.ylabel("Total", fontsize=14)
      plt.xlabel("Sector", fontsize=14)
      plt.xticks(fontsize=12)
      plt.savefig('total_stocks_per_sector.png')

    def plot_histogram_of_betas(df):
      fig, ax = plt.subplots(figsize=(12, 10))
      ax.set_title('Histogram of Betas for each sector', fontsize=18)
      ax.set_ylabel('frequence', fontsize=14)
      ax.set_xlabel('beta value', fontsize=14)
      plt.tight_layout()
      df.rename(columns=IMPT_BETA_COLUMNS)[
          IMPT_BETA_COLUMNS.values()].hist(sharey=True, ax=ax)
      plt.savefig('Distribution of Betas over 5 year period.png')

    def plot_sector_betas_over_time(betas_df, title):
      fig, axs = plt.subplots(6, 2, sharey=True, figsize=(15, 35))
      plt.tight_layout()
      plt.subplots_adjust(hspace=.6)
      plt.xticks(fontsize=12)
      new_df = betas_df.set_index('Date')

      for sym, ax in zip(SECTOR_ETF_SYMBOLS.keys(), axs.flatten()):
        new_df[f'{sym.lower()}_beta'].plot(
            ax=ax)
        ax.axhline(y=1, color='r')
        ax.set_ylabel('beta', fontsize=14)
        ax.set_xlabel('date', fontsize=14)
        ax.set_title(SECTOR_ETF_SYMBOLS[sym], fontsize=14)

      fig.delaxes(axs[-1, -1])
      plt.savefig(title, bbox_inches="tight")

    def plot_average_betas(df, title):
      fig, ax = plt.subplots(figsize=(12, 8))
      ax.set_title(title, fontsize=18)
      ax.set_ylabel('beta', fontsize=14)
      ax.set_xlabel('sector', fontsize=14)
      new_df = df
      new_df['difference'] = df['historical_average_beta'] - \
          df['recent_average_beta']
      new_df.sort_values(by='difference', ascending=True, inplace=True)
      new_df[['sector', 'historical_average_beta', 'recent_average_beta']].plot(
          kind='bar', x='sector', ax=ax)
      plt.tight_layout()
      plt.savefig(title)

    def plot_histogram_of_betas(df):
      fig, ax = plt.subplots(figsize=(12, 8))
      ax.set_title('Histogram of Betas for each sector', fontsize=18)
      ax.set_ylabel('frequence', fontsize=14)
      ax.set_xlabel('beta value', fontsize=14)
      df[IMPT_BETA_COLUMNS.keys()].hist(ax=ax)

    def plot_correlation(df, title):
      fig, ax=plt.subplots(figsize=(12, 8))
      ax.set_title(title, fontsize=18)
      plt.xticks(fontsize=12)
      new_corr_df['recent_cat']='recent'
      sns.stripplot(ax=ax, x="category", y="correlation",
                    data=df, jitter=0.05)
      ax.set_ylabel('correlation', fontsize=16)
      ax.set_xlabel('time period', fontsize=16)
      plt.tight_layout()
      plt.savefig(title)
      plt.tight_layout()
      plt.savefig(title)

    def plot_correlation_matrix(df, title):
      fig, ax=plt.subplots(figsize=(10, 8))
      df[IMPT_COLUMNS.keys()]
      corrMatrix=df.corr()
      sns.heatmap(corrMatrix, annot=True, ax=ax, vmin=-1, vmax=1, linewidths=1,
                  xticklabels=IMPT_COLUMNS.values(), yticklabels=IMPT_COLUMNS.values())
      b, t=plt.ylim()
      b += 0.5
      t -= 0.5
      plt.ylim(b, t)
      ax.set_title(title, fontsize=16)
      plt.tight_layout()
      plt.savefig(title)
      plt.show()
