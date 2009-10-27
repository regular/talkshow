import pyglet
from pyglet.gl import *
from round_rect import RoundRect
import wrappers

window = pyglet.window.Window()
#image = pyglet.resource.image('kitten.jpg')

rr = RoundRect(None, "name", 120, 20, 100, 100, color="#ff6e00")

r = wrappers.Rect(None, "rect",  50, 50, 100,100, color = "#ff0000", opacity=0.5)
t = wrappers.Text(None, "text", 50, 50, h=100, color="#ffff00", opacity=0.5, text="Tubfex")
r.w = t.w

def on_resize(width, height):
    glViewport(0, 0, width, height)
    
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height);    
    glScalef(1, -1, 1);
    glTranslatef(0, -height, 0);
    
    glMatrixMode(gl.GL_MODELVIEW)

window.on_resize = on_resize

@window.event
def on_draw():
    window.clear()
    #image.blit(0, 0)
     
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
  
    rr.draw()  
    r.draw()
    t.draw()
    
    glDisable(GL_BLEND)


pyglet.app.run()