from binance_mod.client import Client
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import time


class Binance:

    def __init__(self, fmt):
        self.loadAPI()
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
        self.fmt = fmt

        self.org_columns = ['open',
                            'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                            'trades', 'tb_base_av', 'tb_quote_av', 'ignore']

        self.columns = ['open', 'high', 'low', 'close', 'volume']
    
    def loadAPI(self):
        with open ("secret.txt", "r") as myfile:
            data = myfile.read().splitlines()
            self.api_key = data[0]
            self.api_secret = data[1]
    
    """
    Download data from Binance
    Step: Step in number of days. Download data in batches of days given by 'step'
    Pause: Pause seconds before downloading next batch.
        if pause == -1 --> random sleep(2,5)
        if pause == 0 --> no sleep
        if pause == num--> sleep for num of seconds
    """
    def downloadData(self, symbol, from_date, to_date, time_interval=Client.KLINE_INTERVAL_1MINUTE, output_filename="output.csv", step=1, pause=-1, simulate=False):
        from_date_obj = datetime.strptime(from_date, self.fmt)
        step_date_obj = from_date_obj + timedelta(days=step)
        step_date = step_date_obj.strftime(self.fmt)

        from_millis = self.to_unixmillis(from_date)
        to_millis = self.to_unixmillis(to_date)
        step_millis = self.to_unixmillis(step_date)

        count = 0
        while True:
            from_millis_str = str(from_millis)
            step_millis_str = str(step_millis)
            print('Step %d:Downloading data from %s to %s' % (count,
                                                            str(self.to_datetime(from_millis_str)),
                                                            str(self.to_datetime(step_millis_str))
                                                            ))
            if not simulate:
                # download data

                klines = self.client.get_historical_klines(symbol, time_interval,
                                                            from_millis_str, end_str=step_millis_str)
                klines_len = len(klines)
                if klines_len == 0:
                    print('\t Failed to download from %s to %s. Got %d' % (str(self.to_datetime(from_millis_str)),
                                                                        str(self.to_datetime(step_millis_str)), klines_len
                                                                        ))
                    time.sleep(5)

                print('\t Downloaded data of len %d from %s to %s' % (klines_len,
                                                                    str(self.to_datetime(from_millis_str)),
                                                                    str(self.to_datetime(step_millis_str))
                                                                    ))
                new_columns = [item + '_' + symbol for item in self.org_columns]
                new_columns.insert(0, 'timestamp')

                data_df = pd.DataFrame(klines,
                                    columns=new_columns)
                data_df['timestamp'] = pd.to_datetime(data_df['timestamp'], unit='ms')
                data_df.set_index('timestamp', inplace=True)

                # Dropping everything else besides the columns in self.columns and timestamp
                data_df.drop(columns=[item + '_' + symbol for item in [item for item in self.org_columns if item not in self.columns]], axis=1, inplace=True)

                data_df.to_csv(".\\binance_data\\" + output_filename)

            # move to next step of batches
            from_millis = step_millis
            step_date_obj = step_date_obj + timedelta(days=step)
            step_date = step_date_obj.strftime(self.fmt)
            step_millis = self.to_unixmillis(step_date)
            count = count + 1
            if pause == -1:
                pause = np.random.randint(2, 5)
            time.sleep(pause)
            if step_millis >= to_millis:
                break
    
    def to_unixmillis(self, from_date):
        from_date_obj = datetime.strptime(from_date, self.fmt)
        past = datetime(1970, 1, 1, tzinfo=from_date_obj.tzinfo)
        return int((from_date_obj - past).total_seconds() * 1000.0)
    
    def to_datetime(self, ms):
        return datetime.fromtimestamp(int(float(ms) / 1000.0))

if __name__ == "__main__":
    print("running binance")

    binance = Binance()

    from_date = '2021-04-04 00:00:00'
    to_date = '2021-04-04 12:00:00'
    symbol = 'BTCUSDT'

    binance.downloadData(symbol=symbol, from_date=from_date, to_date=to_date, output_filename=symbol+".csv")