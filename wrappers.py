import weakref
import sys
from sys import getrefcount
import string
import pyglet
from pyglet.gl import *
from pyglet.media import *
from rect import *
from animated_property import AnimatedProperty

class Visible(object):
    instanceCount = 0

    def __init__(self, p, name, x=0, y=0, w=10, h=10):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        
        self.__parent__ = None
        self.setParent(p)
        
        self.__class__.instanceCount += 1
        
    def __del__(self):
        self.__class__.instanceCount -= 1
        
    def getParent(self):
        if self.__parent__ == None: return None
        return self.__parent__()
    
    def setParent(self, newParent):
        if self.__parent__ != None:
            if self.__parent__() == newParent:
                return
        else:        
            if newParent == None:
                return
                
        if newParent != None:
            newParent.__addChild__(self)
        
        if self.__parent__ != None:
            self.__parent__().__removeChild__(self)
        
        if newParent != None:
            self.__parent__ = weakref.ref(newParent) 
        else:
            self.__parent__ = None
    parent = property(getParent, setParent)
  
    def contains(self, x, y):
        if x >= self.x and y >= self.y and x < self.x + self.w and y < self.y + self.h:
            return True
        else:
            return False
    
    def _getPosition(self): return (self.x, self.y)
    def _setPosition(self, value): self.x, self.y = value
    position = property(_getPosition, _setPosition)

    def _getExtent(self): return (self.w, self.h)
    def _setExtent(self, value): self.w, self.h = value     
    extent = property(_getExtent, _setExtent)

    def draw(self):
        pass
            
    def animate(self, propname, startvalue, endvalue, when, duration = 0, flags = 0):
        if propname != "color":
            AnimatedProperty.animate(self, propname, startvalue, endvalue, when, duration, flags)
        else:
            self._color_fade_value1 = splitColorChannels(startvalue)
            self._color_fade_value2 = splitColorChannels(endvalue)
            self._color_fade = 0.0
            AnimatedProperty.animate(self, "_color_fade", 0.0, 1.0, when, duration, flags)
    
def splitColorChannels(c):
    return (
        string.atoi(c[1:3], 16) / 255.0,
        string.atoi(c[3:5], 16) / 255.0,
        string.atoi(c[5:7], 16) / 255.0
    )

def mergeColorChannels(r,g,b):
    return "#%2.2X%2.2X%2.2X" % (r*255,g*255,b*255)

class ColoredVisible(Visible):
    instanceCount = 0

    def __init__(self, p, name, x=0, y=0, w=0, h=0, color="#00ff00", opacity=1.0):
        Visible.__init__(self, p, name, x, y, w, h)
        self.color = color
        self.opacity = opacity
        
    def _setColor(self, c):
        self.r, self.g, self.b = splitColorChannels(c)
    def _getColor(self):
        return mergeColorChannels(self.r, self.g, self.b)
    color = property(_getColor, _setColor)
    
    def _setCOLORFADE(self, cf):
        self._COLORFADE= cf
        r1, g1, b1 = self._color_fade_value1
        r2, g2, b2 = self._color_fade_value2

        self.r = r1 + (r2 - r1) * cf
        self.g = g1 + (g2 - g1) * cf
        self.b = b1 + (b2 - b1) * cf

    def _getCOLORFADE(self):
        return self._COLORFADE
    _color_fade = property(_getCOLORFADE, _setCOLORFADE)


class Rect(ColoredVisible):
    instanceCount = 0

    def __init__(self, p, name, x=0, y=0, w=0, h=0, color="#00ff00", opacity=1.0):
        ColoredVisible.__init__(self, p, name, x, y, w, h, color, opacity)
    
    def draw(self):
        #glColor3f(self.r,self.g,self.b)
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 0, 2, 3],
            ('v2f', (float(self.x), float(self.y),
                     float(self.x+self.w), float(self.y),
                     float(self.x+self.w), float(self.y+self.h),
                     float(self.x), float(self.y+self.h))),
            ('c4f', (self.r, self.g, self.b, self.opacity)*4)
        )

