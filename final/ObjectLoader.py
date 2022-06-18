import numpy as np
from OpenGL.GL import *



class Mesh:
    buffer = []

    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d)-1 if d else 0)


    @staticmethod # sorted vertex buffer for use with glDrawArrays function
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # sort the vertex coordinates
                start = ind * 3
                end = start + 3
                Mesh.buffer.extend(vertices[start:end])
            elif i % 3 == 1: # sort the texture coordinates
                start = ind * 2
                end = start + 2
                Mesh.buffer.extend(textures[start:end])
            elif i % 3 == 2: # sort the normal vectors
                start = ind * 3
                end = start + 3
                Mesh.buffer.extend(normals[start:end])


    @staticmethod # TODO unsorted vertex buffer for use with glDrawElements function
    def create_unsorted_vertex_buffer(indices_data, vertices, textures, normals):
        num_verts = len(vertices) // 3

        for i1 in range(num_verts):
            start = i1 * 3
            end = start + 3
            Mesh.buffer.extend(vertices[start:end])

            for i2, data in enumerate(indices_data):
                if i2 % 3 == 0 and data == i1:
                    start = indices_data[i2 + 1] * 2
                    end = start + 2
                    Mesh.buffer.extend(textures[start:end])

                    start = indices_data[i2 + 2] * 3
                    end = start + 3
                    Mesh.buffer.extend(normals[start:end])

                    break


    @staticmethod
    def load_model(file, sorted=True):
        vert_coords = [] # will contain all the vertex coordinates
        tex_coords = [] # will contain all the texture coordinates
        norm_coords = [] # will contain all the vertex normals

        all_indices = [] # will contain all the vertex, texture and normal indices
        indices = [] # will contain the indices for indexed drawing


        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if values[0] == 'v':
                    Mesh.search_data(values, vert_coords, 'v', 'float')
                elif values[0] == 'vt':
                    Mesh.search_data(values, tex_coords, 'vt', 'float')
                elif values[0] == 'vn':
                    Mesh.search_data(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        Mesh.search_data(val, all_indices, 'f', 'int')
                        indices.append(int(val[0])-1)

                line = f.readline()

        if sorted:
            # use with glDrawArrays
            Mesh.create_sorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)
        else:
            # use with glDrawElements
            Mesh.create_unsorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)

        # Mesh.show_buffer_data(Mesh.buffer)

        buffer = Mesh.buffer.copy() # create a local copy of the buffer list, otherwise it will overwrite the static field buffer
        Mesh.buffer = [] # after copy, make sure to set it back to an empty list

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')
