import os
import numpy as np
import pandas as pd

def load_data():
    '''
            gender   age   income  goal  career  dec  attr  sinc  intel  fun  amb  shar  like  prob  met
        0        0  21.0  69487.0   2.0  lawyer    1   6.0   9.0    7.0  7.0  6.0   5.0   7.0   6.0  2.0
        1        0  21.0  69487.0   2.0  lawyer    1   7.0   8.0    7.0  8.0  5.0   6.0   7.0   5.0  1.0
        2        0  21.0  69487.0   2.0  lawyer    1   5.0   8.0    9.0  8.0  5.0   7.0   7.0   NaN  1.0
        3        0  21.0  69487.0   2.0  lawyer    1   7.0   6.0    8.0  7.0  6.0   8.0   7.0   6.0  2.0
        4        0  21.0  69487.0   2.0  lawyer    1   5.0   6.0    7.0  7.0  6.0   6.0   6.0   6.0  2.0
    '''
    
    path = os.path.join("./data/speed_data_data.csv")
    raw_data = pd.read_csv(path)
    print("Raw data loading finished. Including %d records." % raw_data.shape[0])
    return raw_data


def truncate_nan(data: pd.DataFrame):
    data.dropna()
    return data
    

def aggregate(data: pd.DataFrame):
    pass


# And so on...
    

if __name__ == '__main__':
    
    data = load_data()
    import pdb; pdb.set_trace()