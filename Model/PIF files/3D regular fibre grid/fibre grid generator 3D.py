import random
from math import sqrt
output_file = "./3d regularcollagen16.piff"
lattice_dim = 200  # width and height of the lattice
grid_size = 16

x_sizez = grid_size
y_sizez = grid_size

y_sizex = grid_size
z_sizex = grid_size

z_sizey = grid_size
x_sizey = grid_size

cell_width = 8
n = 5
cluster_radius = int(n/2*cell_width)


with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) +" 0 " + str(lattice_dim - 1) + '\n')
    cell_count = 0
    # Fibres in z direction
    for x in range(0, lattice_dim, x_sizez):
        for y in range(0, lattice_dim, y_sizez):
            cell_count += 1
            f.write(" ".join([str(cell_count), "Collagen", str(x), str(x), str(y), str(y), str(0), str(lattice_dim-1), '\n']))
    # Fibres in x direction
    for y in range(0, lattice_dim, y_sizex):
        for z in range(0, lattice_dim, z_sizex):
            cell_count += 1
            f.write(" ".join([str(cell_count), "Collagen", str(0), str(lattice_dim-1), str(y), str(y), str(z), str(z), '\n']))
    # Fibres in y direction
    for z in range(0, lattice_dim, z_sizey):
        for x in range(0, lattice_dim, x_sizey):
            cell_count += 1
            f.write(" ".join([str(cell_count), "Collagen", str(x), str(x), str(0), str(lattice_dim-1), str(z), str(z), '\n']))
        
        
    for x in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
        for y in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
            for z in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
                # Calculate center of mass
                com_x = x + cell_width / 2.
                com_y = y + cell_width / 2.
                com_z = z + cell_width //2
                # Check if COM is within cluster radius
                if sqrt((com_x - lattice_dim//2) ** 2 + (com_y - lattice_dim//2) ** 2 + (com_y - lattice_dim//2)**2) > cluster_radius:
                    continue
    
                # If within cluster radius, add cell to PIF file
                # format:  cell# celltype x1 x2 y1 y2 z1 z2
                cell_count += 1
                f.write(" ".join([str(cell_count), "Tumor", str(x), str(x + cell_width - 1),
                                str(y), str(y + cell_width - 1), str(z), str(z + cell_width - 1), '\n']))   
                                
