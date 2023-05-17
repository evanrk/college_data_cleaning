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
            multi_college_dfs.append((data_name, idps_data))


    single_college_merged_df = functools.reduce(concat_df, single_college_dfs) # cool

    return single_college_dfs, multi_college_dfs, single_college_merged_df

def drop_with_letter(df, letter="X"):
    columns_to_drop = []
    for index, column in enumerate(df.columns):
        if column[0] == letter:
            columns_to_drop.append(column)

    df = df.drop(columns=columns_to_drop)
    # df.insert(0, "INSTNM", df.pop("INSTNM"))
    df.sort_index()

    return df

def replace_names(merged_df, association_dfs):
    words_merged_df = pd.DataFrame()
    words_merged_df["UNITID"] = merged_df["UNITID"]

    for association_df in association_dfs:
        for index, column in enumerate(merged_df.columns): # for every column name in the columns of merged_df
            # column_stripped = column.replace(" ", "")
            column_stripped = ""
            allowed_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"] # abc's for checking uppercase
            for char in column:
                if char == char.lower() and char in allowed_chars:
                    allowed_chars.append(" ") # adds a space to allowed chars if the title is a sentence (not an acronym which is in all caps)
                
            allowed_chars += ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "_", "(", ")", "/"]
            
            for char in column:
                if char.lower() in allowed_chars:
                    column_stripped += char
                # else:
                    # print(column)
            var_name_df = association_df[association_df["varName"] == column_stripped]
            
            # print(column.replace(" ", "_"), column_stripped)
            title_values = var_name_df["varTitle"].to_numpy()

            if len(title_values): # if the title_value exists:
                title_value = title_values[0].replace("\n", "").replace("\r", "")
                if "Codevalue" in var_name_df: # if there is a value to be decoded:
                    decoded_values = [] # list of the decoded values within every column of every merged_df csv file
                    var_name_df = var_name_df.set_index("Codevalue")

                    for coded_value in merged_df[column_stripped]: # checks for every coded value in the college data csv
                        try:
                            decoded_values.append(var_name_df.loc[str(coded_value).strip()]["valueLabel"]) # checks for regular
                        except KeyError: 
                            try:
                                decoded_values.append(var_name_df.loc["0"+str(coded_value).strip()]["valueLabel"]) # adds leading zero
                            except KeyError: 
                                try:
                                    decoded_values.append(var_name_df.loc[str(coded_value).strip()+"0"]["valueLabel"]) # adds trailing zero
                                except KeyError:
                                    try: 
                                        decoded_values.append(var_name_df.loc[str(coded_value).strip()[:-2]]["valueLabel"]) # checks for extra trailing zero and decimal point
                                    except KeyError:
                                        try:
                                            decoded_values.append(var_name_df.loc["0"+str(coded_value).strip()+"0"]["valueLabel"]) # adds leading and trailing zero
                                        except KeyError:
                                            decoded_values.append(None)
                    print(decoded_values[-1])

                    # print(f"{column}: {title_value}")

                    # merged_df is everything, both words and numbers
                    merged_df[column] = decoded_values
                    # words_merged_df is just words
                    words_merged_df[column] = decoded_values
                merged_df.rename(columns={column: title_value}, inplace=True)
                words_merged_df.rename(columns={column: title_value}, inplace=True)
        
    return merged_df, words_merged_df