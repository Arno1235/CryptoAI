from binance import *
from extra_analysis import *
from load_data import *
from neural_network import *
from notify_user import *
from place_buy import *
import numpy as np
import datetime

def predictSymbol(symbol, showPlots=False, fmt="%Y-%m-%d %H:%M:%S"):

    binance = Binance(fmt)

    from_date = datetime.datetime.strptime(datetime.datetime.now(), fmt) - datetime.timedelta(minutes = 125)
    to_date = datetime.datetime.strptime(datetime.datetime.now(), fmt)

    binance.downloadData(symbol=symbol, from_date=from_date, to_date=to_date, output_filename=symbol+".csv")

    n_per_learn = 90
    n_per_predict = 30

    df, n_features, input_X, input_Y, close_scaler = loadData(".\\binance_data\\" + symbol + ".csv", symbol, n_per_learn, n_per_predict)

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