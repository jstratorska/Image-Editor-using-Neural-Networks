import glob
import pandas as pd
import numpy as np
from .draw_sketches import draw

def find_files(path):
    files = glob.glob(path)
    return files

def read_data(path):
    train_data_files = find_files("\\Data\\json\\" + path + "\\"+ "*") 
    global train_data
    train_data = pd.DataFrame()
    for i in range (len(train_data_files)):
        data = pd.read_json(train_data_files[i])
        data = data[data.recognized==True][["word", "drawing"]]
        train_data = train_data.append(data[:200])
    return train_data

def read_data_one(path, subpath):
    data =  pd.read_json("Data\\json\\" + path + "\\" + subpath + ".json")  
    data = data[data.recognized==True][["word", "drawing"]][:200]
    return data

def to_array(data):
    for i in range(0, len(data['drawing'])):
        data['drawing'].iloc[i]= np.array(data['drawing'].iloc[i]) 
    return data