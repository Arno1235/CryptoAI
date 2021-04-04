import numpy as np
import matplotlib.pyplot as plt
from pandas._libs.tslibs import Timedelta
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

"""
Calculates the root mean square error between the two Dataframes
"""
def val_rmse(df1, df2, symbol):
    df = df1.copy()
    
    # Adding a new column with the closing prices from the second DF
    df['close2'] = df2['close_' + symbol]
    
    # Dropping the NaN values
    df.dropna(inplace=True)
    
    # Adding another column containing the difference between the two DFs' closing prices
    df['diff'] = df['close_' + symbol] - df.close2
    
    # Squaring the difference and getting the mean
    rms = (df[['diff']]**2).mean()
    
    # Returning the sqaure root of the root mean square
    return float(np.sqrt(rms))

def plot_predictionsVSactual(actual, predictions, symbol):
    # Printing the RMSE
    print("RMSE:", val_rmse(actual, predictions, symbol))
        
    # Plotting
    plt.figure(figsize=(16,6))

    # Plotting those predictions
    plt.plot(predictions, label='Predicted')

    # Plotting the actual values
    plt.plot(actual, label='Actual')

    plt.title(f"Predicted vs Actual Closing Prices")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

def plotPrediction(prediction, df, close_scaler, fmt):
    # Transforming the predicted values back to their original format
    prediction = close_scaler.inverse_transform(prediction)[0]

    # Creating a DF of the predicted prices
    preds = pd.DataFrame(prediction, 
                        index=pd.date_range(start=datetime.datetime.strptime(df.index[-1], fmt) + datetime.timedelta(minutes=1),
                                            periods=len(prediction),
                                            freq="1min"),
                        columns=[df.columns[0]])
    
    print(preds)

    plt.plot(preds, label='Prediction')
    plt.title("Prediction for " + str(datetime.datetime.strptime(df.index[-1], fmt) + datetime.timedelta(minutes=1)) + " until " + str(datetime.datetime.strptime(df.index[-1], fmt) + datetime.timedelta(minutes=len(prediction))))
    plt.show()


if __name__ == "__main__":
    print("running extra_analysis")