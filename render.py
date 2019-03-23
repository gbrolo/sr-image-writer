from software_renderer import Software_Renderer
from texture_loader import texture_loader
from polygon_math import VERTEX_3

GL = Software_Renderer('render.bmp')

def init_renderer():
    GL.glInit()
    GL.glCreateWindow(1920, 1080)
    GL.glViewPort(0, 0, 1920, 1080)
    GL.glClear(1, 1, 1)
    GL.glColor(1, 1, 1)

############################################### DRAWING FUNCTIONS ############################################
def draw_deer_centered():
    obj = 'deer/deer.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.1, 0.1)
    rotate = (0, 25, 0)
    intensity = 1    
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(12, 1, 0), 
        VERTEX_3(0, 0, 0), 
        VERTEX_3(1, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

def draw_deer_two_sides():
    obj = 'deer/deer.obj'
    translate = (8, 11, 0)
    scale = (60, 60, 60)
    intensity = 1
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    
    init_renderer()
    GL.glLoadObj(obj, translate, scale, intensity, texture)

    obj = 'deer/deer_reverse.obj'
    translate = (20, 11, 0)
    scale = (60, 60, 60)
    intensity = 1
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    
    GL.glLoadObj(obj, translate, scale, intensity, texture)
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

def draw_deer_uv():
    obj = 'deer/deer.obj'
    translate = 1
    scale = 1
    print('Rendering UV wireframe:   ' + obj)
    
    GL.glInit()
    GL.glCreateWindow(2048, 2048)
    GL.glViewPort(0, 0, 2048, 2048)
    GL.glClear(0, 0, 0)
    GL.glColor(0, 0, 0)

    GL.glLoadTexture('deer/deer.bmp', 1)
    GL.glLoadObjWireFrameUV(obj, scale, translate)

    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

# Call any of 'DRAWING FUNCTIONS'
draw_deer_centered()
# draw_deer_two_sides()
# draw_deer_uv()