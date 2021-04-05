from binance import *
from data_manipulation_functions import *

import numpy as np

def predictSymbol(symbol, showPlots=False, fmt="%Y-%m-%d %H:%M:%S"):

    binance = Binance(symbol)

    binance.getData(6)
    binance.scaleData()

    n_per_learn = 90
    n_per_predict = 30

    input_X, input_Y = split_sequence(binance.df.to_numpy(), n_per_learn, n_per_predict)

    n_layers = 1
    n_nodes = 30

    neuralNetwork = NeuralNetwork(symbol, n_layers, n_nodes, n_per_learn, n_per_predict, n_features)

    result = neuralNetwork.trainNN(input_X, input_Y)

    if showPlots: visualize_training_results(result)

    prediction = neuralNetwork.predictionNN(np.array(df.tail(n_per_learn)).reshape(1, n_per_learn, n_features))
    prediction = scalePrediction(prediction, df, close_scaler, fmt)
    if showPlots: plotPrediction(prediction, df, fmt)

if __name__ == "__main__":
    print("running main")

    symbol_list = ['BTCUSDT']

    while True:
        for symbol in symbol_list:
            predictSymbol(symbol, showPlots=True)
        break