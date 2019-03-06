import struct

def color(r, g, b):
    return bytes([b, g, r])

class texture_loader(object):
    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
        # Read without BM, bmp size and zeros
        self.image = open(self.filename, 'rb')
        self.image.seek(10)
        self.header_size = struct.unpack('=l', self.image.read(4))[0]
        self.image.seek(18)

        # Width, Height and pixel array
        self.width = struct.unpack("=l", self.image.read(4))[0]
        self.height = struct.unpack("=l", self.image.read(4))[0]
        self.pixels = []

        self.image.seek(self.header_size)

        for y in range(self.height):
            self.pixels.append([])

            for x in range(self.width):
                blue = ord(self.image.read(1))
                green = ord(self.image.read(1))
                red = ord(self.image.read(1))

                self.pixels[y].append(color(red, green, blue))

        self.image.close()

    def get_texture_color(self, tex_x_pos, tex_y_pos, intensity = 1):
        x_coord = int(tex_x_pos * self.width)
        y_coord = int(tex_y_pos * self.height)

        try:
            return bytes(
            map(
                lambda tex: round(tex * intensity) if tex * intensity > 0 else 0, self.pixels[y_coord][x_coord]
            )
        )
        except:
            pass