## Assessing Recent Volatility of Economic Sectors


The US stock market has experienced an extreme period of volatility since late February 2020. The economic impact of the Coronavirus outbreak has led to significant changes in business activity. The volatility of the S&P 500 as measured by the CBOE volatility index reached its highest value on March 16 since the 2008 recession ([source](https://finance.yahoo.com/news/stock-market-volatility-tops-financial-205105166.html)).

The goal of this project is to assess the changes in volatility and correlation of particular sectors that make up the Standard & Poors 500 index.

![Sector Counts](/plots/total_stocks_in_each_sector.png)


### Questions

1. Given the great increase in volatility of the overall market, has the relative volatility of individual sectors changed since the beginning of the coronavirus outbreak and the rapid stock market decline?

2. How has the correlation between market and sectors changed since the beginning of the stock market decline? Do the sectors continue to move in the same or different pattern as the overall market?

### Data

In order to measure volatility, I used Beta calculation for sectors relative to the S&P benchmark. Beta is measure of an asset's correlation to the risk in the overall market and can be either positive or negative.

Notes on beta:

- Can be calculated as the covariance (benchmark, asset) / variance (benchmark)
- Beta of 1 indicates that the asset is more volatile than the index
- Beta less than 1 means indicates that asset is less volatile than the index
- Negative beta means that the asset moves in the opposite direction as the market

To calculate beta, I used a [library](https://github.com/ranaroussi/yfinance) that interfaces with Yahoo Finance to retrieve daily price data across the S&P and sectors, using the S&P SPDR exchanged traded funds (ETF) for sectors. The sector ETF's are already weighted for holdings per company.

10 period betas of exchange traded funds (ETF's) for each sector were calculated based on the daily percent change of the sectors. I then compared Beta for 10 periods after the beginning of the recent stock market decline (February 21, 2020), March 7, 2020 up to April 8, 2020, with prior one month, three month, 1 year, and 5 year data. The recent data since March 7 consisted of a sample size of 23 data points.

I used a one-tailed t-test (Welch’s t-test given differences of size and variance of compared samples) to compare whether there were significant changes in Beta with previous time periods.

Histogram of betas over 5 year period:

![Betas Histogram](/plots/betas_histogram.png)

Histogram shows that some sectors have lower betas generally than the S&P, such as Consumer Staples, while Information Technology often has higher betas.

### Hypothesis

#### Null

- 10 period beta of sectors has not changed significantly in recent period compared to previous one month, three month, one year, and three year intervals. I defined the recent period as between February 21, 2020 through April 8, 2020, with beta calculations beginning 10 periods after February 21.

#### Alternative

There is a significant increase or decrease in relative volatility for sectors that have been impacted by the recent economic state.

### Findings

Below is a table of p values showing sectors with a significant increase, decrease, or no change in beta for varying time periods.

![P-values](/data/p_values_over_time.png)

- Industrials, Materials, Health Care, and Consumer Discretionary sectors have not experienced significant volatility changes over most time periods.
- Financials, Consumer Staples, Real Estate, and Utilities have experienced significant increase in volatility over all time periods
- Information Technology has experienced significant decrease in volatility for all time periods

Looking at the differences in average betas between the recent period and prior time frames, we see that Utilities and Real Estate have the highest increase in average beta while Information Technology and Communication Services have the lowest decrease in average beta.

![Sector Counts](/plots/average_betas/one_year.png)

![Sector Counts](/plots/average_betas/five_year.png)

In general, the sectors betas have got closer to 1. Sectors such as Utilities and Real Estate with lower average volatility than the market have increased in beta. Information Technology and Communication Services, two sectors with higher volatility, have decreased in beta.

Beta over one year for these sectors:

![Betas over time 1](/plots/betas_over_time/xlc-xlk-betas-one-year.png)

![Betas over time 2](/plots/betas_over_time/xlre-xlu-betas-one-year.png)

### Correlation

I also looked at the correlation between sectors and the index over time, to get a sense of the pattern of price movements.

![Correlation Scatter](/plots/correlation/time_period_scatter.png)

The scatter plot of correlation for sectors and the index and time intervals shows closer correlation to 1 among all sectors in the recent period compared to previous periods.

Correlation Between Sectors:

![Correlation Matrix 1 Year](/plots/correlation/one_year_matrix.png)

![Correlation Matrix 3 Month](/plots/correlation/three_month_matrix.png)

![Correlation Matrix Recent](/plots/correlation/recent_period_matrix.png)

### Discussion

In the recent time period we have seen beta and correlation, when compared to the S&P index, get closer to 1 across many sectors. In addition, we have seen a strong increase in correlation between all sectors. This is an indication that the magnitude and the pattern of price changes across the sectors in the recent period of economic uncertainity have been roughly equivalent. Sectors that have more relative risk in terms of their price movements such as Information Technology, have less overall risk, while the opposite is true for lower beta sectors such as Utilities.

### Improvements

- Identify the proper techniques for evaluating changes in time series data, accounting for autocorrelation. T-test is not an appropriate mechanism for evaluating changes in financial data as previous data points influence future data.
- Incorporate individual industries that make up specific sectors to get a sense of variation within sectors in volatility
- Compare changes to previous recessions to determine if there are trends specific to periods of economic decline
