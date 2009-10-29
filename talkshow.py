import pyglet
from pyglet.gl import *
from round_rect import RoundRect
import wrappers

world = wrappers.Group(None, "world", 0, 0, 640, 480, clipChildren = False)

screen = wrappers.Screen("TALKSHOW")
vp0 = wrappers.Viewport(screen, "vp0", 0, 0, 640, 480, world=world)

#image = pyglet.resource.image('kitten.jpg')

rr = RoundRect(world, "name", 120, 20, 100, 100, color="#ff6e00")

g = wrappers.Group(None, "Group", 0,0, 200, 200, clipChildren=True)
b = wrappers.Rect(g, "bg",  50, 50, 100,200, color = "#ffffff", opacity=0.5)
r = wrappers.Rect(g, "rect",  50, 50, 100, 100, color = "#ff0000", opacity=0.5)
t = wrappers.Text(g, "text", 50, 50, h=r.h, color="#ffff00", opacity=0.5, text="Tubifex")
r.w = t.w
g.w = b.w + 1
g.offset = (50, 50)

vp = wrappers.Viewport(world, "viewport", 50,0, 200, 100, world = g)

class MyHandler:
    def onMouseMove(self, x, y):
        print x, y

screen.event_handler = MyHandler()

pyglet.app.run()