class Screen(ColoredVisible):    
    def __init__(self, name, device = "", w = 640, h = 480, color="#00007f"):
        
        self.window = pyglet.window.Window(caption=name, fullscreen=1, resizable=True)
                
        ColoredVisible.__init__(self, None, name, 0, 0, self.w, self.h, color, opacity=1.0)
        self.__children__ = []
        self.event_handler = None
        
        def on_resize(width, height):
            self.extent = width, height
            glViewport(0, 0, width, height)

            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            gluOrtho2D(0, width, 0, height);    
            glScalef(1, -1, 1);
            glTranslatef(0, -height, 0);

            glMatrixMode(gl.GL_MODELVIEW)

        self.window.on_resize = on_resize
        
        @self.window.event
        def on_draw():
            self.window.clear()

            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable(GL_BLEND)

            for x in self.__children__:
                x.draw()

            glDisable(GL_BLEND)
                     
        buttonLUT = {
            pyglet.window.mouse.LEFT: "left",
            pyglet.window.mouse.MIDDLE: "middle",
            pyglet.window.mouse.RIGHT: "right",
        }
                
        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            y = self.h - y
            h = self.getHandlerMethod("onMouseMove")
            if h: h(x, y)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            y = self.h - y
            h = self.getHandlerMethod("onMouseButtonDown")
            if h: h(buttonLUT[button], x, y)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            y = self.h - y
            h = self.getHandlerMethod("onMouseButtonUp")
            if h: h(buttonLUT[button], x, y)

        @self.window.event         
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            # we use the same handler as for mouse move
            y = self.h - y
            h = self.getHandlerMethod("onMouseMove")
            if h: h(x, y)
            
        #@self.window.event
        #def on_mouse_scroll(x, y, scroll_x, scroll_y):
        
    def getHandlerMethod(self, name):
        if self.event_handler != None:
            if hasattr(self.event_handler, name):
                return getattr(self.event_handler, name)
        return None
          
    def __addChild__(self, c):
        if not c in self.__children__:
            self.__children__.append(c)

    def __removeChild__(self, c):
        self.__children__.remove(c)

    def __iter__(self):
        return self.__children__.__iter__()

    def __len__(self):
        return len(self.__children__)
        
    def getW(self): return self.window.width
    def setW(self, w):
        if w != self.window.width:
            self.window.width = w
    w = property(getW, setW)

    def getH(self): return self.window.height
    def setH(self, h): 
        if h != self.window.height:
            self.window.height = h
    h = property(getH, setH)
         
class Image(ColoredVisible):
    def __init__(self, p, name, path, x=0, y=0, w=None, h=None, color="#ffffff", opacity=1.0):
        if path:
            image = pyglet.image.load(path.encode(sys.getfilesystemencoding()))
            self.sprite = pyglet.sprite.Sprite(image)
        
        if w == None: w = self.sprite.width
        if h == None: h = self.sprite.height
        
        ColoredVisible.__init__(self, p, name, x, y, w, h, color, opacity)
      
    def _colorComponentGetter(i):
         def getter(self): 
             self.sprite.color[i]/255.0
         return getter

    def _colorComponentSetter(i):
        def setter(self, x):
            components = list(self.sprite.color)
            components[i] = int(x * 255)
            self.sprite.color = components
        return setter

    r = property(_colorComponentGetter(0), _colorComponentSetter(0))
    g = property(_colorComponentGetter(1), _colorComponentSetter(1))
    b = property(_colorComponentGetter(2), _colorComponentSetter(2))
    
    def _setOpacity(self, x): self.sprite.opacity = int(x*255.0)
    def _getOpacity(self): return self.sprite.opacity/255.0
    opacity = property(_getOpacity, _setOpacity)
            
    def draw(self):
        glMatrixMode(gl.GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.x, self.y+self.h, 0);
        glScalef(float(self.w) / float(self.sprite.width), -float(self.h) / float(self.sprite.height), 1);
        self.sprite.draw()
        glPopMatrix()
    
    
class Text(ColoredVisible):
    def __init__(self, p, name, x=0, y=0, h=0, color="#00ff00", opacity=1.0, text=None, font=None):
        self.label = pyglet.text.Label(
            text if text != None else name,
            font_name=font if font != None else "Helvetica",
            font_size=h,
            anchor_y = 'center',
            x=0, y=0)
        
        ColoredVisible.__init__(self, p, name, x, y, self.label.content_width, h, color, opacity)

    def _colorComponentGetter(i):
        def getter(self): 
            self.label.color[i]/255.0
        return getter
        
    def _colorComponentSetter(i):
        def setter(self, x):
            components = list(self.label.color)
            components[i] = int(x * 255)
            self.label.color = components
        return setter
        
    r = property(_colorComponentGetter(0), _colorComponentSetter(0))
    g = property(_colorComponentGetter(1), _colorComponentSetter(1))
    b = property(_colorComponentGetter(2), _colorComponentSetter(2))
    opacity = property(_colorComponentGetter(3), _colorComponentSetter(3))

    def _setText(self, t): self.label.text = t
    def _getText(self): return self.label.text
    text = property(_getText, _setText)

    def _setFont(self, x): self.label.font_name = x
    def _getFont(self): return self.label.font_name
    font = property(_getFont, _setFont)

    def draw(self):
        glMatrixMode(gl.GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.x, self.y + self.h, 0);
        glScalef(float(self.w) / float(self.label.content_width), -float(self.h) / float(self.label.font_size), 1);
        self.label.draw()
        glPopMatrix()

