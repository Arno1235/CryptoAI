from binance import Binance, Coin
from neural_network import NeuralNetwork, ACCURACY_THRESHOLD, TIME_THRESHOLD
from extra_functions import *
from notify_user import notifyUser
from log import Log
from interpret_data import minmax_interpration

import datetime
import time
import numpy as np



def predictCoin(coin, showPlots=False, log=Log()):

    coin.getScaledData(hours_ago=12)

    n_per_learn = 180 # 90
    n_per_predict = 60 # 30

    input_X, input_Y = split_sequence(coin.df.to_numpy(), n_per_learn, n_per_predict)

    n_layers = 1 # 1
    n_nodes = 30 # 30

    neuralNetwork = NeuralNetwork(n_layers, n_nodes, n_per_learn, n_per_predict, coin.n_features)
    result = neuralNetwork.trainNN(input_X, input_Y, epochs=1000)
    if showPlots: visualize_training_results(result)

    prediction = neuralNetwork.predictionNN(np.array(coin.df.tail(n_per_learn)).reshape(1, n_per_learn, coin.n_features))
    prediction = scalePrediction(prediction, coin.df, coin.close_scaler)
    if showPlots: plotPrediction(prediction)

    first_value = prediction['close'].iloc[0]

    prediction_in_percentages = convertToPercentages(prediction)
    if showPlots: plotPrediction(prediction_in_percentages)

    acc = result.history['accuracy'][-1]
    
    # if acc > ACCURACY_THRESHOLD:
    #     interpretation = minmax_interpration(prediction=prediction_in_percentages, first_value=first_value)
    #     if interpretation != False:
    #         min_sell, max_sell = interpretation
    #         notifyUser("You should buy %s and sell at %f and %f, I am %f sure." %(symbol, min_sell, max_sell, acc))
    #         log.write("TEST: buy %s and sell at %f and %f, accuracy = %f" %(symbol, min_sell, max_sell, acc))

    if acc > ACCURACY_THRESHOLD:
        min, max = minmax_interpration(prediction=prediction_in_percentages, first_value=first_value)
        log.write([symbol, min, max])

    log.save()

if __name__ == "__main__":
    print("running main")

    symbol_list = ['BTCEUR', 'DOGEEUR', 'LTCEUR', 'VETEUR', 'ADAEUR', 'ETHEUR']

    binance = Binance()

    coin_list = []
    for symbol in symbol_list:
        coin = Coin(symbol=symbol, binance=binance, log=Log(symbol))
        coin_list.append(coin)

    while True:
        for coin in coin_list:
            time0 = datetime.datetime.now()
            predictCoin(coin=coin, binance=binance, showPlots=False, log=log)
            timediff = (datetime.datetime.now() - time0).total_seconds()
            if timediff < TIME_THRESHOLD:
                print("Sleeping for %i seconds." %(TIME_THRESHOLD - timediff))
                time.sleep(TIME_THRESHOLD - timediff)