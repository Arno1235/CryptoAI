# Neural Network libraries
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout



# Nueral Network class
class NeuralNetwork:

    # Initializes the class
    # n_layers: number of layers
    # n_nodes; number of nodes
    # n_per_learn: numper of periods to learn
    # n_per_predict: number of periods to predict
    # n_features: number of features
    # activation: activation method
    def __init__(self, n_layers, n_nodes, n_per_learn, n_per_predict, n_features, activation="tanh"):
        self.n_layers = n_layers
        self.n_nodes = n_nodes
        self.n_per_learn = n_per_learn
        self.n_per_predict = n_per_predict
        self.n_features = n_features
        self.activation = activation

        self.createNN()
    
    # Creates the Neural Network
    def createNN(self):
        # Instatiating the model
        self.model = Sequential()

        # Input layer
        self.model.add(LSTM(90, 
                    activation=self.activation, 
                    return_sequences=True, 
                    input_shape=(self.n_per_learn, self.n_features)))

        # Hidden layers
        self.layerMaker()

        # Final Hidden layer
        self.model.add(LSTM(60, activation=self.activation))

        # Output layer
        self.model.add(Dense(self.n_per_predict))

        # Model summary
        self.model.summary()

        # Compiling the data with selected specifications
        self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    # Creates a specified number of hidden layers for an RNN
    # Optional: Adds regularization option - the dropout layer to prevent potential overfitting (if necessary)    
    def layerMaker(self, drop=None, d_rate=.5):
        # Creating the specified number of hidden layers with the specified number of nodes
        for x in range(1, self.n_layers+1):
            self.model.add(LSTM(self.n_nodes, activation=self.activation, return_sequences=True))

            # Adds a Dropout layer after every Nth hidden layer (the 'drop' variable)
            try:
                if x % drop == 0:
                    self.model.add(Dropout(d_rate))
            except:
                pass
    
    # Fitting and Training of the Neural Network
    def trainNN(self, input_X, input_Y, epochs = 10, batch_size=128, validation_split=0.1):
        return self.model.fit(input_X, input_Y, epochs=epochs, batch_size=batch_size, validation_split=validation_split)
    
    # Predict Using Neural Network
    def predictionNN(self, input_data):
        # Predicting off of the most recent days from the original DF
        return self.model.predict(input_data)



if __name__ == "__main__":
    print("running neural_network")