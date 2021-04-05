import numpy as np

"""
Splits the multivariate time sequence
"""
def split_sequence(seq, n_steps_in, n_steps_out):

    # Creating a list for both variables
    input_X, input_Y = [], []
    
    for i in range(len(seq)):
        
        # Finding the end of the current sequence
        end = i + n_steps_in
        out_end = end + n_steps_out
        
        # Breaking out of the loop if we have exceeded the dataset's length
        if out_end > len(seq):
            break
        
        # Splitting the sequences into: x = past prices and indicators, y = prices ahead
        seq_x, seq_y = seq[i:end, :], seq[end:out_end, 0]
        
        input_X.append(seq_x)
        input_Y.append(seq_y)
    
    return np.array(input_X), np.array(input_Y)


if __name__ == "__main__":
    print("running load_data")