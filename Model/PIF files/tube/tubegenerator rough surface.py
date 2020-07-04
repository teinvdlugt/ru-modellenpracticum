import random
from math import sqrt
output_file = "./3d tube rough surface with collagen.piff"
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
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) +" 0 " + str(lattice_dim - 1) + '\n')
    # Fibres in x direction
    for cell_id in range(1, no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - fibre_length)
        y = random.randint(0, lattice_dim - 1)
        z = random.randint(0, lattice_dim - 1)
        f.write(" ".join([str(1), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), str(z), str(z), '\n']))
    # Fibres in y direction
    for cell_id in range(1 + no_of_fibres_per_direction, 2 * no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - 1)
        y = random.randint(0, lattice_dim - fibre_length)
        z = random.randint(0, lattice_dim - 1) 
        f.write(" ".join([str(1), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), str(z), str(z), '\n']))
    # Fibres in z direction
    for cell_id in range(1 + 2 * no_of_fibres_per_direction, 3 * no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - 1)
        y = random.randint(0, lattice_dim - 1)
        z = random.randint(0, lattice_dim - fibre_length) 
        f.write(" ".join([str(1), "Collagen", str(x), str(x), str(y), str(y), str(z), str(z + fibre_length - 1), '\n']))
    
    
    x = tuberadius + 2
    for y in range( 0, tuberadius + 2):
        while (x**2 + y**2 > (tuberadius+1)**2 and x > 0):
            x += -1
            f.write(" ".join([str(0), "Medium", str(-x+tubecent), str(x+tubecent), str(y+tubecent), str(y+tubecent), str(0), str(lattice_dim -1), '\n']))



            
            f.write(" ".join([str(0), "Medium", str(-x+tubecent), str(x+tubecent), str(-y+tubecent), str(-y+tubecent), str(0), str(lattice_dim -1), '\n']))
            print(x,y)
        f.write(" ".join([str(0), "Medium", str(-x+tubecent), str(x+tubecent), str(y+tubecent), str(y+tubecent), str(0), str(lattice_dim -1), '\n']))



            
        f.write(" ".join([str(0), "Medium", str(-x+tubecent), str(x+tubecent), str(-y+tubecent), str(-y+tubecent), str(0), str(lattice_dim -1), '\n']))
        
        
     

        
    cell_count = 1
    for x in range(lattice_dim//2 - cell_width, lattice_dim//2 + cell_width, cell_width):
        for y in range(lattice_dim//2 - cell_width, lattice_dim//2 + cell_width, cell_width):
            for z in range(lattice_dim//2 - height*cell_width//2, lattice_dim//2 + height*cell_width//2, cell_width):
                cell_count += 1
                f.write(" ".join([str(cell_count), "Tumor", str(x), str(x + cell_width - 1),
                                str(y), str(y + cell_width - 1), str(z), str(z + cell_width - 1), '\n'])) 