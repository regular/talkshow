import pyglet
from pyglet.gl import *
from round_rect import RoundRect
import wrappers
import widget
from delayed_call import *
import animated_property
import time

#world = wrappers.Group(None, "world", 0, 0, 640, 480, clipChildren = False)

screen = wrappers.Screen("TALKSHOW")
#vp0 = wrappers.Viewport(screen, "vp0", 0, 0, 640, 480, world=world)

#image = pyglet.resource.image('kitten.jpg')

#rr = RoundRect(world, "name", 120, 20, 100, 50, color="#ff6e00")

#g = wrappers.Group(None, "Group", 0,0, 200, 200, clipChildren=True)
#b = wrappers.Rect(g, "bg",  50, 50, 100,200, color = "#ffffff", opacity=0.5)
#r = wrappers.Rect(g, "rect",  50, 50, 100, 100, color = "#ff0000", opacity=0.5)
#t = wrappers.Text(g, "text", 50, 50, h=r.h, color="#ffff00", opacity=0.5, text="Tubifex")
#r.w = t.w
#g.w = b.w + 1
#g.offset = (50, 50)

#rr2 = RoundRect(world, "name", 120, 160, 100, 50, color="#006edd")

#vp = wrappers.Viewport(world, "viewport", 50,0, 200, 100, world = g)


def tick():
    animated_property.T = time.time()*1000
    animated_property.AnimatedProperty.tick()
    return True
    
pc = PeriodicCall(tick,0)

#g.animate("x", -100, 500, 0, 5000, flags=animated_property.LOOP)
#rr.animate("w", 40, 200, 0, 2000, flags=animated_property.LOOP|animated_property.PING_PONG|animated_property.SMOOTH)

rootWidget = widget.Widget(screen, "Widgets", w=screen.w, h=screen.h)
#slider = widget.Slider(rootWidget, "slider1", 20, 20, 200, 40)
box = widget.Box(rootWidget, "box", 400,400)

screen.event_handler = rootWidget


pyglet.app.run()