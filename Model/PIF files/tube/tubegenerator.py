import random
from math import sqrt
output_file = "./3d tube only smooth surface.piff"
lattice_dim = 200  # width and height of the lattice
no_of_fibres_per_direction = 10000  # total number: twice this number (in x and y directions)
fibre_ratio = 3
fibre_length = 30  # fibre width is taken to be 1 pixel (as in Scianna)
cell_width = 8
n = 2
cluster_radius = int(n/2*cell_width)
cell_count = 1
reltubewidth = 3 #width of the tube relative to cell size
tuberadius = cell_width * reltubewidth //2
tubecent = 100
height = 4

with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim-1) + '\n')
    

                                
                                
    x = tuberadius + 2
    for y in range( 0, tuberadius + 2):
        while (x**2 + y**2 > (tuberadius+1)**2 and x > 0):
            x += -1
            f.write(" ".join([str(1), "Collagen", str(x+tubecent), str(x+tubecent+1), str(y+tubecent), str(y+tubecent), str(0), str(lattice_dim -1), '\n']))

            f.write(" ".join([str(1), "Collagen", str(-x+tubecent-1), str(-x+tubecent), str(y+tubecent), str(y+tubecent), str(0), str(lattice_dim -1), '\n']))

            
            f.write(" ".join([str(1), "Collagen", str(x+tubecent), str(x+tubecent+1), str(-y+tubecent), str(-y+tubecent), str(0), str(lattice_dim -1), '\n']))

            
            f.write(" ".join([str(1), "Collagen", str(-x+tubecent-1), str(-x+tubecent), str(-y+tubecent), str(-y+tubecent), str(0), str(lattice_dim -1), '\n']))
            print(x,y)
        f.write(" ".join([str(1), "Collagen", str(x+tubecent), str(x+tubecent+1), str(y+tubecent), str(y+tubecent), str(0), str(lattice_dim -1), '\n']))

        
        f.write(" ".join([str(1), "Collagen", str(-x+tubecent-1), str(-x+tubecent), str(y+tubecent), str(y+tubecent), str(0), str(lattice_dim -1), '\n']))

        
        f.write(" ".join([str(1), "Collagen", str(x+tubecent), str(x+tubecent+1), str(-y+tubecent), str(-y+tubecent), str(0), str(lattice_dim -1), '\n']))

        
        f.write(" ".join([str(1), "Collagen", str(-x+tubecent-1), str(-x+tubecent), str(-y+tubecent), str(-y+tubecent), str(0), str(lattice_dim -1), '\n']))
        
        
    cell_count = 1
    for x in range(lattice_dim//2 - cell_width, lattice_dim//2 + cell_width, cell_width):
        for y in range(lattice_dim//2 - cell_width, lattice_dim//2 + cell_width, cell_width):
            for z in range(lattice_dim//2 - height*cell_width//2, lattice_dim//2 + height*cell_width//2, cell_width):
                cell_count += 1
                f.write(" ".join([str(cell_count), "Tumor", str(x), str(x + cell_width - 1),
                                str(y), str(y + cell_width - 1), str(z), str(z + cell_width - 1), '\n']))  