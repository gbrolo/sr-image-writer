class object_loader(object):
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.textures = []

        with open(filename) as f:
            self.document_lines = f.read().splitlines()

        self.read()

    def read(self):
        for line in self.document_lines:
            if line:

                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''

                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int, face.split('/'))) for face in value.split(' ')])
                elif prefix == 'vt':
                    self.textures.append(list(map(float, value.split(' '))))

        # for vertex in self.vertices:
        #     print(vertex)

        # for face in self.faces:
        #     print(face)