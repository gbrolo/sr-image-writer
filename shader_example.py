from software_renderer import Software_Renderer
from texture_loader import texture_loader
from polygon_math import VERTEX_3

GL = Software_Renderer('render.bmp')

def init_renderer():
    GL.glInit()
    GL.glCreateWindow(1920, 1080)
    GL.glViewPort(0, 0, 1920, 1080)
    GL.glClear(0, 0, 0)
    GL.glColor(1, 1, 1)

############################################### DRAWING FUNCTIONS ############################################
def high_shot():
    # first obj
    obj = 'deer/deer_normals.obj'
    translate = (-0.5, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    # texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(10, 25, 28), 
        VERTEX_3(0, -0.2, 0), 
        VERTEX_3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity)

    # second obj
    obj = 'deer/deer_normals.obj'
    translate = (0.5, 0, 0)
    scale = (0.1, 0.17, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

high_shot()
