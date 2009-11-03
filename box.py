from round_rect import RoundRect
from wrappers import *
from widget import *
from delayed_call import *
from animated_property import *
import time
import animated_property
      
screen = Screen("Test", "", 800,600, color="#4f4f4f")
Rect(screen,"bg",w=screen.w, h=screen.h, color="#00007f")
rootWidget = Widget(screen, "Widgets", w=screen.w, h=screen.h)

r = Box(rootWidget, "rr", 600, 400)
r.clipCHildren=False
r.x = 40
r.y = 40

slider = Slider(rootWidget, "slider1", 20, 200, 200, 40)
scroller = Scrollbar(rootWidget, "sb1", 250, 100, 300, 40)
button = Button(rootWidget, "button", 250, 400, 300, 40)

image = Image(rootWidget, "image", "content/Zwei/cursor_big_over_2.png", x=40, y=40)
#led = LED(rootWidget, "led1", 650, 500)
t = Label(rootWidget, "Hello", x=40, y=40, size=400, font="Helvetica")
#t = Text(rootWidget, "Hello", x=40, y=40, h=400, font="Helvetica")


#r.animate("w", 300, 500, 0, 3000, PING_PONG | SMOOTH)
#r.animate("h", 200, 300, 0, 2000, PING_PONG | SMOOTH)

image.animate("w", 300, 500, 0, 3000, PING_PONG | SMOOTH)
image.animate("h", 200, 300, 0, 2000, PING_PONG | SMOOTH)

t.animate("w", 300, 500, 0, 3000, PING_PONG | SMOOTH)
t.animate("h", 200, 300, 0, 2000, PING_PONG | SMOOTH)


screen.event_handler = rootWidget

#pc0 = PeriodicCall(led.toggle, 250)

def tick():
    animated_property.T = time.time()*1000
    AnimatedProperty.tick()
    return True
    
pct = PeriodicCall(tick,0)

pyglet.app.run()