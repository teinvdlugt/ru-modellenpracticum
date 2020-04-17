import random

output_file = "./collagen2d.piff"
celltype = "Collagen"
lattice_dim = 200  # width and height of the lattice
no_of_fibres_per_direction = 100  # total number: twice this number (in x and y directions)
fibre_length = 10  # fibre width is taken to be 1 pixel (as in Scianna)

# See https://compucell3dreferencemanual.readthedocs.io/en/latest/pif_initializer.html#pif-initializer
# for PIF file structure:
#    cell# celltype x1 x2 y1 y2 z1 z2

with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) + " 0 0\n")
    # Fibres in x direction
    for cell_id in range(1, no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - fibre_length)
        y = random.randint(0, lattice_dim - 1)
        f.write(" ".join([str(cell_id), celltype, str(x), str(x + fibre_length - 1), str(y), str(y), '0 0\n']))
    # Fibres in y direction
    for cell_id in range(1 + no_of_fibres_per_direction, 2 * no_of_fibres_per_direction + 1):
        # Choose random position
        x = random.randint(0, lattice_dim - 1)
        y = random.randint(0, lattice_dim - fibre_length)
        f.write(" ".join([str(cell_id), celltype, str(x), str(x), str(y), str(y + fibre_length - 1), '0 0\n']))
