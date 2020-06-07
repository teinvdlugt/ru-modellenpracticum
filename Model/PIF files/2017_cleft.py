import random
from math import sqrt
output_file = "./2d cleft similar to 2017.piff"
lattice_dim = 400  # width and height of the lattice
no_of_fibres_per_direction = 1800  # total number: twice this number (in x and y directions)
fibre_ratio = 2
fibre_length = 10  # fibre width is taken to be 1 pixel (as in Scianna)
cell_width = 8
n = 9
cluster_radius = int(n/2*cell_width)
cell_count = no_of_fibres_per_direction*2+1

# See https://compucell3dreferencemanual.readthedocs.io/en/latest/pif_initializer.html#pif-initializer
# for PIF file structure:
#    cell# celltype x1 x2 y1 y2 z1 z2

with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) + " 0 0\n")
    # Fibres in x direction, first half
    for cell_id in range(1, int(no_of_fibres_per_direction*(1/(fibre_ratio+1))) + 1):
        # Choose random position
        x = random.randint(0, lattice_dim//2 - fibre_length)
        y = random.randint(0, lattice_dim - 1)
        f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), '0 0\n']))
        
    # Fibres in x direction second half
    for cell_id in range(int((1/(fibre_ratio+1))*no_of_fibres_per_direction)+1, no_of_fibres_per_direction+ 1):
        # Choose random position
        x = random.randint(lattice_dim//2, lattice_dim - fibre_length)
        y = random.randint(0, lattice_dim - 1)
        f.write(" ".join([str(cell_id), "Collagen", str(x), str(x + fibre_length - 1), str(y), str(y), '0 0\n']))
        
    # Fibres in y direction
    for cell_id in range(1 + no_of_fibres_per_direction, int((1+1/(fibre_ratio+1)) * no_of_fibres_per_direction) + 1):
        # Choose random position
        x = random.randint(0, lattice_dim//2 - 1)
        y = random.randint(0, lattice_dim - fibre_length)
        f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), '0 0\n']))

    # Fibres in y direction
    for cell_id in range(int((1+1/(fibre_ratio+1)) * no_of_fibres_per_direction) + 1,no_of_fibres_per_direction*2+1 ):
        # Choose random position
        x = random.randint(lattice_dim/2, lattice_dim - 1)
        y = random.randint(0, lattice_dim - fibre_length)
        f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y + fibre_length - 1), '0 0\n']))
        
    f.write(" ".join([str(0), "Medium", str(lattice_dim//2-3), str(lattice_dim//2+3), str(0), str(lattice_dim - 1), '0 0\n']))
        
    for x in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
        for y in range(lattice_dim//2 - cluster_radius, lattice_dim//2 + cluster_radius - cell_width, cell_width):
            # Calculate center of mass
            com_x = x + cell_width / 2.
            com_y = y + cell_width / 2.
            # Check if COM is within cluster radius
            if sqrt((com_x - lattice_dim//2) ** 2 + (com_y - lattice_dim//2) ** 2) > cluster_radius:
                continue

            # If within cluster radius, add cell to PIF file
            # format:  cell# celltype x1 x2 y1 y2 z1 z2
            cell_count += 1
            f.write(" ".join([str(cell_count), "Tumor", str(x), str(x + cell_width - 1),
                              str(y), str(y + cell_width - 1), '0 0\n']))    