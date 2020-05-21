import numpy as np


class ObjectLoader:
    def __init__(self):
        self.vertex_coords = []
        self.texture_coords = []
        self.normal_coords = []

        self.vertex_index = []
        self.texture_index = []
        self.normal_index = []

        self.model = []

    def load_model(self, file):
        for line in open(file, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':
                self.vertex_coords.append(values[1:4])
            if values[0] == 'vt':
                self.texture_coords.append(values[1:3])
            if values[0] == 'vn':
                self.normal_coords.append(values[1:4])

            if values[0] == 'f':
                face_i = []
                text_i = []
                normal_i = []
                for v in values[1:4]:
                    w = v.split('/')
                    face_i.append(int(w[0]) - 1)
                    text_i.append(int(w[1]) - 1)
                    normal_i.append(int(w[2]) - 1)
                self.vertex_index.append(face_i)
                self.texture_index.append(text_i)
                self.normal_index.append(normal_i)

        self.vertex_index = [y for x in self.vertex_index for y in x]
        self.texture_index = [y for x in self.texture_index for y in x]
        self.normal_index = [y for x in self.normal_index for y in x]

        for i in self.vertex_index:
            self.model.extend(self.vertex_coords[i])

        for i in self.texture_index:
            self.model.extend(self.texture_coords[i])

        # for i in self.normal_index:
        #     self.model.extend(self.normal_coords[i])

        self.model = np.array(self.model, dtype='float32')
