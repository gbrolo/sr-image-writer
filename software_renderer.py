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

                # print("f1, f2, v1, v2: " + str(f1) + ', ' + str(f2) +', ' + str(v1) + ', ' + str(v2))

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
 
    def glLoadObj(self, filename, t=(0,0,0), s=(1,1,1), intensity=1, bary=False, tex=None):
        model = object_loader(filename)

        for face in model.faces:
            # print('face is: ' + str(face))
            vcount = len(face)

            if vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                point_A = transform(model.vertices[f1], t, s)
                point_B = transform(model.vertices[f2], t, s)
                point_C = transform(model.vertices[f3], t, s)

                normal = vector_normal(cross_product(sub(point_B, point_A), sub(point_C, point_A)))
                grey = self.glShaderIntensity(normal, intensity)

                # print('about to draw triangle at points: (A,B,C)' + str(point_A) + ', ' + str(point_B) + ', ' + str(point_C))
                if not tex:
                    if grey < 0:
                        continue  

                    if bary:
                        self.glBarycentricTriangle(point_A, point_B, point_C, color(grey, grey, grey))
                    else:                    
                        self.glTriangle(point_A, point_B, point_C, color(grey, grey, grey))
                else:                    
                    tex_A = VERTEX_3(*model.textures[face[0][1] - 1])
                    tex_B = VERTEX_3(*model.textures[face[1][1] - 1])
                    tex_C = VERTEX_3(*model.textures[face[2][1] - 1])

                    tex_coords = (tex_A, tex_B, tex_C)
                    tex_intensity = dot_product(normal, VERTEX_3(0,0,intensity))

                    if bary:
                        self.glBarycentricTriangle(
                            point_A, point_B, point_C, tex=tex, tex_coords=tex_coords, intensity=tex_intensity
                        )
                    else:
                        self.glTriangle(point_A, point_B, point_C, color(grey, grey, grey))


            else:
                # we have 4 faces (asuming we have a square to paint!)
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1 

                # print('f1, f2, f3, f4: ' + str(f1) + ', ' + str(f2) + ', ' + str(f3) + ', ' + str(f4))  

                vertices = [
                    transform(model.vertices[f1], t, s),
                    transform(model.vertices[f2], t, s),
                    transform(model.vertices[f3], t, s),
                    transform(model.vertices[f4], t, s)
                ]

                # print('vertices: ' + str(vertices))

                normal = vector_normal(cross_product(sub(vertices[0], vertices[1]), sub(vertices[1], vertices[2])))                
                grey = self.glShaderIntensity(normal, intensity)

                point_A, point_B, point_C, point_D = vertices 

                # print('about to draw 2 triangles at points: (A,B,C,D)' + str(point_A) + ', ' + str(point_B) + ', ' + str(point_C) + ', ' + str(point_D))
                if not tex:
                    if grey < 0:
                        continue

                    if bary:
                        self.glBarycentricTriangle(point_A, point_B, point_C, color(grey, grey, grey))
                        self.glBarycentricTriangle(point_A, point_C, point_D, color(grey, grey, grey))
                    else:
                        self.glTriangle(point_A, point_B, point_C, color(grey, grey, grey))
                        self.glTriangle(point_A, point_C, point_D, color(grey, grey, grey))
                else:
                    tex_A = VERTEX_3(*model.textures[face[0][1] - 1])
                    tex_B = VERTEX_3(*model.textures[face[1][1] - 1])
                    tex_C = VERTEX_3(*model.textures[face[2][1] - 1])
                    tex_D = VERTEX_3(*model.textures[face[3][1] - 1])

                    tex_intensity = dot_product(normal, VERTEX_3(0,0,intensity))

                    if bary:
                        tex_coords = (tex_A, tex_B, tex_C)
                        self.glBarycentricTriangle(
                            point_A, point_B, point_C, tex=tex, tex_coords=tex_coords, intensity=tex_intensity
                        )

                        tex_coords = (tex_A, tex_C, tex_D)
                        self.glBarycentricTriangle(
                            point_A, point_C, point_D, tex=tex, tex_coords=tex_coords, intensity=tex_intensity
                        )
                    else:
                        self.glTriangle(point_A, point_B, point_C, color(grey, grey, grey))
                        self.glTriangle(point_A, point_C, point_D, color(grey, grey, grey))

    def glShaderIntensity(self, normal, intensity):
        return round(255 * dot_product(normal, VERTEX_3(0,0,intensity)))

    def glTriangle(self, point_A, point_B, point_C, color=None):
        # swap points
        if point_A.y > point_B.y:
            point_A, point_B = point_B, point_A
        if point_A.y > point_C.y:
            point_A, point_C = point_C, point_A
        if point_B.y > point_C.y: 
            point_B, point_C = point_C, point_B

        # changes in x and y in segment AC
        dx_AC = point_C.x - point_A.x
        dy_AC = point_C.y - point_A.y

        if dy_AC == 0:
            return

        slope_AC = dx_AC/dy_AC

        # changes in x and y in segment AB
        dx_AB = point_B.x - point_A.x
        dy_AB = point_B.y - point_A.y

        if dy_AB != 0:
            slope_AB = dx_AB/dy_AB

            for y in range(point_A.y, point_B.y + 1):
                xi = round(point_A.x - slope_AC * (point_A.y - y))
                xf = round(point_A.x - slope_AB * (point_A.y - y))

                # swap condition
                if xi > xf:
                    xi, xf = xf, xi
                    
                for x in range(xi, xf + 1):
                    # print('about to draw point at: (x,y)' + str(x) + ', ' + str(y) + ', ' + '. Normalized: ' + str(self.glGetNormalizedXCoord(x)) + str(self.glGetNormalizedYCoord(y)))
                    self.glVertex(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y), color)

        # changes in x and y in segment BC
        dx_BC = point_C.x - point_B.x
        dy_BC = point_C.y - point_B.y

        if dy_BC:
            slope_BC = dx_BC/dy_BC

            for y in range(point_B.y, point_C.y + 1):
                xi = round(point_A.x - slope_AC * (point_A.y - y))
                xf = round(point_B.x - slope_BC * (point_B.y - y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    # print('about to draw point at: (x,y)' + str(x) + ', ' + str(y) + ', ' + '. Normalized: ' + str(self.glGetNormalizedXCoord(x)) + str(self.glGetNormalizedYCoord(y)))
                    self.glVertex(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y), color)

    def glBarycentricTriangle(self, point_A, point_B, point_C, color=None, tex=None, tex_coords=(), intensity=1):
        # print('bary method')
        min_bounding_box, max_bounding_box = bounding_box(point_A, point_B, point_C)

        for x in range(min_bounding_box.x, max_bounding_box.x + 1):
            for y in range(min_bounding_box.y, max_bounding_box.y + 1):
                b1, b2, b3 = barycentric(point_A, point_B, point_C, VERTEX_2(x, y))

                if (b1 < 0) or (b2 < 0) or (b3 < 0):
                    continue

                # apply textures
                if tex:
                    tex_v_A, tex_v_B, tex_v_C = tex_coords
                    tex_x_pos = (tex_v_A.x * b1) + (tex_v_B.x * b2) + (tex_v_C.x * b3)
                    tex_y_pos = (tex_v_A.y * b1) + (tex_v_B.y * b2) + (tex_v_C.y * b3)

                    # replace default color with texture
                    color = tex.get_texture_color(tex_x_pos, tex_y_pos, intensity)

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
