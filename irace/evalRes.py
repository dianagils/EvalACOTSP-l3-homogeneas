import os
import numpy as np
from scipy.stats import kurtosis

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

        mean_deviation = np.mean(values) if values else float('inf')
        return mean_deviation, values
    else:
        return float('inf'), []

def process_directory(directory_path):
    best_mean_deviation = float('inf')
    best_values = []

    for config_folder in os.listdir(directory_path):
        config_path = os.path.join(directory_path, config_folder)
        if os.path.isdir(config_path):
            for file_name in os.listdir(config_path):
                file_path = os.path.join(config_path, file_name)
                file_key = file_name[:-4]
                
                mean_deviation, result = read_result_file(file_path)

                if mean_deviation < best_mean_deviation:
                    best_mean_deviation = mean_deviation
                    best_values = result

    return best_mean_deviation, best_values

directories = ["Dir_S1", "Dir_S2"]

for directory in directories:
    directory_path = os.path.join(os.getcwd(), directory)
    best_mean_deviation, best_values = process_directory(directory_path)

    if best_values:
        mean = np.mean(best_values)
        std_dev = np.std(best_values)
        mini = min(best_values)
        maxi = max(best_values)
        kurtosi = kurtosis(best_values)
        
        print(f'Best Values for {directory}')
        print(f'Mean: {mean}')
        print(f'Std Dev: {std_dev}')
        print(f'Min: {mini}')
        print(f'Max: {maxi}')
        print(f'Kurtosis: {kurtosi}')
    else:
        print(f'No valid results found for {directory}')
