import os
import re
import numpy as np
from scipy.stats import kurtosis, wilcoxon

def read_result_file(file_path):
    if file_path.endswith(".txt"):
        indices_to_pick = [i for i in range(1, 21)]
        values = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for index in indices_to_pick:
                try:
                    line_value = float(lines[index - 1].strip())
                    values.append(line_value)
                except IndexError:
                    pass
        return values
    else:
        return []

def process_directory(directory_path, all_results):
    directory_results = []
    for config_folder in os.listdir(directory_path):
        config_path = os.path.join(directory_path, config_folder)
        if os.path.isdir(config_path):
            config_name = config_folder 
            for file_name in os.listdir(config_path):
                file_path = os.path.join(config_path, file_name)
                file_name = file_name[:-4]
                result = read_result_file(file_path)
                all_results = all_results + result
    return all_results
directories = ["Dir_S1", "Dir_S2"]
all_results = []
for directory in directories:
    directory_path = os.path.join(os.getcwd(), directory)
    all_results = process_directory(directory_path, all_results)

    values = all_results
    mean = np.mean(values)
    std_dev = np.std(values)
    mini = min(values)
    maxi = max(values)
    kurtosi = kurtosis(values)
    print(f'Values for {directory}')
    print(f'Mean {mean}')
    print(f'Std Dev {std_dev}')
    print(f'Min {mini}')
    print(f'Max {maxi}')
    print(f'Kurtosis {kurtosi}')

    