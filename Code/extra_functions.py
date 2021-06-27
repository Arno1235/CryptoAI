# Extra Functions libraries
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("bmh")
import pandas as pd
import datetime



# Splits the multivariate time sequence
def split_sequence(seq, n_per_learn, n_per_predict):

    # Creating a list for both variables
    input_X, input_Y = [], []
    
    for i in range(len(seq)):
        
        # Finding the end of the current sequence
        end = i + n_per_learn
        out_end = end + n_per_predict
        
        # Breaking out of the loop if we have exceeded the dataset's length
        if out_end > len(seq):
            break
        
        # Splitting the sequences into: x = past prices and indicators, y = prices ahead
        seq_x, seq_y = seq[i:end, :], seq[end:out_end, 0]
        
        input_X.append(seq_x)
        input_Y.append(seq_y)
    
    return np.array(input_X), np.array(input_Y)

# Plots the loss and accuracy for the training and testing data
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

# Returns scaled prediction
def scalePrediction(prediction, df, close_scaler, fmt="%Y-%m-%d %H:%M:%S"):
    # Transforming the predicted values back to their original format
    prediction = close_scaler.inverse_transform(prediction)[0]

    # Creating a DF of the predicted prices
    return pd.DataFrame(prediction, 
                        index=pd.date_range(start=datetime.datetime.strptime(df.index[-1], fmt) + datetime.timedelta(minutes=1),
                                            periods=len(prediction),
                                            freq="1min"),
                        columns=[df.columns[0]])

# Returns a table of the difference from the first value in percentages
def convertToPercentages(df):
    for i in range(1, len(df)):
        df['close'].iloc[i] = 100 * (df['close'].iloc[i] - df['close'].iloc[0]) / df['close'].iloc[0] # Difference in percentage
    df['close'].iloc[0] = 0
    return df

# Plots the predictions
def plotPrediction(preds):
    plt.plot(preds, label='Prediction')
    plt.show()



if __name__ == "__main__":
    print("running extra_analysis")