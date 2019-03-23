import struct
import math
from utils import *
from object_loader import object_loader
from texture_loader import texture_loader
from collections import namedtuple
from polygon_math import *

class Software_Renderer(object):
    def __init__(self, filename):
        self.filename = filename

        self.glInit()

    def glInit(self):
        self.pixels = []
        self.gl_color = color(255, 255, 255)
        self.glInitTexParams()

    def glInitTexParams(self):
        self.tex = None
        self.active_v_array = None
        self.active_tex = None
        self.vertex_buffer = []

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewPort(self, x, y, width, height):
        self.viewport_width = width
        self.viewport_height = height
        self.viewport_x_offset = x
        self.viewport_y_offset = y

    def glClear(self, r=0, g=0, b=0):
        self.glClearColor(r, g, b)
        self.glSetZBuffer()

    def glClearColor(self, r, g, b): 
        r_converted = math.floor(r*255)
        g_converted = math.floor(g*255)
        b_converted = math.floor(b*255)

        self.pixels = [
            [color(r_converted, g_converted, b_converted) for x in range(self.width)]
            for y in range(self.height)
        ]

    def glSetZBuffer(self, z='inf'):
        self.zBuffer = [
            [-float(z) for x in range(self.width)]
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
        real_y_viewport_coord = real_y_coord - self.viewport_y_offset
        dy = real_y_viewport_coord - (self.viewport_height / 2)
        y = dy / (self.viewport_height / 2)
        return y

    def glVertex(self, x, y, color=None):
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

            # draw only if inside picture dimensions
            if ((real_x_coord <= self.width) and (real_y_coord <= self.height)):
                if (real_x_coord == self.width):
                    real_x_coord = self.width - 1
                if (real_y_coord == self.height): 
                    real_y_coord = self.height - 1
                self.pixels[round(real_y_coord)][round(real_x_coord)] = color or self.gl_color

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

    def glLoadObjWireFrame(self, filename, scalefactor):
        model = object_loader(filename)

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j+1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]                

                x1 = v1[0] * scalefactor
                y1 = v1[1] * scalefactor
                x2 = v2[0] * scalefactor
                y2 = v2[1] * scalefactor

                self.glLine(x1, y1, x2, y2)

    def glLoadTexture(self, filename, scalefactor):
        texture = texture_loader(filename)
        
        for y in range(texture.height):
            for x in range(texture.width):
                tex_color = texture.get_texture_color(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y))
                # print(tex_color)
                self.glVertex(self.glGetNormalizedXCoord(x*scalefactor), self.glGetNormalizedYCoord(y*scalefactor), tex_color)

    def glLoadObjWireFrameUV(self, filename, scalefactor, t):
        model = object_loader(filename)              

        # for vt in model.textures:     
        #     print((vt[0] * scalefactor) - 0.5, (vt[1] * scalefactor) - 0.5)
        #     self.glVertex((vt[0] * scalefactor) - 0.5, (vt[1] * scalefactor) - 0.5)

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][1]
                f2 = face[(j+1) % vcount][1]

                v1 = model.textures[f1 - 1]
                v2 = model.textures[f2 - 1]

                # print("f1, f2, v1, v2: " + str(f1) + ', ' + str(f2) +', ' + str(v1) + ', ' + str(v2))

                x1 = (v1[0] * scalefactor) - t
                y1 = (v1[1] * scalefactor) - t
                x2 = (v2[0] * scalefactor) - t
                y2 = (v2[1] * scalefactor) - t

                self.glLine(x1, y1, x2, y2)

    def glLoadObj(self, filename, t=(0,0,0), s=(1,1,1), intensity=1, tex=None):
        model = object_loader(filename)
        self.active_tex = tex
        
        for face in model.faces:
            vcount = len(face)

            for vertex in range(vcount):
                transformed_vertex = transform(model.vertices[face[vertex][0] - 1], t, s)
                self.vertex_buffer.append(transformed_vertex)

            if self.active_tex:
                for vertex in range(vcount):
                    tex_vertex = VERTEX_3(*model.textures[face[vertex][1] - 1])
                    self.vertex_buffer.append(tex_vertex)

        self.active_v_array = iter(self.vertex_buffer)
        self.vertex_buffer = []

        try:
            while True:
                self.glBarycentricTriangle()
        except StopIteration:
                pass

    def glShaderIntensity(self, normal, intensity):
        return round(255 * dot_product(normal, VERTEX_3(0,0,intensity)))

    def glBarycentricTriangle(self, intensity=1):        
        point_A = next(self.active_v_array)
        point_B = next(self.active_v_array)
        point_C = next(self.active_v_array)

        print(point_A, point_B, point_C)

        # if we have textures
        # if self.active_tex:
        #     tex_v_A = next(self.active_v_array)
        #     tex_v_B = next(self.active_v_array)
        #     tex_v_C = next(self.active_v_array)

        # bounding boxes for bary
        min_bounding_box, max_bounding_box = bounding_box(point_A, point_B, point_C)
        print('bbox')
        print(min_bounding_box, max_bounding_box)

        normal = vector_normal(cross_product(sub(point_B, point_A), sub(point_C, point_A)))
        grey = self.glShaderIntensity(normal, intensity)
        tex_intensity = dot_product(normal, VERTEX_3(0,0,intensity))

        if tex_intensity < 0:
            return

        for x in range(min_bounding_box.x, max_bounding_box.x + 1):
            for y in range(min_bounding_box.y, max_bounding_box.y + 1):
                b1, b2, b3 = barycentric(point_A, point_B, point_C, VERTEX_2(x, y))

                if (b1 < 0) or (b2 < 0) or (b3 < 0):
                    continue                

                # apply textures
                if self.active_tex:
                    tex_v_A = next(self.active_v_array)
                    tex_v_B = next(self.active_v_array)
                    tex_v_C = next(self.active_v_array)   

                    tex_x_pos = (tex_v_A.x * b1) + (tex_v_B.x * b2) + (tex_v_C.x * b3)
                    tex_y_pos = (tex_v_A.y * b1) + (tex_v_B.y * b2) + (tex_v_C.y * b3)

                    # replace default color with texture
                    color = self.active_tex.get_texture_color(tex_x_pos, tex_y_pos, tex_intensity)
                else:
                    if grey < 0:
                        color = grey

                z = (point_A.z * b1) + (point_B.z * b2) + (point_C.z * b3)

                if x < 0 or y < 0:
                    continue

                # if x < len(self.zBuffer) and y < len(self.zBuffer[x]) and z > self.zBuffer[y][x]:
                if z > self.zBuffer[y][x]:
                    # print('about to draw point at: (x,y)' + str(x) + ', ' + str(y) + ', ' + '. Normalized: ' + str(self.glGetNormalizedXCoord(x)) + str(self.glGetNormalizedYCoord(y)))
                    self.glVertex(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y), color)
                    self.zBuffer[y][x] = z

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
