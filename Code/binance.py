from binance_mod.client import Client
import pandas as pd

class Binance:

    def __init__(self, fmt, symbol):
        self.loadAPISecret()
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
        self.fmt = fmt
        self.symbol = symbol

        self.org_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']
        self.imp_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    
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
            return
        print("Succesfully downloaded %s lines of data from %s for %s" % (str(len(klines)), self.symbol, hours))

        self.df = pd.DataFrame(klines, columns=self.org_columns)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='ms')
        self.df.set_index('timestamp', inplace=True)
        self.df.drop(columns=[item for item in self.org_columns if item not in self.imp_columns], axis=1, inplace=True)
        
        print(self.df)


if __name__ == "__main__":
    print("running binance")

    binance = Binance("", "BTCEUR")

    binance.getData(1)