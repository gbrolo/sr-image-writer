from software_renderer import Software_Renderer
from texture_loader import texture_loader

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
    translate = (17, 11, 0)
    scale = (60, 60, 60)
    intensity = 1
    barycentric = True
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale) + '\nbarycentric:   ' + str(barycentric))
    
    init_renderer()
    GL.glLoadObj(obj, translate, scale, intensity, barycentric, texture)
    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

def draw_deer_two_sides():
    obj = 'deer/deer.obj'
    translate = (8, 11, 0)
    scale = (60, 60, 60)
    intensity = 1
    barycentric = True
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale) + '\nbarycentric:   ' + str(barycentric))
    
    init_renderer()
    GL.glLoadObj(obj, translate, scale, intensity, barycentric, texture)

    obj = 'deer/deer_reverse.obj'
    translate = (20, 11, 0)
    scale = (60, 60, 60)
    intensity = 1
    barycentric = True
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale) + '\nbarycentric:   ' + str(barycentric))
    
    GL.glLoadObj(obj, translate, scale, intensity, barycentric, texture)
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