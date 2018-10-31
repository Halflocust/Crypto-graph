import pandas as pd 
import pandas_datareader as web 
import datetime as dt 
import requests
import os
import numpy as np 
import matplotlib as mpl 


#Enter coins that you are interested in in the list below. These are the names used on coinmarketcap. So use the names on coinmarketcap for success
coins = ["Bitcoin", "Ethereum", "Litecoin","XRP","EOS"]


def get_tickers_all_crypto():
	#pointless - just wanted to do it
	coinmarketcap_url_ticks = 'https://api.coinmarketcap.com/v2/listings/'
	available_crypto_ticks = requests.get(coinmarketcap_url_ticks, headers={"Accept": "application/json"}).json()
	data = available_crypto_ticks["data"]
	#returns the symbols for all crypto currencies listed on coinmarketcap
	for item in data:
		print(item["symbol"])


def get_coin_info(coins):
	coin_symbols = []
	coinmarketcap_url_listing = 'https://api.coinmarketcap.com/v2/listings/'
	crypto_listing = requests.get(coinmarketcap_url_listing, headers={"Accept":"application/json"}).json()
	data = crypto_listing["data"]
	for crypto in coins:
		for item in data:
			if item["name"] == crypto:
				coin_symbols.append(item["symbol"])
	return coin_symbols
			
def save_historic_data_to_csv():
	if not os.path.exists("coin_dfs/historic"):
		os.makedirs("coin_dfs/historic") 
	coins_list = get_coin_info(coins)
	start = dt.datetime(2016,1,1)
	end = dt.datetime(2018,12,31)
	for item in coins_list:
		if not os.path.exists("coin_dfs/historic/{}".format(item)):
			print("Grabbing data for {}".format(item))
			df = web.DataReader(item+"-USD","yahoo",start,end)
			df.to_csv("coin_dfs/historic/{}.csv".format(item))
		else:
			print("already have the data for {}".format(coin))

def assemble_df_csv(coins):
	for coin in coins:
		# Moving averages added to df
		df = pd.read_csv("coin_dfs/historic/{}.csv".format(coin))
		df.set_index("Date",inplace=True)
		df["ma20"] = df.Close.rolling(window=20).mean()
		df["ma50"] = df.Close.rolling(window=50).mean()
		df["ma100"] = df.Close.rolling(window=100).mean()
		#Prepping the df for the RSI field:
		df["daily_move"] = df.Close - df.Close.shift(1)
		df["avg_gain"] = np.where(df.daily_move > 0,df.daily_move,0)
		df["avg_loss"] = np.where(df.daily_move < 0,df.daily_move * -1,0)
		# Bringing the RSI into the df:
		df["rsi_14d"] = 100-(100/(1+ (df.avg_gain.rolling(window=14).mean()/df.avg_loss.rolling(window=14).mean())))
		df.to_csv("coin_dfs/final_df/{}.csv".format(coin))

# def rsi_calculation_14d(data_frame):
# 	df = data_frame
# 	df.set_index("Date",inplace=True)
# 	#Prepping the df for th RSI
# 	df["daily_move"] = df.Close - df.Close.shift(1)
# 	df["avg_gain"] = np.where(df.daily_move > 0,df.daily_move,0)
# 	df["avg_loss"] = np.where(df.daily_move < 0,df.daily_move * -1,0)
# 	# Bringing the RSI into the df
# 	df["rsi"] = 100-(100/(1+ (df.avg_gain.rolling(window=14).mean()/df.avg_loss.rolling(window=14).mean())))


	






