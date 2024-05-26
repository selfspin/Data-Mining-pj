import os
import json
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


def combine_career(data: pd.DataFrame, json_path="../data/career.json"):
    
    with open(json_path, "r", encoding="utf-8") as f:
        career = json.load(f)
        career_category = career.keys()
    
    def categorize(career_str):
        for category in career_category:
            if career_str in career[category]:
                return category
        import pdb; pdb.set_trace()
        raise NotImplementedError 
    
    # Naive loop.
    row_n = data.shape[0]
    for idx in range(row_n):
        if data.loc[idx]["career"] is np.nan:
            data.loc[idx]["career"] = "nan"
        else:
            data.iloc[idx, 4] = categorize(data.loc[idx]["career"])
    
    return data


def partial_by_income(data: pd.DataFrame):
    '''
    Divide the data into two groups by whether one has the income.
    The "income" attr of individuals who do not have income will be set to 0.
    '''
    no_income_data = data[data["income"].isna()]
    no_income_data = no_income_data.fillna(value={"income": 0.})
    income_data = data[~data["income"].isna()]
    return no_income_data, income_data


def truncate_nan(data: pd.DataFrame):
    raw_n_rows = data.shape[0]
    data = data.dropna().reset_index(drop=True)
    new_n_rows = data.shape[0]
    print("Have truncated nan. nrows %d -> %d" %(raw_n_rows, new_n_rows))
    return data
    

def aggregate(data: pd.DataFrame):
    '''
    Aggregate records by the first 5 columns.
    The other attrs will be set to the mean.
    '''
    def match(row1, row2):
        return (row1[:5] == row2[:5]).sum() == 5

    def stack(row_list):
        _row_list = [row[6:12] for row in row_list]
        _df = pd.DataFrame(_row_list)
        _df = _df.mean(axis=0)
        _head_df = row_list[0][:5]
        _df = pd.concat([_head_df, _df], axis=0)
        return _df
    
    # Naive O(n^2) approach.
    new_data = []
    temp_data = []
    row_n = data.shape[0]
    
    temp_row = data.loc[0]
    for idx in range(row_n):
        
        cur_row = data.loc[idx]
        if match(temp_row, cur_row):
            temp_data.append(cur_row.copy())
        else:
            new_data.append(stack(temp_data))
            temp_data = [cur_row.copy()]
            
        temp_row = data.loc[idx]
        
    return pd.DataFrame(new_data)
        
# And so on...
    

if __name__ == '__main__':
    
    # 1. Load the raw data.
    data = load_data()
    data = combine_career(data, json_path="./data/career.json")
    # 2. Divide the data into two parts: with income and w/o income.
    no_income_data, income_data = partial_by_income(data)
    # 3. Drop the na records.
    no_income_data, income_data = truncate_nan(no_income_data), truncate_nan(income_data)
    # 4. Aggregate the data.
    aggr_no_income_data, aggr_income_data = aggregate(no_income_data), aggregate(income_data)
    import pdb; pdb.set_trace()