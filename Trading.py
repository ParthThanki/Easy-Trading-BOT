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