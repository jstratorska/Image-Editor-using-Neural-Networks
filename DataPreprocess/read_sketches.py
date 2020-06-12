from PIL import Image
import numpy as np
import pandas as pd
from .read_data import find_files

def read_sketch_data(path):
    train_data = pd.DataFrame()
    images = find_files("Data\\sketches\\" + path + "\\*\\*")
    
    for i in range (len(images)):
        image = Image.open(images[i])
        data = np.array(image)
        train_data = train_data.append(pd.DataFrame((data[:,:,0]/255).reshape(1, -1)))
    return train_data.T, len(images)