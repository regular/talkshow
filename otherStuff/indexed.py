import pyglet
from pyglet.gl import *

def create_rect(x,y,w,h,color):
    vli = pyglet.graphics.vertex_list_indexed(4, (0, 1, 2, 0, 2, 3), "v2f", "c4B") 

    # PROBLEM: if this line, which should have no effect, is commented in, 
    # rect b becomes a triangle!
    # It seems like the points referenced by the indices are being copied
    # from rect a to rect b
    vli.indices[0:3] = (0, 1, 2)

    vli.vertices = (x, y, x+w, y, x+w, y+h, x, y+h)     
    vli.colors= color*4
    return vli
 
window = pyglet.window.Window()

a = create_rect(10,10,100,100,(0,255,0,255))
b = create_rect(110,110,100,100,(0,0,255,255))


@window.event
def on_draw():
    window.clear()
    #a.draw(pyglet.gl.GL_TRIANGLES)
    b.draw(pyglet.gl.GL_TRIANGLES)

pyglet.app.run()