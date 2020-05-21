import numpy as np
import matplotlib.pyplot as plt
import os

# Currently only works for 2D!

lattice_dim = [200,200,1] # [x,y,z]
cell_types = ["Medium","Collagen","Tumor"]

path = os.getcwd()
directory = os.fsencode(path+"\Model\Simulation\Fields_output")

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".csv"): 
         f = open(os.path.join(directory, file),"r")
         lines = f.readlines()
         
         if lattice_dim[2] == 1:
             data_array = np.zeros((lattice_dim[1],lattice_dim[0]))
             for line in lines:
                 line_data = line.split(",")
                 data_array[int(line_data[1]),int(line_data[0])]=float((line_data[3])[:-2])
         f.close()
         plt.imshow(data_array,origin="lower")
         plt.colorbar(orientation='vertical')
         plt.title(filename)
         plt.xlabel("x")
         plt.ylabel("y")
         plt.show()
         continue
     else:
         continue
