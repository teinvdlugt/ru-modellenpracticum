output_file = "./collagen3d.piff"
lattice_dim = 200  # no of lattice sites in each direction
lower_bound = 40  # Draw collagen from lower_bound to upper_bound in each direction (both inclusive)
upper_bound = 160
pore_size = 4

# See https://compucell3dreferencemanual.readthedocs.io/en/latest/pif_initializer.html#pif-initializer
# for PIF file structure:
#    cell# celltype x1 x2 y1 y2 z1 z2

with open(output_file, 'w') as f:
    # First fill with Medium
    f.write(" ".join(["0 Medium 0", str(lattice_dim - 1), "0", str(lattice_dim - 1), "0", str(lattice_dim - 1), "\n"]))

    cell_id = 0
    # Fibres in x direction
    for y in range(lower_bound, upper_bound + 1, pore_size):
        for z in range(lower_bound, upper_bound + 1, pore_size):
            cell_id += 1
            f.write(" ".join([str(cell_id), "Collagen", str(lower_bound), str(upper_bound),
                              str(y), str(y), str(z), str(z), "\n"]))
    # Fibres in y direction
    for x in range(lower_bound, upper_bound + 1, pore_size):
        for z in range(lower_bound, upper_bound + 1, pore_size):
            cell_id += 1
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(lower_bound), str(upper_bound),
                              str(z), str(z), "\n"]))
    # Fibres in z direction
    for x in range(lower_bound, upper_bound + 1, pore_size):
        for y in range(lower_bound, upper_bound + 1, pore_size):
            cell_id += 1
            f.write(" ".join([str(cell_id), "Collagen", str(x), str(x), str(y), str(y),
                              str(lower_bound), str(upper_bound), "\n"]))
