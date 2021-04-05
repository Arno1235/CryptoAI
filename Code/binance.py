from binance_mod.client import Client
from datetime import datetime, timedelta

class Binance:

    def __init__(self, fmt, symbol):
        self.loadAPISecret()
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
        self.fmt = fmt
        self.symbol = symbol
    
    def loadAPISecret(self):
        with open ("secret.txt", "r") as myfile:
            data = myfile.read().splitlines()
            self.api_key = data[0]
            self.api_secret = data[1]
    
    def getData(self, hours, time_interval=Client.KLINE_INTERVAL_1MINUTE):
        hours = str(hours) + " hour ago UTC"
        klines = self.client.get_historical_klines(self.symbol, time_interval, hours)
        if len(klines) < 1:
            print("Failed to download data from %s for %s." % (self.symbol, hours))
        else:
            print("Succesfully downloaded %s lines of data from %s for %s" % (str(len(klines)), self.symbol, hours))
        


if __name__ == "__main__":
    print("running binance")

    binance = Binance("", "BTCEUR")

    binance.getData(1)