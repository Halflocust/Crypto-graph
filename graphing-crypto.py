import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib as mpl 
import matplotlib.dates as mdates
import datetime as dt 

plt.style.use('ggplot')

years = mdates.YearLocator()
months = mdates.MonthLocator()
yearsFMT = mdates.DateFormatter('%Y')

# Writes the files to a specific directory. Change this to suit you
df = pd.read_csv("coin_dfs/final_df/BTC.csv")

df2 = df.loc[:,["Date","rsi_14d"]]
df2.dropna(inplace=True)

df2.reset_index(inplace=True)

df["Date"] = df.Date.astype("datetime64[ns]")
df["Date"] = df.Date.map(mdates.date2num)

df2["Date"] = df2.Date.astype("datetime64[ns]")
df2["Date"] = df2["Date"].map(mdates.date2num)

fig = plt.figure(figsize=(12,6))

#share price and 50ma plot
ax = fig.add_subplot(211)
ax.plot(df.Date,df.Close,label="Close")
ax.xaxis_date()
ax.plot(df.Date,df.ma50,label="50 day ma")
ax.legend()
ax.set(title="BTC daily move",xlabel="Date",ylabel="USD")

#RSI plot
ax1 = fig.add_subplot(212,label="BTC")
ax1.plot(df2.Date, df2.rsi_14d)
ax1.axhline(70)
ax1.axhline(30)
ax1.set(title="rsi - 14 day intervals",xlabel="Date",ylabel="RSI")
ax1.xaxis_date()
ax1.legend(["BTC RSI"])


# def plots_coin_info(coin):
# 	df = pd.read_csv("coin_dfs/final_df/{}.csv".format(coin))
# 	df.Date = df.Date.astype("datetime64[ns]")
# 	df.Date = df.Date.map(mdates.date2num)
# 	df2 = df.loc[:,["Date","rsi_14d"]]
# 	fig = plt.figure()
	

 
plt.tight_layout()
plt.show()