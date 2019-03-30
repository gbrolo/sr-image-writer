def facePosMinus1(f, b=10, value=None):
    try:
        return int(f, b) - 1
    except ValueError:
        return value

class object_loader(object):
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.textures = []
        self.normals = []

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
                    self.faces.append([list(map(facePosMinus1, face.split('/'))) for face in value.split(' ')])
                elif prefix == 'vt':
                    self.textures.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float, value.split(' '))))