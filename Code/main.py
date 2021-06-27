from binance import *
from neural_network import *
from extra_functions import *

import numpy as np

def predictSymbol(symbol, binance, showPlots=False):

    coin = Coin(symbol=symbol, binance=binance)

    coin.getScaledData(hours_ago=12)

    n_per_learn = 90
    n_per_predict = 30

    input_X, input_Y = split_sequence(coin.df.to_numpy(), n_per_learn, n_per_predict)

    n_layers = 1
    n_nodes = 30

    neuralNetwork = NeuralNetwork(n_layers, n_nodes, n_per_learn, n_per_predict, coin.n_features)
    result = neuralNetwork.trainNN(input_X, input_Y)
    if showPlots: visualize_training_results(result)

    prediction = neuralNetwork.predictionNN(np.array(coin.df.tail(n_per_learn)).reshape(1, n_per_learn, coin.n_features))
    prediction = scalePrediction(prediction, coin.df, coin.close_scaler)
    if showPlots: plotPrediction(prediction)

    prediction = convertToPercentages(prediction)
    if showPlots: plotPrediction(prediction)

if __name__ == "__main__":
    print("running main")

    symbol_list = ['BTCUSDT']

    binance = Binance()

    while True:
        for symbol in symbol_list:
            predictSymbol(symbol, binance, showPlots=True)
        break