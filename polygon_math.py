from collections import namedtuple

VERTEX_2 = namedtuple('Point2', ['x', 'y'])
VERTEX_3 = namedtuple('Point3', ['x', 'y', 'z'])

def sum(v1, v2):
    return VERTEX_3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def sub(v1, v2):
    return VERTEX_3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def scalar_mult(v1, k):
    return VERTEX_3(v1.x * k, v1.y * k, v1.z *k)

def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def cross_product(v1, v2):
    return VERTEX_3(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x,)

def vector_length(v1):
    return (v1.x**2 + v1.y**2 + v1.z**2)**0.5

def vector_normal(v1):
    length = vector_length(v1)

    if not length:
        return VERTEX_3(0, 0, 0)
    else:
        return VERTEX_3(v1.x/length, v1.y/length, v1.z/length)

def bounding_box(*vertices):
    x_coords = [ v.x for v in vertices ]
    y_coords = [ v.y for v in vertices ]
    x_coords.sort()
    y_coords.sort()

    return VERTEX_2(x_coords[0], y_coords[0]), VERTEX_2(x_coords[-1], y_coords[-1])

def transform(v, t=(0,0,0), s=(1,1,1)):
        return VERTEX_3(round((v[0] + t[0]) * s[0]), round((v[1] + t[1]) * s[1]), round((v[2] + t[2]) * s[2]))

