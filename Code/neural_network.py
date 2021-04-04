# Neural Network library
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout


class NeuralNetwork:

    def __init__(self, crypto, n_layers, n_nodes, n_per_learn, n_per_predict, n_features):
        self.crypto = crypto
        self.n_layers = n_layers
        self.n_nodes = n_nodes
        self.n_per_learn = n_per_learn
        self.n_per_predict = n_per_predict
        self.n_features = n_features
        self.activation = "tanh"

        self.createNN()
    
    """
    Creating the Neural Network
    """
    def createNN(self):
        # Instatiating the model
        self.model = Sequential()

        # Input layer
        self.model.add(LSTM(90, 
                    activation=self.activation, 
                    return_sequences=True, 
                    input_shape=(self.n_per_learn, self.n_features)))

        # Hidden layers
        self.layer_maker()

        # Final Hidden layer
        self.model.add(LSTM(60, activation=self.activation))

        # Output layer
        self.model.add(Dense(self.n_per_predict))

        # Model summary
        self.model.summary()

        # Compiling the data with selected specifications
        self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    """
    Creates a specified number of hidden layers for an RNN
    Optional: Adds regularization option - the dropout layer to prevent potential overfitting (if necessary)
    """
    def layer_maker(self, drop=None, d_rate=.5):
        # Creating the specified number of hidden layers with the specified number of nodes
        for x in range(1, self.n_layers+1):
            self.model.add(LSTM(self.n_nodes, activation=self.activation, return_sequences=True))

            # Adds a Dropout layer after every Nth hidden layer (the 'drop' variable)
            try:
                if x % drop == 0:
                    self.model.add(Dropout(d_rate))
            except:
                pass
    
    """
    Fitting and Training Neural Network
    """
    def trainNN(self, input_X, input_Y):
        self.model.fit(input_X, input_Y, epochs=50, batch_size=128, validation_split=0.1)
    
    """
    Predict Using Neural Network
    """
    def predictionNN(self, input_data):
        # Predicting off of the most recent days from the original DF
        return self.model.predict(input_data)


if __name__ == "__main__":
    print("running neural_network")