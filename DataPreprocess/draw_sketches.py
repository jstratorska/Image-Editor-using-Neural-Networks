from matplotlib import pyplot as plt
import pandas as pd

def draw(data, path, subpath):
    for i in range(len(data)):
        t = plt.figure(figsize=(1,1))
        for j in range(0, len(data['drawing'].iloc[i])):
            plt.axis('off')
            plt.plot(data['drawing'].iloc[i][j][0], data['drawing'].iloc[i][j][1],linewidth=2, color='black')
        
        new_path = "Data\\sketches\\" + path + "\\" + subpath + "\\" + subpath + str(i)  + ".png"
        t.savefig(new_path)
        plt.close(t)