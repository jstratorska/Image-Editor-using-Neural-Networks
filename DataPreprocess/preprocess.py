import numpy as np
import glob

def find_files(path):
    files = glob.glob(path)
    return files

#  Transforms the ndjson file contents into valid json format and splits the data into train and test
def to_json_file(path):

    files = find_files("Data\\ndjson\\" + path + ".ndjson")
    # files[i][15:-6]
    for i in range(len(files)):
        fileRead = open (files[i], "r")
        fileWriteTrain = open("Data\\json\\train\\" + path + ".json", "w+")
        fileWriteTest = open("Data\\json\\test\\" + path + ".json", "w+")

        if fileRead.mode == "r":
            lines = fileRead.readlines()
            fileWriteTrain.write("[\n")
            fileWriteTest.write("[\n")

            i = 1            
            for line in lines:        
                i += 1
                # Every fourth sketch is used for the test
                if i % 4 == 0:
                    if i != len(lines) + 1:
                        fileWriteTest.write(line[:-1] + ",\n")
                    else:
                        fileWriteTest.write(line[:-1] + "]")
                        fileWriteTrain.write(line[:-1] + "]") 

                else:
                    if i != len(lines) + 1:
                        fileWriteTrain.write(line[:-1] + ",\n")
                    else:
                        fileWriteTrain.write(line[:-1] + "]") 
                        fileWriteTest.write(line[:-1] + "]")  

        fileRead.close()
        fileWriteTrain.close()
        fileWriteTest.close()