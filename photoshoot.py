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
def medium_shot():
    obj = 'deer/deer.obj'
    translate = (1.5, 0.05, -0.2)
    scale = (0.15, 0.18, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(5, 1, 0), 
        VERTEX_3(0, 0, 0), 
        VERTEX_3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

def dutch_angle():
    obj = 'deer/deer.obj'
    translate = (0, 0, 0)
    scale = (0.08, 0.16, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(5, 1, 0), 
        VERTEX_3(0, 0, 0), 
        VERTEX_3(0, 1, 0.13)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

def low_shot():
    obj = 'deer/deer.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(10, -6.5, 5), 
        VERTEX_3(0, -0.2, 0), 
        VERTEX_3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

def high_shot():
    obj = 'deer/deer.obj'
    translate = (0, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(10, 25, 28), 
        VERTEX_3(0, -0.2, 0), 
        VERTEX_3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

################################################# EXAMPLES ####################################################
# Call any of 'DRAWING FUNCTIONS'
medium_shot()
# dutch_angle()
# low_shot()
# high_shot()
