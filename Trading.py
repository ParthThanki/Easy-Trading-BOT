import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# historical data for S&P 500
Sp_Data = yf.download('^GSPC', start='2020-01-01', end='2021-01-01')

# Calculating moving averages
short_window = 40
long_window = 100

Sp_Data['short_mavg'] = Sp_Data['Close'].rolling(window=short_window, min_periods=1).mean()
Sp_Data['long_mavg'] = Sp_Data['Close'].rolling(window=long_window, min_periods=1).mean()

# Generate signals
Sp_Data['signal'] = 0
Sp_Data['signal'][short_window:] = np.where(Sp_Data['short_mavg'][short_window:] > Sp_Data['long_mavg'][short_window:], 1, 0)

# Generate trading orders
Sp_Data['position'] = Sp_Data['signal'].diff()

# Plotting the data
plt.figure(figsize=(10,5))
plt.plot(Sp_Data['Close'], label='S&P 500')
plt.plot(Sp_Data['short_mavg'], label='40-Day Moving Average')
plt.plot(Sp_Data['long_mavg'], label='100-Day Moving Average')

# Plot Buy Signals
plt.plot(Sp_Data[Sp_Data['position'] == 1].index, Sp_Data['short_mavg'][Sp_Data['position'] == 1], '^', markersize=10, color='g', lw=0, label='Buy')

# Plot Sell Signals
plt.plot(Sp_Data[Sp_Data['position'] == -1].index, Sp_Data['short_mavg'][Sp_Data['position'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell')

plt.title("S&P 500 - Moving Average Crossover")
plt.legend()
plt.show()

# Simulate Trades Testing
initial_capital = float(10000.0)  # Starting capital
positions = pd.DataFrame(index=Sp_Data.index).fillna(0.0)

# Buy a 100 shares
positions['S&P500'] = 100 * Sp_Data['signal']

# Initialize the portfolio with value owned
portfolio = positions.multiply(Sp_Data['Close'], axis=0)

# Store the difference in shares owned
pos_diff = positions.diff()

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(Sp_Data['Close'], axis=0)).sum(axis=1)

# Add `cash` to portfolio
portfolio['cash'] = initial_capital - (pos_diff.multiply(Sp_Data['Close'], axis=0)).sum(axis=1).cumsum()

# Add `total` to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add `returns` to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

# Plot the equity curve
plt.figure(figsize=(10,5))
plt.plot(portfolio['total'], label='Portfolio value')
plt.title('Equity Curve')
plt.legend()
plt.show()