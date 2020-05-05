# Making necessary imports
import pandas as pd
import os

# Dealing with confirmed, recovery and death files
files = ['confirmed.csv' , 'death.csv', 'recovery.csv']

# Writing a function for data preprocessing
def states_merge(fname):
    base_path = "C:\\Users\\usama\\OneDrive\\Desktop\\github\\COVID19-visualization\\dataset\\"
    file_path = os.path.join(base_path, fname)
    datafr = pd.read_csv(file_path)
    # find unique values in Country/Region column
    unique = datafr['Country/Region'].unique()
    # Declare empty new_dict array
    new_dict = []
    # Sum the states total and add an country row
    for country in unique:
        c_data = datafr[datafr['Country/Region'] == country].sum(axis=0)
        new_dict.append(c_data)
        
    dataset = pd.DataFrame(new_dict)
    dataset = dataset.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis = 1)
    unique = pd.DataFrame(unique)
    d = pd.concat([unique, dataset], axis = 1)
    
    # output path
    output_path = "C:\\Users\\usama\\OneDrive\\Desktop\\github\\COVID19-visualization\\outputs\\"
    save = os.path.join(output_path, fname)
    d.to_csv(save, index = False)

for file in files:
    states_merge(file)