# Adds tumor cells in a disk shape to an existing PIF file

from math import sqrt
import shutil

cluster_radius = 24
cluster_center = 100
cell_width = 8  # cell_width x cell_width pixels per cell
file_input = './tumoroids.piff'
file_output = './tumoroid2d.piff'

# Copy collagen file
shutil.copyfile(file_input, file_output)

with open(file_input, 'r') as f:
    last_cell_id = int(f.readlines()[-1].split(" ")[0])

with open(file_output, 'a+') as f:
    cell_count = 0

    for x in range(cluster_center - cluster_radius, cluster_center + cluster_radius - cell_width, cell_width):
        for y in range(cluster_center - cluster_radius, cluster_center + cluster_radius - cell_width, cell_width):
            # Calculate center of mass
            com_x = x + cell_width / 2
            com_y = y + cell_width / 2
            # Check if COM is within cluster radius
            if sqrt((com_x - cluster_center) ** 2 + (com_y - cluster_center) ** 2) > cluster_radius:
                continue

            # If within cluster radius, add cell to PIF file
            # format:  cell# celltype x1 x2 y1 y2 z1 z2
            cell_count += 1
            f.write(" ".join([str(last_cell_id + cell_count), "Tumor", str(x), str(x + cell_width - 1),
                              str(y), str(y + cell_width - 1), '0 0\n']))

print("Number of cells added:", cell_count)