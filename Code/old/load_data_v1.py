import pandas as pd
import ta
from sklearn.preprocessing import RobustScaler
import numpy as np

def loadData(csv_file, symbol, n_per_learn, n_per_predict):
    # Loading in the Data
    df = pd.read_csv(csv_file)

    ## Datetime conversion
    #df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Setting the index
    df.set_index('timestamp', inplace=True)

    # Dropping any NaNs
    df.dropna(inplace=True)

    ## Technical Indicators

    # Adding all the indicators
    df = ta.add_all_ta_features(df, open="open_" + symbol, high="high_" + symbol, low="low_" + symbol, close="close_" + symbol, volume="volume_" + symbol, fillna=True)

    # Dropping everything else besides 'Close' and the Indicators
    df.drop(["open_" + symbol, "high_" + symbol, "low_" + symbol, "volume_" + symbol], axis=1, inplace=True)

    ## Scaling

    # Scale fitting the close prices separately for inverse_transformations purposes later
    close_scaler = RobustScaler()

    close_scaler.fit(df[['close_' + symbol]])

    # Normalizing/Scaling the DF
    scaler = RobustScaler()

    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

    # Features 
    n_features = df.shape[1]
    # Splitting the data into appropriate sequences
    input_X, input_Y = split_sequence(df.to_numpy(), n_per_learn, n_per_predict)

    return df, n_features, input_X, input_Y, close_scaler

"""
Splits the multivariate time sequence
"""
def split_sequence(seq, n_steps_in, n_steps_out):

    # Creating a list for both variables
    input_X, input_Y = [], []
    
    for i in range(len(seq)):
        
        # Finding the end of the current sequence
        end = i + n_steps_in
        out_end = end + n_steps_out
        
        # Breaking out of the loop if we have exceeded the dataset's length
        if out_end > len(seq):
            break
        
        # Splitting the sequences into: x = past prices and indicators, y = prices ahead
        seq_x, seq_y = seq[i:end, :], seq[end:out_end, 0]
        
        input_X.append(seq_x)
        input_Y.append(seq_y)
    
    return np.array(input_X), np.array(input_Y)

def getActualData(close_scaler, df, symbol):
    # Transforming the actual values to their original price
    return pd.DataFrame(close_scaler.inverse_transform(df[["close_" + symbol]]), 
                        index=df.index, 
                        columns=[df.columns[0]])


if __name__ == "__main__":
    print("running load_data")