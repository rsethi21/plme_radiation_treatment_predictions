import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="path to input data folder", required=True)
parser.add_argument("-o", "--output", help="path to output data folder", required=True)

def extract_information(string, n):
    information = string.split(".")
    information = information[1:-1]
    information = [int(data[1:]) if i != 0 else data for i, data in enumerate(information)]
    return np.array([information]*n)

if __name__ == "__main__":
    args = parser.parse_args()
    original_col_names = ["dose_quantity", "cell_number", "u1", "plme", "u2", "u3", "u4"]
    col_names = ["particle_type", "interaction_max_DSB", "dose_rate", "energy_threshold_DSB", "chance_DSB"]
    dataframes_to_concat = []
    for file_name in os.listdir(args.input):
        path = os.path.join(args.input, file_name)
        temp_csv = pd.read_csv(path, names=original_col_names)
        new_data = extract_information(file_name, len(temp_csv))
        for index in range(len(col_names)):
            temp_csv.insert(len(temp_csv.columns), col_names[index], new_data[:,index])
        dataframes_to_concat.append(temp_csv)
    final_df = pd.concat(dataframes_to_concat, axis=0, ignore_index=True)
    final_df.to_csv(os.path.join(args.output, "data.csv"))
