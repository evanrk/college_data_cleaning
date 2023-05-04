import numpy as np
import pandas as pd

import os
import functools

def concat_df(df1, df2):
    return pd.concat([df1, df2], axis=1)

def clean_data_names(data_filenames):
    return [filename.split('.')[0] for filename in data_filenames]

def combine_csv(directory:str):
    single_college_dfs = []
    multi_college_dfs = []

    data_filenames = os.listdir(directory)

    for index, filename in enumerate(data_filenames): # iterates over every file in the data directory
        idps_data = pd.read_csv(directory+"/"+filename, encoding="ISO-8859-1")
        data_name = filename.split(".")[0]


    # idps_data.drop_duplicates("UNITID")
    
        if not idps_data["UNITID"].duplicated().max(): # True is greater than False, so if theres one True it will skip the file
            idps_data = idps_data.set_index("UNITID")
            single_college_dfs.append(idps_data)
        else:
            multi_college_dfs.append(idps_data)


    single_college_merged_df = functools.reduce(concat_df, single_college_dfs) # cool

    return single_college_dfs, multi_college_dfs, single_college_merged_df

def drop_with_letter(df, letter="X"):
    columns_to_drop = []
    for index, column in enumerate(df.columns):
        if column[0] == "X":
            columns_to_drop.append(column)

    df = df.drop(columns=columns_to_drop)
    # df.insert(0, "INSTNM", df.pop("INSTNM"))
    df.sort_index()

    return df