import numpy as np
import matplotlib.pyplot as plt
import os
try:
     from mayavi import mlab
except ImportError:
     print ("Warning: \'Mayavi\' module not found. Do not try to plot 3D chemical fields!")

###### OPTIONS ######

lattice_dim = [200,200,200] # [x,y,z]. If you're visualising a 2D field, set z=1.
lowest_coord = [0,0,0] # [x,y,z]. If x runs from 40 to 110, then change x in lattice_dim to 70 and in
                       # lowest_coord to 40
cell_types = ["Medium","Collagen","Tumor"]
contour_toggle_3d = False # Set True if you want a contour map.

#####################

highest_coord = [sum(x) for x in zip(lattice_dim, lowest_coord)]
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
                 data_array[int(line_data[1])-lowest_coord[1],int(line_data[0])-lowest_coord[0]]=float((line_data[3])[:-1])
                 
             plt.imshow(data_array,origin="lower")
             plt.colorbar(orientation='vertical')
             f.close()
             plt.title(filename)
             plt.xlabel("x")
             plt.ylabel("y")
             plt.show()
         else:
             data_array = np.zeros((lattice_dim[0],lattice_dim[1],lattice_dim[2]))
             for line in lines:
                 line_data = line.split(",")
                 data_array[int(line_data[0])-lowest_coord[0],int(line_data[1])-lowest_coord[1],int(line_data[2])-lowest_coord[2]]=float((line_data[3])[:-1])

             if not contour_toggle_3d:
                 grid = mlab.pipeline.scalar_field(data_array)
                 vol = mlab.pipeline.volume(grid,vmin=1e-06)

                 # Change the opacity to something more reasonable
                 
                 try:
                      from tvtk.util.ctf import PiecewiseFunction
                 except ImportError:
                      continue

                 otf = PiecewiseFunction()
                 otf.add_point(0.0, 0.0)
                 otf.add_point(0.315,0.3)
                 vol._otf = otf
                 vol._volume_property.set_scalar_opacity(otf)
             else:
                 mlab.contour3d(data_array,extent=[lowest_coord[0],highest_coord[0],lowest_coord[1],highest_coord[1],lowest_coord[2],highest_coord[2]])
             
             
             mlab.axes()
             mlab.title(filename,size=1,opacity=0.8)
             mlab.colorbar(orientation="vertical")
             mlab.show()
         
         continue
     else:
         continue
