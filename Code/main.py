from binance import *
from extra_analysis import *
from load_data import *
from neural_network import *
from notify_user import *
from place_buy import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import timedelta


if __name__ == "__main__":
    print("running main")

    binance = Binance()

    from_date = '2021-04-04 00:00:00'
    to_date = '2021-04-04 12:00:00'
    symbol = 'BTCUSDT'

    #binance.downloadData(symbol=symbol, from_date=from_date, to_date=to_date, output_filename=symbol+".csv")

    n_per_learn = 90
    n_per_predict = 30

    df, n_features, input_X, input_Y, close_scaler = loadData(".\\binance_data\\" + symbol + ".csv", symbol, n_per_learn, n_per_predict)

    n_layers = 1
    n_nodes = 30

    neuralNetwork = NeuralNetwork(symbol, n_layers, n_nodes, n_per_learn, n_per_predict, n_features)

    result = neuralNetwork.trainNN(input_X, input_Y)

    visualize_training_results(result)

    prediction = neuralNetwork.predictionNN(np.array(df.tail(n_per_learn)).reshape(1, n_per_learn, n_features))
    
    plotPrediction(prediction, df, close_scaler, binance.fmt)