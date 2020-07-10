import random
from math import ceil
output_file = "./3d new cleft.piff"
lattice_dim = 200  # width and height of the lattice

grid_size1 = 2

x_sizez1 = grid_size1
y_sizez1 = grid_size1

y_sizex1 = grid_size1
z_sizex1 = grid_size1

z_sizey1 = grid_size1
x_sizey1 = grid_size1

grid_size2 = 3

x_sizez2 = grid_size2
y_sizez2 = grid_size2

y_sizex2 = grid_size2
z_sizex2 = grid_size2

z_sizey2 = grid_size2
x_sizey2 = grid_size2


cleft_width = 10
cell_width = 8
tumor_ny = 5
tumor_nz = 5
tumor_nx = 5      #ceil(cleft_width/cell_width) #to ensure the cells completely fill up the cleft 



with open(output_file, 'w') as f:
    # First fill with Medium
    f.write("0 Medium 0 " + str(lattice_dim - 1) + " 0 " + str(lattice_dim - 1) +" 0 " + str(lattice_dim - 1) + '\n')
    # Fibres in z direction
    for x in range(0, lattice_dim//2-cleft_width//2, x_sizez1):
        for y in range(0, lattice_dim, y_sizez1):
            f.write(" ".join([str(1), "Collagen", str(x), str(x), str(y), str(y), str(0), str(lattice_dim-1), '\n']))
    # Fibres in z direction
    for x in range(lattice_dim//2+cleft_width//2, lattice_dim - 1, x_sizez2):
        for y in range(0, lattice_dim, y_sizez2):
            f.write(" ".join([str(1), "Collagen", str(x), str(x), str(y), str(y), str(0), str(lattice_dim-1), '\n']))
    # Fibres in x direction first half
    for y in range(0, lattice_dim, y_sizex1):
        for z in range(0, lattice_dim, z_sizex1):
            f.write(" ".join([str(1), "Collagen", str(0), str(lattice_dim//2 - cleft_width//2 - 1), str(y), str(y), str(z), str(z), '\n']))
    
    # Fibres in x direction second
    for y in range(0, lattice_dim, y_sizex2):
        for z in range(0, lattice_dim, z_sizex2):
            f.write(" ".join([str(1), "Collagen", str(lattice_dim//2 + cleft_width//2), str(lattice_dim - 1), str(y), str(y), str(z), str(z), '\n']))
            
            
    # Fibres in y direction, first half
    for z in range(0, lattice_dim, z_sizey1):
        for x in range(0, lattice_dim//2 - cleft_width//2, x_sizey1):
            f.write(" ".join([str(1), "Collagen", str(x), str(x), str(0), str(lattice_dim-1), str(z), str(z), '\n']))
            
    # Fibres in y direction, second half
    for z in range(0, lattice_dim, z_sizey2):
        for x in range(lattice_dim//2 + cleft_width//2, lattice_dim -1, x_sizey2):
            f.write(" ".join([str(1), "Collagen", str(x), str(x), str(0), str(lattice_dim-1), str(z), str(z), '\n']))       

    # tumorcells
    cell_count = 1
    tumor_widthx = tumor_nx * cell_width #to ensure the cells completely fill up the cleft 
    tumor_lengthy = tumor_ny * cell_width
    tumor_lengthz = tumor_nz * cell_width
    
    xbegin = lattice_dim//2 - tumor_widthx//2
    xend = lattice_dim//2 + tumor_widthx//2 
    
    ybegin = lattice_dim//2 - tumor_lengthy//2
    yend = lattice_dim//2 + tumor_lengthy//2 
    
    zbegin = lattice_dim//2 - tumor_lengthz//2
    zend = lattice_dim//2 + tumor_lengthz//2 
    
    
    for x in range(xbegin, xend, cell_width):
        for y in range(ybegin, yend, cell_width):
            for z in range(zbegin, zend, cell_width):
                if (((x == xbegin or x==xend -cell_width) and (y== ybegin or y==yend -cell_width)) or ((x == xbegin or x==xend -cell_width) and (z== zbegin or z==zend -cell_width))  or ((z == zbegin or z==zend -cell_width) and (y== ybegin or y==yend -cell_width))):
                    continue #removes edges of the cube
                cell_count += 1
                f.write(" ".join([str(cell_count), "Tumor", str(x), str(x + cell_width - 1),
                                str(y), str(y + cell_width - 1), str(z), str(z + cell_width - 1), '\n']))




    