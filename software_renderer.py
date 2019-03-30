import struct
import math
from math import cos, sin
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
        self.active_shader = self.glSetGouradShader
        self.active_shader_no_tex = self.glSetGouradShaderNoTexture

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
        self.glLoadViewPortMatrix()

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

    def glLoadObj(self, filename, t=(0,0,0), s=(1,1,1), r=(0,0,0), intensity=1, tex=None):

        self.glLoadModelMatrix(t, s, r)

        model = object_loader(filename)
        if tex:
            self.active_tex = tex
            
        vertex_buffer = []
        
        for face in model.faces:
            for fi in face:
                transformed_vertex = matrix_transform(
                    VERTEX_3(*model.vertices[fi[0]]),
                    self.ViewPortMatrix,
                    self.ProjectionMatrix,
                    self.ViewMatrix,
                    self.ModelMatrix
                )
                vertex_buffer.append(transformed_vertex)

            if self.active_tex:
                for fi in face:
                    tex_vertex = VERTEX_3(*model.textures[fi[1]])
                    vertex_buffer.append(tex_vertex)

            for fi in face:
                normal_vertex = VERTEX_3(*model.normals[fi[2]])
                vertex_buffer.append(normal_vertex)

        self.active_v_array = iter(vertex_buffer)        

        try:
            while True:
                self.glBarycentricTriangle()
        except StopIteration:
                pass

    def glLookAt(self, e, c, u):
        z = vector_normal(sub(e, c))
        x = vector_normal(cross_product(u, z))
        y = vector_normal(cross_product(z, x))

        self.glLoadViewMatrix(x, y, z, c)
        self.glLoadProjectionMatrix(-1 / vector_length(sub(e, c)))        

    def glLoadModelMatrix(self, t=(0,0,0), s=(1,1,1), r=(0,0,0)):
        t = VERTEX_3(*t)
        s = VERTEX_3(*s)
        r = VERTEX_3(*r)

        translation_matrix = [
            [1, 0, 0, t.x],
            [0, 1, 0, t.y],
            [0, 0, 1, t.z],
            [0, 0, 0,   1]
        ]

        a = r.x
        r_matrix_x = [
            [1,          0,          0,  0],
            [0,     cos(a),    -sin(a),  0],
            [0,     sin(a),     cos(a),  0],
            [0,          0,          0,  1]
        ]

        a = r.y
        r_matrix_y = [
            [cos(a),    0,  -sin(a),    0],
            [     0,    1,        0,    0],
            [-sin(a),   0,   cos(a),    0],
            [0,         0,        0,    1]
        ]

        a = r.z
        r_matrix_z = [
            [cos(a),    -sin(a),    0,  0],
            [sin(a),     cos(a),    0,  0],
            [     0,          0,    1,  0],
            [     0,          0,    0,  1]
        ]

        rotation_matrix = matrix_mult(matrix_mult(r_matrix_x, r_matrix_y), r_matrix_z)
        scale_matrix = [
            [s.x,     0,      0,    0],
            [  0,   s.y,      0,    0],
            [  0,     0,    s.z,    0],
            [  0,     0,      0,    1]
        ]

        self.ModelMatrix = matrix_mult(matrix_mult(translation_matrix, rotation_matrix), scale_matrix)

    def glLoadViewMatrix(self, i, j, k, c):
        M = [
            [i.x,   i.y,    i.z,    0],
            [j.x,   j.y,    j.z,    0],
            [k.x,   k.y,    k.z,    0],
            [  0,     0,      0,    1]
        ]

        O = [
            [1, 0, 0, -c.x],
            [0, 1, 0, -c.y],
            [0, 0, 1, -c.z],
            [0, 0, 0,    1]
        ]

        self.ViewMatrix = matrix_mult(M, O)

    def glLoadProjectionMatrix(self, k):
        self.ProjectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, k, 1]
        ]

    def glLoadViewPortMatrix(self):
        self.ViewPortMatrix = [
            [self.viewport_width / 2,                           0,      0,     self.viewport_width / 2],
            [                      0,    self.viewport_height / 2,      0,    self.viewport_height / 2],
            [                      0,                           0,    128,                         128],
            [                      0,                           0,      0,                           1]
        ]

    def glShaderIntensity(self, normal, intensity):
        return round(255 * dot_product(normal, VERTEX_3(0,0,intensity)))

    def glBarycentricTriangle(self, intensity=1):        
        point_A = next(self.active_v_array)
        point_B = next(self.active_v_array)
        point_C = next(self.active_v_array)        

        # if we have textures
        if self.active_tex:
            tex_v_A = next(self.active_v_array)
            tex_v_B = next(self.active_v_array)
            tex_v_C = next(self.active_v_array)

        # normals
        normal_A = next(self.active_v_array)
        normal_B = next(self.active_v_array)
        normal_C = next(self.active_v_array)

        # bounding boxes for bary
        min_bounding_box, max_bounding_box = bounding_box(point_A, point_B, point_C)

        # print('bboxes', min_bounding_box, max_bounding_box)

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
                    tex_x_pos = (tex_v_A.x * b1) + (tex_v_B.x * b2) + (tex_v_C.x * b3)
                    tex_y_pos = (tex_v_A.y * b1) + (tex_v_B.y * b2) + (tex_v_C.y * b3)

                    # replace default color with texture
                    #colour = self.active_tex.get_texture_color(tex_x_pos, tex_y_pos, tex_intensity)

                    colour = self.active_shader(
                        self,
                        triangle=(point_A, point_B, point_C),
                        barycentric_coords=(b1, b2, b3),
                        texture_coords=(tex_x_pos, tex_y_pos),
                        varying_normals=(normal_A, normal_B, normal_C),
                        intensity=intensity
                    )

                    z = (point_A.z * b1) + (point_B.z * b2) + (point_C.z * b3)

                    if x < 0 or y < 0:
                        continue

                    # if x < len(self.zBuffer) and y < len(self.zBuffer[x]) and z > self.zBuffer[y][x]:
                    try:
                        if z > self.zBuffer[y][x]:
                            # print('about to draw point at: (x,y)' + str(x) + ', ' + str(y) + ', ' + '. Normalized: ' + str(self.glGetNormalizedXCoord(x)) + str(self.glGetNormalizedYCoord(y)))
                            self.glVertex(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y), colour)
                            self.zBuffer[y][x] = z
                    except:
                        pass
                else:
                    if grey < 0:
                        continue

                    z = (point_A.z * b1) + (point_B.z * b2) + (point_C.z * b3)

                    if x < 0 or y < 0:
                        continue

                    colour_grey = self.active_shader_no_tex(
                        self,                        
                        barycentric_coords=(b1, b2, b3),                        
                        varying_normals=(normal_A, normal_B, normal_C),
                        intensity=intensity
                    )

                    # if x < len(self.zBuffer) and y < len(self.zBuffer[x]) and z > self.zBuffer[y][x]:
                    try:
                        if z > self.zBuffer[y][x]:
                            # print('about to draw point at: (x,y)' + str(x) + ', ' + str(y) + ', ' + '. Normalized: ' + str(self.glGetNormalizedXCoord(x)) + str(self.glGetNormalizedYCoord(y)))
                            self.glVertex(self.glGetNormalizedXCoord(x), self.glGetNormalizedYCoord(y), colour_grey)
                            self.zBuffer[y][x] = z
                    except:
                        pass

    def glSetGouradShaderNoTexture(self, obj, **kwargs):
        b1, b2, b3 = kwargs['barycentric_coords']                
        normal_A, normal_B, normal_C = kwargs['varying_normals']

        norm_x = normal_A.x * b1 + normal_B.x * b2 + normal_C.x * b3
        norm_y = normal_A.y * b1 + normal_B.y * b2 + normal_C.y * b3
        norm_z = normal_A.z * b1 + normal_B.z * b2 + normal_C.z * b3

        norm = VERTEX_3(norm_x, norm_y, norm_z)        

        texture_color = color(255, 255, 255)
        tex_intensity = dot_product(norm, VERTEX_3(0, 0, kwargs['intensity']))

        try:
            return color(
                int(texture_color[2] * tex_intensity) if (texture_color[0] * tex_intensity > 0) else 0,
                int(texture_color[1] * tex_intensity) if (texture_color[1] * tex_intensity > 0) else 0,
                int(texture_color[0] * tex_intensity) if (texture_color[2] * tex_intensity > 0) else 0
            )
        except:
            pass

    def glSetGouradShader(self, obj, **kwargs):
        b1, b2, b3 = kwargs['barycentric_coords']
        tex_x_pos, tex_y_pos = kwargs['texture_coords']
        texture_color = obj.active_tex.get_texture_color(tex_x_pos, tex_y_pos)
        normal_A, normal_B, normal_C = kwargs['varying_normals']

        intensity_point_A, intensity_point_B, intensity_point_C = [
            dot_product(normal, VERTEX_3(0,0,kwargs['intensity'])) for normal in (normal_A, normal_B, normal_C)
        ]

        tex_intensity = (b1*intensity_point_A) + (b2*intensity_point_B) + (b3*intensity_point_C)

        try:
            return color(
                int(texture_color[2] * tex_intensity) if (texture_color[0] * tex_intensity > 0) else 0,
                int(texture_color[1] * tex_intensity) if (texture_color[1] * tex_intensity > 0) else 0,
                int(texture_color[0] * tex_intensity) if (texture_color[2] * tex_intensity > 0) else 0
            )
        except:
            pass

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
