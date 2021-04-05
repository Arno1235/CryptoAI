import numpy as np
import matplotlib.pyplot as plt
plt.style.use("bmh")
import pandas as pd
import datetime


"""
Plots the loss and accuracy for the training and testing data
"""
def visualize_training_results(results):
    history = results.history
    plt.figure(figsize=(16,5))
    plt.plot(history['val_loss'])
    plt.plot(history['loss'])
    plt.legend(['val_loss', 'loss'])
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.show()
    
    plt.figure(figsize=(16,5))
    plt.plot(history['val_accuracy'])
    plt.plot(history['accuracy'])
    plt.legend(['val_accuracy', 'accuracy'])
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.show()

def scalePrediction(prediction, df, close_scaler, fmt="%Y-%m-%d %H:%M:%S"):
    # Transforming the predicted values back to their original format
    prediction = close_scaler.inverse_transform(prediction)[0]

    # Creating a DF of the predicted prices
    return pd.DataFrame(prediction, 
                        index=pd.date_range(start=datetime.datetime.strptime(df.index[-1], fmt) + datetime.timedelta(minutes=1),
                                            periods=len(prediction),
                                            freq="1min"),
                        columns=[df.columns[0]])

def plotPrediction(preds):

    plt.plot(preds, label='Prediction')
    plt.show()


if __name__ == "__main__":
    print("running extra_analysis")