class ClippingContainer(Visible):
    instanceCount = 0

    def __init__(self, p, name, x=0, y=0, w=10, h=10, ox=0, oy=0, clip=True):
        Visible.__init__(self, p, name, x, y, w, h)
        self.ox = ox
        self.oy = oy
        self.clip = clip

    def _getOffset(self): return (self.ox, self.oy)
    def _setOffset(self, value): self.ox, self.oy = value     
    offset = property(_getOffset, _setOffset)

    def draw(self):
        if self.clip:
            self.drawClipped()
        else:
            self.drawUnclipped()

    def drawUnclipped(self):
        pass

    def drawClipped(self):
        # get screen coordinates of lower left corner
        x = self.x
        y = self.y + self.h

        model_view_matrix = (GLdouble * 16)() 
        projection_matrix = (GLdouble * 16)() 
        viewport = (GLint * 4)() 
        glGetDoublev(GL_MODELVIEW_MATRIX, model_view_matrix)
        glGetDoublev(GL_PROJECTION_MATRIX, projection_matrix)
        glGetIntegerv(GL_VIEWPORT, viewport)
        s_x, s_y, s_z = GLdouble(), GLdouble(), GLdouble()

        gluProject(x, y, 0.0, model_view_matrix, projection_matrix, viewport, s_x, s_y, s_z)

        scissor_was_enabled = glIsEnabled(GL_SCISSOR_TEST)
        
        old_scissor  = (GLint*4)();
        r = ((int(s_x.value), int(s_y.value)), self.extent)
        if scissor_was_enabled:
            glGetIntegerv(GL_SCISSOR_BOX, old_scissor);
            osr = (old_scissor[0:2], old_scissor[2:4])
            r = clip_rect(r, osr)
        glScissor(*[int(x) for x in flatten_rect(r)])

        glEnable(GL_SCISSOR_TEST)

        self.drawUnclipped()

        if not scissor_was_enabled:
            glDisable(GL_SCISSOR_TEST)
        else:
            glScissor(old_scissor[0], old_scissor[1], old_scissor[2], old_scissor[3])
            
                          
class Group(ClippingContainer):
    instanceCount = 0
    
    def __init__(self, p, name, x=0, y=0, w=10, h=10, ox=0, oy=0, clipChildren=True):
        self._W, self._H = w, h
        ClippingContainer.__init__(self, p, name, x, y, w, h*2 if hasattr(self,'fg') else h, ox, oy, clipChildren)     
        
        self.__children__ = []

    def __addChild__(self, c):
        if not c in self.__children__:
            self.__children__.append(c)
    
    def __removeChild__(self, c):
        self.__children__.remove(c)
        
    def __iter__(self):
        return self.__children__.__iter__()
   
    def __len__(self):
        return len(self.__children__)
     
    def drawUnclipped(self):
        glMatrixMode(gl.GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.x - self.ox, self.y - self.oy, 0);
        for x in self:
            x.draw()
        glPopMatrix()
        
    ## W TODO: this isn't nice stuff ...
    def _getW(self): return self._W
    def _setW(self, value):
        if self._W == value: return
        self._W = value
        #print value
        self.doLayout(self._W, self._H)
    w = property(_getW, _setW)

    ## H
    def _getH(self): return self._H
    def _setH(self, value): 
        self._H = value
        if self._H == value: return
        self.doLayout(self._W, self._H)
    h = property(_getH, _setH)

    ## EXTENT
    def _getExtent(self): return (self._W, self._H)
    def _setExtent(self, value): 
        if (self._W, self._H) == value: return
        self._W, self._H = value
        self.doLayout(self._W, self._H)
    extent = property(_getExtent, _setExtent)

    def doLayout(self, w, h):
        pass

class Viewport(ClippingContainer):
    instanceCount = 0

    def __init__(self, p, name, x=0, y=0, w=10, h=10, ox=0, oy=0, world = None):
        ClippingContainer.__init__(self, p, name, x, y, w, h, ox, oy, True)     
        self.world = world 

    def drawUnclipped(self):
        if not self.world: return
        glMatrixMode(gl.GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.x - self.ox, self.y - self.oy, 0);
        self.world.draw()
        glPopMatrix()

