import numpy as np
import matplotlib.pyplot as plt
import os
import zlib
try:
     from mayavi import mlab
except ImportError:
     print ("Warning: \'Mayavi\' module not found. Do not try to plot 3D chemical fields!")

###### OPTIONS ######

lattice_dim = [200,200,200] # [x,y,z]. If you're visualising a 2D field, set z=1.
lowest_coord = [0,0,0] # [x,y,z]. If x runs from 40 to 110, then change x in lattice_dim to 70 and in
                       # lowest_coord to 40
fields = ["MMP","Migration factor","CTP"]
contour_toggle_3d = False # Set True if you want a contour map.

output_frequency = 10
compression_save_frequency = 100

#####################

highest_coord = [sum(x) for x in zip(lattice_dim, lowest_coord)]
path = os.getcwd()
directory = path+"\Model\Simulation\Fields_output"
files = sorted(os.listdir(directory))
item_number = np.prod(lattice_dim)

for field in fields:
     relevant_files = [x for x in files if field in x ]
     uncompressed_files = [x for x in relevant_files if x.endswith("unc.txt")]
     compressed_files = sorted(list(set(relevant_files)-set(uncompressed_files)))
     data_array = np.empty((0,lattice_dim[0],lattice_dim[1],lattice_dim[2]),dtype="float32")
     
     for file in compressed_files:
         f = open(os.path.join(directory, file),"rb")
         raw_data = zlib.decompress(f.read())
         for i in range(0,compression_save_frequency//output_frequency):
              data_array = np.append(data_array,[np.frombuffer(raw_data,dtype="float16",count=item_number,offset=i*2*item_number).reshape(tuple(lattice_dim)).astype("float32")],axis=0)
         f.close()

     for file in uncompressed_files:
         f = open(os.path.join(directory, file),"rb")
         data_array = np.append(data_array,[np.fromfile(f,dtype="float16").reshape(tuple(lattice_dim)).astype("float32")],axis=0)

     for index,data in enumerate(data_array):
         
         if lattice_dim[2] == 1:
             data = data.squeeze()
             plt.imshow(data.T,origin="lower")
             plt.colorbar(orientation='vertical')
             plt.title(" ".join([field,"mcs = %d" % (index*output_frequency)]))
             plt.xlabel("x")
             plt.ylabel("y")
             plt.show()
         else:
             if not contour_toggle_3d:
                 grid = mlab.pipeline.scalar_field(data)
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
                 mlab.contour3d(data,extent=[lowest_coord[0],highest_coord[0],lowest_coord[1],highest_coord[1],lowest_coord[2],highest_coord[2]])
             
             mlab.axes()
             mlab.title(" ".join([field,"mcs = %d" % (index*output_frequency)]),size=1,opacity=0.8)
             mlab.colorbar(orientation="vertical")
             mlab.show()
         
         continue
     else:
         continue
