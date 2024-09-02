import os
import json
import plotly.graph_objects as go
import pandas as pd

header = ["algorithm", "localsearch", "alpha","beta", "rho", "ants", "q0", "rasrank", "elitistants", "nnls", "dlb"]
algorithmMap = {"as": 0, "mmas": 1, "eas": 2, "ras": 3, "acs": 4}

def load_configs(folder_path):
    config_data = []
    config_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    for file in config_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as f:
            # load the text file 
            data = f.read()
            values = data.split()
            config_dict = dict(zip(header, values))
            config_dict["algorithm"] = algorithmMap[config_dict["algorithm"]]
            config_data.append(config_dict)

    return config_data


def create_parallel_coordinates_plot(combined_df, output_path, color=None):
    if (color == None):
        color_scale = [[0, 'blue'], [1, 'red']]
    else:
        color_scale = [[0, color], [1, color]]

    print(combined_df)
    fig = go.Figure(data=go.Parcoords(
        line=dict(color=combined_df['Experiment'],
                  colorscale = color_scale,
                ),
        labelfont=dict(size=18),
        rangefont=dict(size=18),
        tickfont=dict(size=18),
        dimensions=list([
            dict(range=[0, 4],
                 label='Algorithm', values=combined_df['algorithm'], ticktext=list(algorithmMap.keys()), tickvals=list(algorithmMap.values())),
            dict(range=[0, 3],
                 label='Local Search', values=combined_df['localsearch']),
            dict(range=[0, 5],
                 label='Alpha', values=combined_df['alpha']),
            dict(range=[0, 10],
                 label='Beta', values=combined_df['beta']),
            dict(range=[0.01, 1],
                 label='Rho', values=combined_df['rho']),
            dict(range=[5, 100],
                 label='Ants', values=combined_df['ants']),
            # dict(range=[0, 1],
            #      label='Q0', values=combined_df['q0']),
            # dict(range=[1, 100],
            #      label='RAS Rank', values=combined_df['rasrank']),
            # dict(range=[1, 750],
            #      label='Elitist Ants', values=combined_df['elitistants']),
            # dict(range=[5, 50],
            #      label='NNLS', values=combined_df['nnls']),
            # dict(range=[0, 1],
            #      label='DLB', values=combined_df['dlb']),
        ])
    ))
    fig.update_layout(
        width=700,
    )
    # Save the plot
    fig.write_image(output_path)


def iterate_through_folders(root_folder):
  solo_path = root_folder + "1"
  path = root_folder + "2"
  nSeeds = 10

  solo_config_data = []
  config_data = []

  for i in range(nSeeds):
    # find folder that ends with s_i
    solo_folder = [f for f in os.listdir(solo_path) if f.endswith("s_" + str(i + 1))]
    folder = [f for f in os.listdir(path) if f.endswith("s_" + str(i + 1))]

    currentSoloData = load_configs(os.path.join(solo_path, solo_folder[0]))
    currentData = load_configs(os.path.join(path, folder[0]))
    ## add to lists
    solo_config_data += currentSoloData
    config_data += currentData
  # create plot for combined  
  solo_total_df = pd.DataFrame(solo_config_data)
  solo_total_df["Experiment"] = 1
  solo_total_df = solo_total_df.replace('NA', 1e10)
  # create plot for normal

  total_df = pd.DataFrame(config_data)
  total_df["Experiment"] = 0
  total_df = total_df.replace('NA', 1e10)
  combined_df = pd.concat([total_df, solo_total_df])
  output_path = os.path.join(path, "parcoords_combined.png")
  create_parallel_coordinates_plot(combined_df, output_path)

        
if __name__ == "__main__":
    folders = ['Subset_']
    for folder in folders:
        iterate_through_folders(folder)