##  TODO: refactor properties speed, t, progress, duration into common base class
class Video(Image):
    def __init__(self, p, name, path, x=0, y=0, w=None, h=None, color="#ffffff", opacity=1.0):
        self.player = Player()
        self.source = load(path.encode(sys.getfilesystemencoding()))
        self.player.queue(self.source)
        image = self.player.texture
        self.sprite = pyglet.sprite.Sprite(image)
        Image.__init__(self, p, name, None, x, y, w, h, color, opacity)
    
    def __del__(self):
        self.speed=0
        
    def getT(self): return self.player.time
    def setT(self, x): 
        playing = self.player.playing
        self.player.seek(x)
        if playing: self.player.play()
    t = property(getT, setT)

    def getDuration(self):
        return self.source.duration
    duration = property(getDuration, None)
    
    def getProgress(self): return self.player.time/self.source.duration
    def setProgress(self, p): 
        playing = self.player.playing
        self.player.seek(p*self.source.duration)
        if playing: self.player.play()
        
    progress = property(getProgress, setProgress)
    
    def getSpeed(self): 
        if self.player.playing:
            return self.player.pitch
        else:
            return 0.0
    def setSpeed(self, s):
        if s == 0.0:
            if self.player.playing:
                self.player.pause()
        elif not self.player.playing:
            self.player.pitch = s
            self.player.play()
    speed = property(getSpeed, setSpeed)
        
class Sound(object):
    _globalVolume = 1.0
    _allSounds = []
    
    @staticmethod
    def setGlobalVolume(v):
        Sound._globalVolume = v
        for w in Sound._allSounds:
            s = w()
            if s != None:
                s._setAbsoluteVolume(v * s._volume)
    
    def __init__(self, device, path):
        self.player = Player()
        self.source = load(path.encode(sys.getfilesystemencoding()))
        self.player.queue(self.source)
        self.id = len(self._allSounds)
        self._allSounds.append(weakref.ref(self))
        self.volume = 1.0

    def __del__(self):
        self.speed=0
        del self._allSounds[self.id]

    def getT(self): return self.player.time
    def setT(self, x): self.player.seek(x)
    t = property(getT, setT)

    def getDuration(self):
        return self.source.duration
    duration = property(getDuration, None)
    
    def getProgress(self): return self.player.time/self.source.duration
    def setProgress(self, p): self.player.seek(p*self.source.duration)
    progress = property(getProgress, setProgress)
    
    def getSpeed(self): 
        if self.player.playing:
            return self.player.pitch
        else:
            return 0.0
    def setSpeed(self, s):
        if s == 0.0:
            if self.player.playing:
                self.player.pause()
        elif not self.player.playing:
            self.player.pitch = s
            self.player.play()
    speed = property(getSpeed, setSpeed)
    
    def _setAbsoluteVolume(self, v):
        self.player.volume = v
    
    def setVolume(self, v):
        self._volume = v
        self._setAbsoluteVolume(self._volume * self._globalVolume)
    def getVolume(self):
        return self._volume
    volume = property(getVolume, setVolume)
    
##
# Regression Tests
##
import unittest
from test import test_support

class TestVisuals(unittest.TestCase):
    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_Group(self):
        v = Visible(None, "test1")
        assert(Visible.instanceCount == 1)
        assert(v.parent == None)
        assert(getrefcount(v) == 2)
        del v
        assert(Visible.instanceCount == 0)

        v = Visible(None, "test1")
        assert(Visible.instanceCount == 1)
        assert(v.parent == None)
        assert(getrefcount(v) == 2)

        g = Group(None, "group")
        assert(Group.instanceCount == 1)
        assert(Visible.instanceCount == 1)
        assert(g.parent == None)
        assert(len(g)==0)

        v.parent = g
        assert(getrefcount(v) == 3)
        assert(g.parent == None)
        assert(v.parent == g)
        assert(len(g)==1)
        for x in g: assert(x==v)

        del v
        for x in g: assert(getrefcount(x) == 3)

        assert(Visible.instanceCount == 1)

        for x in g: assert(x.parent==g)

        for x in g: x.parent = None
        del x
        assert(len(g)==0)
        assert(Visible.instanceCount == 0)
        
        g.ox=10
        g.oy=20
        assert(g.offset==(10,20))
        g.offset = (20,40)
        assert(g.ox==20)
        assert(g.oy==40)

    def test_color_properties(self):
        r = Rect(None, "Rect")
        r.color = "#ff7f00"
        assert(r.r==1.0)
        assert(r.g==0x7f/255.0)
        assert(r.b==0)
        r.b = 10/255.0
        assert(r.color == "#FF7F0A")

    def test_basic_properties(self):
        r = Rect(None, "Rect")
        r.x=10
        r.y=20
        assert(r.position==(10,20))
        r.position = (20,40)
        assert(r.x==20)
        assert(r.y==40)
        
        r.w=10
        r.h=20
        assert(r.extent==(10,20))
        r.extent = (20,40)
        assert(r.w==20)
        assert(r.h==40)
        assert(r.contains(20,40)==True)
        assert(r.contains(19,40)==False)
        assert(r.contains(20,39)==False)
        assert(r.contains(20+20,40+40)==False)
        assert(r.contains(20+19,40+39)==True)


def test_main():
    test_support.run_unittest(
        TestVisuals,
        #... list other tests ...
    )
                 
if __name__ == "__main__":
    # run some tests on Node hierarchy
    test_main()
    
    