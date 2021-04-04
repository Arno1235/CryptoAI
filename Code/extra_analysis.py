import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ta
from datetime import timedelta
plt.style.use("bmh")


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


if __name__ == "__main__":
    print("running extra_analysis")