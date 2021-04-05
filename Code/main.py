from binance import *
from data_manipulation_functions import *
from neural_network import *
from extra_analysis import *

import numpy as np

def predictSymbol(symbol, showPlots=False):

    binance = Binance(symbol)

    binance.getData(6)
    binance.scaleData()

    n_per_learn = 90
    n_per_predict = 30

    input_X, input_Y = split_sequence(binance.df.to_numpy(), n_per_learn, n_per_predict)

    n_layers = 1
    n_nodes = 30

    neuralNetwork = NeuralNetwork(n_layers, n_nodes, n_per_learn, n_per_predict, binance.n_features)

    result = neuralNetwork.trainNN(input_X, input_Y)

    if showPlots: visualize_training_results(result)

    prediction = neuralNetwork.predictionNN(np.array(binance.df.tail(n_per_learn)).reshape(1, n_per_learn, binance.n_features))
    prediction = scalePrediction(prediction, binance.df, binance.close_scaler)
    if showPlots: plotPrediction(prediction)

if __name__ == "__main__":
    print("running main")

    symbol_list = ['BTCUSDT']

    while True:
        for symbol in symbol_list:
            predictSymbol(symbol, showPlots=True)
        break