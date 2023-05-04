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


data_filenames = os.listdir(PATH_TO_IPEDS_DATA)
# # data_filenames = ["adm2021.csv"]

# # data_files_size = 0

# # for filename in data_filenames:
#     # data_files_size += os.path.getsize(PATH_TO_IPEDS_DATA+"/"+filename)

# for index, filename in enumerate(data_filenames): # iterates over every file in the data directory
#     idps_data = pd.read_csv(PATH_TO_IPEDS_DATA+"/"+filename, encoding="ISO-8859-1")
#     data_name = filename.split(".")[0]


#     # idps_data.drop_duplicates("UNITID")
    
#     if not idps_data["UNITID"].duplicated().max(): # True is greater than False, so if theres one True it will skip the file
#         idps_data = idps_data.set_index("UNITID")
#         single_college_dfs.append(idps_data)
#     else:
#         multi_college_dfs.append(idps_data)


# merged_df = functools.reduce(concat, single_college_dfs) # cool

single_college_dfs, multi_college_dfs, merged_df = csv_tools.combine_csv(PATH_TO_IPEDS_DATA)

# columns_to_drop = []
# for index, column in enumerate(merged_df.columns):
#     if column[0] == "X":
#         columns_to_drop.append(column)

# merged_df = merged_df.drop(columns=columns_to_drop)
# merged_df.insert(0, "INSTNM", merged_df.pop("INSTNM"))
# merged_df.sort_index()

# print(merged_df.head())
merged_df = csv_tools.drop_with_letter(merged_df, letter="X")
merged_df.to_csv("./output/single_college_data_variables.csv")
print(merged_df.head())
# print(idps_data.to_dict(orient='index')[100654])

    # for row in idps_data.iloc:
        # college_data = {}
        

# for index, column_title in enumerate(merged_df.columns):
#     column = merged_df.iloc[index]



# for filename in data_filenames: # iterates over every file in the data directory
#     college_data = pd.read_csv(PATH_TO_IPEDS_DATA+"/"+filename, encoding="ISO-8859-1")
#     data_name = filename.split(".")[0]

#     for association_df_name, association_df in variable_meaning_dfs.items(): # gets the association dataframe
#         get_table_name = association_df["TableName"] == data_name.upper()
#         association_df_filename = association_df[get_table_name] # gets the part of the df with this file in it
        
#         for column in college_data.columns: # for every column name in the columns of college_data
#             var_name_df = association_df_filename[association_df_filename["varName"] == column]
#             title_values = var_name_df["varTitle"].to_numpy()
            
#             if len(title_values): # if the title_value exists:
#                 if "Codevalue" in var_name_df: # if there is a value to be decoded:
#                     decoded_values = [] # list of the decoded values within every column of every college_data csv file
#                     var_name_df = var_name_df.set_index("Codevalue")
                    
#                     for coded_value in college_data[column]: # checks for every coded value in the college data csv
#                         try:
#                             decoded_values.append(var_name_df.loc[str(coded_value).strip()]["valueLabel"]) # checks for regular
#                         except KeyError: 
#                             try:
#                                 decoded_values.append(var_name_df.loc["0"+str(coded_value).strip()]["valueLabel"]) # adds leading zero
#                             except KeyError: 
#                                 try:
#                                     decoded_values.append(var_name_df.loc[str(coded_value).strip()+"0"]["valueLabel"]) # adds trailing zero
#                                 except KeyError:
#                                     try: 
#                                         decoded_values.append(var_name_df.loc[str(coded_value).strip()[:-2]]["valueLabel"]) # checks for extra trailing zero and decimal point
#                                     except KeyError:
#                                         try:
#                                             decoded_values.append(var_name_df.loc["0"+str(coded_value).strip()+"0"]["valueLabel"]) # adds leading and trailing zero
#                                         except KeyError:
#                                             decoded_values.append(None)
#                     # lol
                                    
#                     print(decoded_values)
#     print(college_data.shape)
# print("100%")