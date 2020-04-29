from math import sqrt

cluster_radius = 24
cluster_center = 100
cell_width = 8  # cell_width x cell_width pixels per cell
file_input = './tumoroids.piff'
file_output = './tumoroid2d.piff'

with open("Simulation/PressureDemonstration.piff", 'w') as f:
    # Draw medium
    f.write("0 Medium 0 49 0 49 0 0\n")

    # Draw wall
    f.write("1 Wall 15 15 5 45 0 0\n")
    f.write("1 Wall 15 35 5 5 0 0\n")
    f.write("1 Wall 35 35 5 45 0 0\n")

    lower_volume = 0
    upper_volume = 0

    # Draw lower cell
    for x in range(50):
        for y in range(50):
            if ((x - 25) / 2) ** 2 + (y - 11) ** 2 < 17:
                f.write("2 Lower %d %d %d %d 0 0\n" % (x, x, y, y))
                lower_volume += 1

    # Draw upper cell
    for x in range(50):
        for y in range(50):
            if ((x - 25)/1.6) ** 2 + ((y - 25)/1.6) ** 2 < 32:
                f.write("3 Upper %d %d %d %d 0 0\n" % (x, x, y, y))
                upper_volume += 1

    print(lower_volume, upper_volume)

    #
    #
    #
    # for x in range(cluster_center - cluster_radius, cluster_center + cluster_radius - cell_width, cell_width):
    #     for y in range(cluster_center - cluster_radius, cluster_center + cluster_radius - cell_width, cell_width):
    #         # Calculate center of mass
    #         com_x = x + cell_width / 2
    #         com_y = y + cell_width / 2
    #         # Check if COM is within cluster radius
    #         if sqrt((com_x - cluster_center) ** 2 + (com_y - cluster_center) ** 2) > cluster_radius:
    #             continue
    #
    #         # If within cluster radius, add cell to PIF file
    #         # format:  cell# celltype x1 x2 y1 y2 z1 z2
    #         cell_count += 1
    #         f.write(" ".join([str(last_cell_id + cell_count), "Tumor", str(x), str(x + cell_width - 1),
    #                           str(y), str(y + cell_width - 1), '0 0\n']))
