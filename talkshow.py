import pyglet
from pyglet.gl import *
from round_rect import RoundRect
import wrappers

window = pyglet.window.Window()
#image = pyglet.resource.image('kitten.jpg')

rr = RoundRect(None, "name", 120, 20, 100, 100, color="#ff6e00")

g = wrappers.Group(None, "Group", 0,0, 200, 200, clipChildren=True)
b = wrappers.Rect(g, "bg",  50, 50, 100,200, color = "#ffffff", opacity=0.5)
r = wrappers.Rect(g, "rect",  50, 50, 100, 100, color = "#ff0000", opacity=0.5)
t = wrappers.Text(g, "text", 50, 50, h=r.h, color="#ffff00", opacity=0.5, text="Tubifex")
r.w = t.w
g.w = b.w + 1
g.offset = (50, 50)

vp = wrappers.Viewport(None, "viewport", 50,0, 200, 100, world = g)

 
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
    #r.draw()
    #t.draw()
    
    #g.draw()
    vp.draw()
    
    glDisable(GL_BLEND)


pyglet.app.run()