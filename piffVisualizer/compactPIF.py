import numpy as np
import os

files = sorted([f for f in os.listdir('.//') if f.endswith(".piff")])

#Gotta check that size and types
size = np.array([1,1,1])
lines = open(files[0],"r").readlines()
for line in lines:
    split_line = line.split('\t')
    size[0] = np.max([size[0], int(split_line[2])+1])
    size[1] = np.max([size[1], int(split_line[4])+1])
    size[2] = np.max([size[2], int(split_line[6])+1])

type_dictionary = {}
id_dictionary = {}
for f in files:
    lines = open(f, "r").readlines()
    for line in lines:
        split_line = line.split('\t')

        #type:
        if split_line[0] not in id_dictionary:
            id_dictionary[split_line[0]] = len(id_dictionary)

        if split_line[1] not in type_dictionary:
            type_dictionary[split_line[1]] = len(type_dictionary)

type_matrices = []
id_matrices = []

content = np.array([len(files)]).astype('int32').tobytes()+ size.astype('int32').tobytes()

for f in files:
    type_matrix = np.zeros(size)
    id_matrix = np.zeros(size)

    lines = open(f,"r").readlines()
    for line in lines:
        split_line = line.split('\t')

        type_matrix[int(split_line[2]),int(split_line[4]),int(split_line[6])] = type_dictionary[split_line[1]]
        id_matrix[int(split_line[2]),int(split_line[4]),int(split_line[6])] = id_dictionary[split_line[0]]

    type_matrices.append(type_matrix)
    id_matrices.append(id_matrix)

    content += type_matrix.astype('b').tobytes()
    content += id_matrix.astype('b').tobytes()


open("outputpiff","wb").write(content)
