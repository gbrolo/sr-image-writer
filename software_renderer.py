import struct
import math

def char(c) :
    return struct.pack("=c", c.encode('ascii'))

def word(w) :
    return struct.pack("=h", w)

def dword(d) :
    return struct.pack("=l", d)

def color(r, g, b):
    return bytes([b, g, r])

class Software_Renderer(object):
    def __init__(self, filename):
        self.filename = filename

        self.glInit()

    def glInit(self):
        self.pixels = []
        self.gl_color = color(255, 255, 255)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewPort(self, x, y, width, height):
        self.viewport_width = width
        self.viewport_height = height
        self.viewport_x_offset = x
        self.viewport_y_offset = y

    def glClear(self):
        self.glClearColor(0, 0, 0)

    def glClearColor(self, r, g, b): 
        r_converted = math.floor(r*255)
        g_converted = math.floor(g*255)
        b_converted = math.floor(b*255)

        self.pixels = [
            [color(r_converted, g_converted, b_converted) for x in range(self.width)]
            for y in range(self.height)
        ]

    def glGetRealXCoord(self, x):
        dx = x * (self.viewport_width / 2)
        real_x_viewport_coord = (self.viewport_width / 2) + dx
        real_x_coord = real_x_viewport_coord + self.viewport_x_offset
        return real_x_coord

    def glGetRealYCoord(self, y):
        dy = y * (self.viewport_height / 2)
        real_y_viewport_coord = (self.viewport_height / 2) + dy
        real_y_coord = real_y_viewport_coord + self.viewport_y_offset
        return real_y_coord

    def glGetNormalizedXCoord(self, real_x_coord):
        real_x_viewport_coord = real_x_coord - self.viewport_x_offset
        dx = real_x_viewport_coord - (self.viewport_width / 2)
        x = dx / (self.viewport_width / 2)
        return x

    def glGetNormalizedYCoord(self, real_y_coord):
        # get first normalized y coord for pos 0
        real_y_viewport_coord = real_y_coord - self.viewport_y_offset
        dy = real_y_viewport_coord - (self.viewport_height / 2)
        y = dy / (self.viewport_height / 2)
        return y

    def glVertex(self, x, y):
        if ((x >= -1 and x <= 1) and (y >= -1 and y <= 1)):
            # check x first            
            dx = x * (self.viewport_width / 2)
            real_x_viewport_coord = (self.viewport_width / 2) + dx

            # check y
            dy = y * (self.viewport_height / 2)
            real_y_viewport_coord = (self.viewport_height / 2) + dy

            # now add viewport offsets
            real_x_coord = real_x_viewport_coord + self.viewport_x_offset
            real_y_coord = real_y_viewport_coord + self.viewport_y_offset

            # print("real_x_coord: ")
            # print(math.floor(real_x_coord))

            # print("real_y_coord: ")
            # print(math.floor(real_y_coord))            

            # draw only if inside picture dimensions
            if ((real_x_coord <= self.width) and (real_y_coord <= self.height)):
                if (real_x_coord == self.width):
                    real_x_coord = self.width - 1
                if (real_y_coord == self.height): 
                    real_y_coord = self.height - 1
                self.pixels[math.floor(real_y_coord)][math.floor(real_x_coord)] = self.gl_color

    def glColor(self, r, g, b):
        r_converted = math.floor(r*255)
        g_converted = math.floor(g*255)
        b_converted = math.floor(b*255)

        self.gl_color = color(r_converted, g_converted, b_converted)

    def glLineLow(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1

        if (dy < 0):
            yi = -1
            dy = -dy
        
        D = 2*dy - dx
        y = y0

        for x in range(x0, x1):            
            self.glVertex(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y))
            if (D > 0):
                y = y + yi
                D = D - 2*dx
            
            D = D + 2*dy

    def glLineHigh(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1

        if (dx < 0):
            xi = -1
            dx = -dx
        
        D = 2*dx - dy
        x = x0

        for y in range(y0, y1):            
            self.glVertex(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y))
            if (D > 0):
                x = x + xi
                D = D - 2*dy
            
            D = D + 2*dx

    def glLine(self, x0, y0, x1, y1):
        x0 = math.floor(self.glGetRealXCoord(x0))
        y0 = math.floor(self.glGetRealYCoord(y0))
        x1 = math.floor(self.glGetRealXCoord(x1))
        y1 = math.floor(self.glGetRealYCoord(y1))        

        if abs(y1 - y0) < abs(x1 - x0):
            if (x0 > x1):
                self.glLineLow(x1, y1, x0, y0)
            else:
                self.glLineLow(x0, y0, x1, y1)
        else:
            if (y0 > y1):
                self.glLineHigh(x1, y1, x0, y0)
            else:
                self.glLineHigh(x0, y0, x1, y1)
            

    def glFinish(self):
        f = open(self.filename, 'bw')

        # file header 14 bytes
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header 40 bytes
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

        f.close()

# Example
GL = Software_Renderer('render.bmp')
GL.glInit()
GL.glCreateWindow(1920, 1080)
GL.glViewPort(0, 0, 1920, 1080)
GL.glClear()
GL.glColor(1, 0, 0)
GL.glVertex(0,0)
GL.glLine(0,0,1,1)
GL.glFinish()