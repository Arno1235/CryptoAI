# Binance libraries
from log import Log
from binance_mod.client import Client
import os
import pandas as pd
import ta
from sklearn.preprocessing import RobustScaler

# TODO
# Place buy
# Load amount of euro you can buy with



# General Binance API class
class Binance:

    # Initializes the class
    # aks_buy: ask for permission from user to buy
    # basic_coin: basic coin to calculate the assets
    def __init__(self, ask_buy=True, basic_coin="EUR"):
        api_key, api_secret = self.loadAPISecret()
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.ask_buy = ask_buy
        self.basic_coin = basic_coin

        self.update()
    
    # Updates all the account variables
    def update(self):
        self.getAccountInfo()
        self.getStatus()
        self.getAssets()
    
    # Returns the API key and API secret from the secret.txt file
    def loadAPISecret(self):
        with open ("secret.txt", "r") as myfile:
            data = myfile.read().splitlines()
            return data[0], data[1]
    
    # Loads the account information
    def getAccountInfo(self):
        self.accountInfo = self.client.get_account()
        self.accountStatus = self.client.get_account_status()
    
    # Loads the account status
    def getStatus(self):
        self.status = self.client.get_system_status()["msg"]
    
    # Loads the average value for all the coins in possession
    def getAssets(self):
        self.assets = []
        self.assets.append({'asset': "Total " + self.basic_coin, 'value': 0.0})
        balances = self.accountInfo["balances"]
        for symbol in balances:
            if float(symbol["free"]) > 0:
                price = float(self.client.get_avg_price(symbol=symbol["asset"] + self.basic_coin)["price"])
                value = float(symbol["free"]) * price
                self.assets.append({'asset': symbol["asset"], 'amount': symbol["free"], 'price': price, 'value': value})
                self.assets[0]["value"] += value

# Class for the coin itself
class Coin:

    # Initializes the class
    def __init__(self, symbol, binance, log=Log()):
        self.symbol = symbol
        self.binance = binance
        self.log = log

        # Data columns
        self.org_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']
        self.imp_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

        self.update()
    
    # Updates all the coin variables
    def update(self):
        self.getTradeFee()
        self.getAllOrders()
        self.getOpenOrders()
        self.getTrades()
    
    # Loads trade fee
    def getTradeFee(self):
        self.tradeFee = self.binance.client.get_trade_fee(symbol=self.symbol)
    
    # Loads all orders
    def getAllOrders(self):
        self.allOrders = self.binance.client.get_all_orders(symbol=self.symbol)
    
    # Loads open orders
    def getOpenOrders(self):
        self.openOrders = self.binance.client.get_open_orders(symbol=self.symbol)
    
    # Loads trades
    def getTrades(self):
        self.trades = self.binance.client.get_my_trades(symbol=self.symbol)
    
    # Returns data
    # hours_ago: amount of hours to look back
    # time_interval: time interval to get the data
    def getData(self, hours_ago, time_interval=Client.KLINE_INTERVAL_1MINUTE):
        hours_ago = str(hours_ago) + " hour ago UTC"
        klines = self.binance.client.get_historical_klines(self.symbol, time_interval, hours_ago)
        if len(klines) < 1:
            print("Failed to download data from %s for %s." % (self.symbol, hours_ago))
            return
        print("Succesfully downloaded %s lines of data from %s for %s" % (str(len(klines)), self.symbol, hours_ago))

        df_org = pd.DataFrame(klines, columns=self.org_columns)
        df_org['timestamp'] = pd.to_datetime(df_org['timestamp'], unit='ms')
        df_org.set_index('timestamp', inplace=True)
        df_org.drop(columns=[item for item in self.org_columns if item not in self.imp_columns], axis=1, inplace=True)
        df_org.dropna(inplace=True)
        return df_org

    # Loads scaled data in self.df
    def scaleData(self, df_org):
        df_org.to_csv("temp.csv")
        self.df = pd.read_csv("temp.csv")
        self.df.set_index('timestamp', inplace=True)

        self.df = ta.add_all_ta_features(self.df, open='open', high='high', low='low', close='close', volume='volume', fillna=True)
        self.df.drop(["open", "high", "low", "volume"], axis=1, inplace=True)

        self.close_scaler = RobustScaler()
        self.close_scaler.fit(self.df[["close"]])

        self.scaler = RobustScaler()
        self.df = pd.DataFrame(self.scaler.fit_transform(self.df), columns=self.df.columns, index=self.df.index)

        self.n_features = self.df.shape[1]

        if os.path.exists("temp.csv"): os.remove("temp.csv")
    
    # Combines getData and scaleData
    def getScaledData(self, hours_ago, time_interval=Client.KLINE_INTERVAL_1MINUTE):
        self.scaleData(self.getData(hours_ago=hours_ago, time_interval=time_interval))
    
    # TODO
    def placeBuy(self):
        if self.binance.ask_buy:
            if input("Are you sure I can place the buy?\n") != "yes":
                print("Buy canceled")
                return

        print("Buy")



if __name__ == "__main__":
    print("running binance")

    binance = Binance()
    btceur = Coin(symbol="BTCEUR", binance=binance)

    btceur.getScaledData(hours_ago=1)
    print("Scaled data")
    print(btceur.df)

    print("Account info")
    print(binance.accountInfo)
    print("Account status")
    print(binance.accountStatus)
    print("Account assets")
    print(binance.assets)

    print("Binance status")
    print(binance.status)

    print("Trade fee")
    print(btceur.tradeFee)

    print("All orders")
    print(btceur.allOrders)

    print("Open orders")
    print(btceur.openOrders)

    print("Trades")
    print(btceur.trades)

    btceur.placeBuy()