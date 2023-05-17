import numpy as np
import pandas as pd

import os
import functools

import csv_tools

class Table:
    def __init__(self, name, title, description, release_type, date_released, dataframe):
        self.name = name
        self.title = title
        self.description = description
        self.dataframe = dataframe
        self.release_type = release_type
        self.date_released = date_released

def concat(df1, df2):
    return pd.concat([df1, df2], axis=1)

# # hd2021.csv
# data = pd.read_csv("./all_data/IPEDS_data_2021-2022/data/hd2021.csv", encoding="ISO-8859-1")

# unit_id_college = data[["UNITID", "INSTNM"]] # the id of every college connected with the college

# data = data.set_index("UNITID")

# sheets["HD2021"] = data

# hd_2021_columns = list(data.columns)

# print(hd_2021_columns)
single_college_dfs = []
multi_college_dfs = []
variable_meaning_dfs = {}

PATH_TO_IPEDS_DATA = "./all_data/IPEDS_data_2021-2022/data"
PATH_TO_IPEDS_VARIABLES = "./all_data/IPEDS_data_2021-2022/variables"

variable_filenames = os.listdir(PATH_TO_IPEDS_VARIABLES)
for filename in variable_filenames:
    if filename[0] != ".":
        csv_data = pd.read_csv(PATH_TO_IPEDS_VARIABLES+"/"+filename)
        data_name = filename.split(".")[0]
        variable_meaning_dfs[data_name] = csv_data


single_college_dfs, multi_college_dfs, merged_df = csv_tools.combine_csv(PATH_TO_IPEDS_DATA)


# sal2021_is = pd.read_csv(PATH_TO_IPEDS_DATA+"/sal2021_is.csv")
# s2021_sis = pd.read_csv(PATH_TO_IPEDS_DATA+"/s2021_sis.csv")

# sal2021_is.set_index(["UNITID", sal2021_is.columns[1]])
# s2021_sis.set_index(["UNITID", s2021_sis.columns[1]])
print(len(multi_college_dfs))

edited_dfs = []
words_edited_dfs = []

for name, multi_college_df in multi_college_dfs:
    
    edited_df = csv_tools.drop_with_letter(multi_college_df.head(100))
    # print(edited_df["OMCHRT"])
    edited_df.set_index("UNITID")
    
    edited_df, words_edited_df = csv_tools.replace_names(edited_df, [variable_meaning_dfs["valuesets21"], variable_meaning_dfs["vartable21"]])

    words_edited_df.to_csv(f"./output/converted_words/{name}.csv")

# multi_college_df.to_csv("./output/multi_college_data_variables.csv")

# merged_df = pd.read_csv("./output/single_college_data_variables.csv", low_memory=False)

# words_merged_df = pd.DataFrame()

# merged_df, words_merged_df = csv_tools.replace_names(merged_df, variable_meaning_dfs["valuesets21"])
# merged_df, words_merged_df_p2 = csv_tools.replace_names(merged_df, variable_meaning_dfs["vartable21"])
# words_merged_df = pd.concat([words_merged_df, words_merged_df_p2])

# for column in list(words_merged_df.columns):
#     merged_df.drop(column)

# merged_df.to_csv("./output/numbers_single_college_data.csv")