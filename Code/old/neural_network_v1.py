# Neural Network library
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout


"""
Creates a specified number of hidden layers for an RNN
Optional: Adds regularization option - the dropout layer to prevent potential overfitting (if necessary)
"""
def layer_maker(n_layers, n_nodes, activation, drop=None, d_rate=.5):
    # Creating the specified number of hidden layers with the specified number of nodes
    for x in range(1,n_layers+1):
        model.add(LSTM(n_nodes, activation=activation, return_sequences=True))

        # Adds a Dropout layer after every Nth hidden layer (the 'drop' variable)
        try:
            if x % drop == 0:
                model.add(Dropout(d_rate))
        except:
            pass

"""
Runs a 'For' loop to iterate through the length of the DF and create predicted values for every stated interval
Returns a DF containing the predicted values for the model with the corresponding index values based on a business day frequency
"""
def validater(n_per_in, n_per_out):
    # Creating an empty DF to store the predictions
    predictions = pd.DataFrame(index=df.index, columns=[df.columns[0]])

    for i in range(n_per_in, len(df)-n_per_in, n_per_out):
        # Creating rolling intervals to predict off of
        x = df[-i - n_per_in:-i]

        # Predicting using rolling intervals
        yhat = model.predict(np.array(x).reshape(1, n_per_in, n_features))

        # Transforming values back to their normal prices
        yhat = close_scaler.inverse_transform(yhat)[0]

        # DF to store the values and append later, frequency uses business days
        pred_df = pd.DataFrame(yhat, 
                               index=pd.date_range(start=x.index[-1], 
                                                   periods=len(yhat), 
                                                   freq="B"),
                               columns=[x.columns[0]])

        # Updating the predictions DF
        predictions.update(pred_df)
        
    return predictions

"""
Creating the Neural Network
"""
def createNN():
    # Instatiating the model
    model = Sequential()

    # Activation
    activ = "tanh"

    # Input layer
    model.add(LSTM(90, 
                activation=activ, 
                return_sequences=True, 
                input_shape=(n_per_in, n_features)))

    # Hidden layers
    layer_maker(n_layers=1, 
                n_nodes=30, 
                activation=activ)

    # Final Hidden layer
    model.add(LSTM(60, activation=activ))

    # Output layer
    model.add(Dense(n_per_out))

    # Model summary
    model.summary()

    # Compiling the data with selected specifications
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    return model

"""
Fitting and Training Neural Network
"""
def trainNN(model):
    res = model.fit(X, y, epochs=100, batch_size=256, validation_split=0.1) # original: 50, 128, 0.1

if __name__ == "__main__":
    print("running neural_network")