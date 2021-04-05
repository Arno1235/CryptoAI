from binance_mod.client import Client
import pandas as pd

class Binance:

    def __init__(self, symbol):
        self.loadAPISecret()
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
        self.symbol = symbol

        self.org_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']
        self.imp_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    
    def loadAPISecret(self):
        with open ("secret.txt", "r") as myfile:
            data = myfile.read().splitlines()
            self.api_key = data[0]
            self.api_secret = data[1]
    
    def getAccountInfo(self):
        self.accountInfo = self.client.get_account()
        self.accountStatus = self.client.get_account_status()
    
    def getStatus(self):
        self.status = self.client.get_system_status()["msg"]
    
    def getTradeFee(self):
        self.tradeFee = self.client.get_trade_fee(symbol=self.symbol)
    
    def getAllOrders(self):
        self.allOrders = self.client.get_all_orders(symbol=self.symbol)
    
    def getOpenOrders(self):
        self.openOrders = self.client.get_open_orders(symbol=self.symbol)
    
    def getTrades(self):
        self.trades = self.client.get_my_trades(symbol=self.symbol)
    
    def getData(self, hours_ago, time_interval=Client.KLINE_INTERVAL_1MINUTE):
        hours_ago = str(hours_ago) + " hour ago UTC"
        klines = self.client.get_historical_klines(self.symbol, time_interval, hours_ago)
        if len(klines) < 1:
            print("Failed to download data from %s for %s." % (self.symbol, hours_ago))
            return
        print("Succesfully downloaded %s lines of data from %s for %s" % (str(len(klines)), self.symbol, hours_ago))

        self.df = pd.DataFrame(klines, columns=self.org_columns)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='ms')
        self.df.set_index('timestamp', inplace=True)
        self.df.drop(columns=[item for item in self.org_columns if item not in self.imp_columns], axis=1, inplace=True)
    
    


if __name__ == "__main__":
    print("running binance")

    binance = Binance(symbol="BTCEUR")

    binance.getData(1)
    print(binance.df)

    binance.getAccountInfo()
    print(binance.accountInfo)
    print(binance.accountStatus)

    binance.getStatus()
    print(binance.status)

    binance.getTradeFee()
    print(binance.tradeFee)

    binance.getAllOrders()
    print(binance.allOrders)

    binance.getOpenOrders()
    print(binance.openOrders)

    binance.getTrades()
    print(binance.trades)