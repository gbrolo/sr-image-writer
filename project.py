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

def forest():
    # first obj
    obj = 'forest/base.obj'
    translate = (0, -0.8, -0.8)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('forest/base.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    init_renderer()
    GL.glLookAt(
        VERTEX_3(10, 25, 30), 
        VERTEX_3(0, -0.2, 0), 
        VERTEX_3(0, 1, 0)
    )
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # second obj
    obj = 'deer/deer_normals.obj'
    translate = (-0.2, 0, 0)
    scale = (0.08, 0.15, 0.08)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('deer/deer.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # third obj
    obj = 'forest/bhudist_stone.obj'
    translate = (0.75, 0, 0)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('forest/bhudist_stone.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # fourth obj
    obj = 'forest/rock.obj'
    translate = (-0.3, -0.3, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('forest/rock.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # fifth obj
    obj = 'forest/log_normals.obj'
    translate = (0.75, -0.08, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0.1, 0)
    intensity = 1    
    texture = texture_loader('forest/log.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # sixth obj
    obj = 'forest/wall.obj'
    translate = (1.35, 3.6, 3.2)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0.1, 0)
    intensity = 1    
    texture = texture_loader('forest/wall.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture) 

    # seventh obj
    obj = 'forest/fern.obj'
    translate = (-0.50, -0.35, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('forest/fern.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # eight obj
    obj = 'forest/cobblestone.obj'
    translate = (-0.1, -0.60, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('forest/cobblestone.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    # eight obj
    obj = 'forest/cobblestone.obj'
    translate = (0.8, -0.60, 1)
    scale = (0.1, 0.15, 0.1)
    rotate = (0, 0, 0)
    intensity = 1    
    texture = texture_loader('forest/cobblestone.bmp')
    print('Rendering:   ' + obj + '\ntranslate:   ' + str(translate) + '\nscale:   ' + str(scale))
    print('Please wait...')
    
    GL.glLoadObj(obj, translate, scale, rotate, intensity, texture)

    GL.glFinish()

    print('Output rendered to:  \'render.bmp\'')

################################################# EXAMPLES ####################################################
forest()