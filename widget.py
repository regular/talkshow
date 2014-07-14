from round_rect import RoundRect
import wrappers
from wrappers import Group, Text, splitColorChannels, mergeColorChannels, Video, style, Image
from delayed_call import *

from styleSettings import *

import talkshowConfig
conf = talkshowConfig.config()
import talkshowUtils

style = conf.style
mydict = conf.parser.dict
   
class Widget(Group):
    def __init__(self, p, name, x = 0, y = 0, w = 10, h = 10, ox = 0, oy = 0):
        Group.__init__(self, p, name, x, y, w, h, ox, oy)
        self.mouseOwner = None
    
    def reverseIterator(self):
        childrencopy = list(self.__children__)
        childrencopy.reverse()
        return childrencopy.__iter__()
    
    def captureMouse(self):
        self._captureMouse(self)

    def releaseMouse(self):
        self._captureMouse(None)
    
    def _captureMouse(self, newOwner):
        self.mouseOwner = newOwner
        if hasattr(self.parent, "_captureMouse"):
            if newOwner != None:
                self.parent._captureMouse(self)
            else:
                self.parent._captureMouse(None)

    def onMouseButtonDown(self, button, x, y):
        if self.mouseOwner != None:
            self.mouseOwner.onMouseButtonDown(button, x, y)
        else:
            for child in self.reverseIterator():
                if child.contains(x, y):
                    if hasattr(child, "onMouseButtonDown"):
                        child.onMouseButtonDown(button, x - child.x, y - child.y)
                        break
                    
    def onMouseButtonUp(self, button, x, y):
        if self.mouseOwner != None:
            self.mouseOwner.onMouseButtonUp(button, x, y)
        else:
            for child in self.reverseIterator():
                if child.contains(x, y):
                    if hasattr(child, "onMouseButtonUp"):
                        child.onMouseButtonUp(button, x - child.x, y - child.y)
                        break
                    
    def onMouseMove(self, x, y):
        if self.mouseOwner != self:
            for child in self.reverseIterator():
                if hasattr(child, "onMouseMove"):
                    child.onMouseMove(x - child.x, y - child.y)
        else:
            for child in self.reverseIterator():
                if child.contains(x, y):
                    if hasattr(child, "onMouseMove"):
                        child.onMouseMove(x - child.x, y - child.y)
                        

class Label(Widget):
    #FONT = "Helvetica"
    #WEIGHT = -100
    def __init__(self, parent, name, x, y, size, text=None, font=None, color="#ffffff", font_size=None):
        #self.shadow = Text(None, "shadow", 2, 2, h=size*0.75, text=text if text else name, color="#000000", opacity = 0.4, font=font if font else self.FONT)
        #self.fg = Text    (None, "text",   0, 0, h=size*0.75, text=text if text else name, color=color, opacity=0.9,font=font if font else self.FONT) 
        
        #Widget.__init__(self, parent, name, x = x, y = y, w = self.shadow.w + 2, h = self.shadow.h + 2)
        self.FONT = "Helvetica"
        try:  self.FONT = style.boxLabel.font_family.split(',')[0]
        except: pass
        
        self.WEIGHT = -100
        
        try:  self.col = style.boxLabel.color
        except: pass
        
        if font_size:
            self.font_size = font_size
        else:            
            try: self.font_size = int(style.boxLabel.font_size.replace('px',''))
            except: self.font_size = conf.FONT_SIZE_DEFAULT
        
        #self.shadow = Text(None, "shadow", 2, 2, h=size, text=text if text else name, color=self.col, opacity = 0.4, font=font if font else self.FONT) 
        self.fg = Text(None, "text", 0,0, h=self.font_size, text=text if text else name, color=self.col, opacity=1,font=font if font else self.FONT) 
        self.shadow = self.fg
        
        #Widget.__init__(self, parent, name, x = x, y = y, w = self.shadow.w + 2, h = self.shadow.h + 2)
        Widget.__init__(self, parent, name, x = x, y = y, w = self.shadow.w , h = size)
        self.shadow.parent = self.fg.parent = self

    def doLayout(self, w, h):
        debug("doLayout? unnecessary. not doing anything.")
#        self.shadow.w = self.fg.w = w - 2
#        self.shadow.h = self.fg.h = h - 2
        
    def _getTEXT(self):
        return self.fg.text
    def _setTEXT(self, t):
        self.shadow.text = t
        self.fg.text = t
    text = property(_getTEXT, _setTEXT)
    
    def _getCOLOR(self):
        return self.fg.color            
    def _setCOLOR(self, c):        
        self.fg.color = c
    color = property(_getCOLOR, _setCOLOR)

    def getOpacity(self):
        return self.fg.opacity
    def setOpacity(self, c):        
        self.fg.opacity = c
        self.shadow.opacity = c
    progress = color = property(getOpacity, setOpacity)


class Box(Group):
    def __init__(self, parent, name, w, h, s = DefaultSettings):
        Group.__init__(self, parent, name, w=w, h=h)        
        self.settings = s
        
        if s.shadow_offset>0:
            self.shadow = RoundRect(
                self, 
                "shadow", 
                s.shadow_offset, s.shadow_offset, 
                w, h, 
                s.inner_radius - s.shadow_blur, s.outer_radius, 
                color="#000000")
        else:
            self.shadow = None
                
        if s.border_thickness>0:
            self.border = RoundRect(
                self, 
                "border", 
                0, 0, 
                w, h, 
                s.inner_radius, s.outer_radius, 
                color=s.border_color)
        else:
            self.border = None

        self.highlight = RoundRect(
            self, 
            "highlight", 
            s.border_thickness, s.border_thickness, 
            w,h,
            s.inner_radius-s.border_thickness, s.outer_radius-s.border_thickness, 
            color=self.mixColor(s.color, "#ffffff", s.highlight_amount))
            
        self.lowlight = RoundRect(
            self, 
            "lowlight", 
            s.border_thickness + 1* s.bevel_size, s.border_thickness + 1* s.bevel_size, 
            w,h,
            s.inner_radius-s.border_thickness, s.outer_radius-s.border_thickness, 
            color=self.mixColor(s.color, "#000000", s.lowlight_amount))

        self.main = RoundRect(
            self, 
            "border", 
            #s.border_thickness + s.bevel_size, s.border_thickness + s.bevel_size, 
            s.border_thickness, s.border_thickness, 
            w,h,
            s.inner_radius-s.border_thickness, s.outer_radius-s.border_thickness + s.bevel_size, 
            color=s.color)

        self.doLayout(w, h)


    def mixColor(self, c1, c2, amount):
        r1, g1, b1 = splitColorChannels(c1)
        r2, g2, b2 = splitColorChannels(c2)
        
        r = int(r1 + float(r2 - r1) * amount)
        g = int(g1 + float(g2 - g1) * amount)
        b = int(b1 + float(b2 - b1) * amount)
        
        return mergeColorChannels(r, g, b)

    def doLayout(self, w, h):
        s = self.settings
        w -= s.shadow_offset
        h -= s.shadow_offset
        
        if self.shadow: self.shadow.extent = w, h
        if self.border: self.border.extent = w, h
        
        #self.main.extent = w-2 * s.border_thickness - 2 * s.bevel_size, h-2 * s.border_thickness - 2 * s.bevel_size         
        self.main.extent = w-2 * s.border_thickness, h-2 * s.border_thickness
        self.highlight.extent = self.main.extent
        self.lowlight.extent = self.main.w-s.bevel_size, self.main.h - s.bevel_size
        


class Scrollbar(Widget):
    def __init__(self, parent, name, x, y, w, h, action=None):
        Widget.__init__(self, parent, name, x, y, w, h)        
        self.outline = Box(self, "outline", w, h, s = EngraveSettingsOuter)        
        b = self.bar = Box(self, "bar", 39, h/2, s=BarSettings)
        b.x, b.y = 2,2
        self.dragOrigin = None
        self.action = action
        self.value = None
        self.minmax = (self.outline.y + self.outline.h - self.bar.h + 2,2)
       
    def onMouseButtonDown(self, button, x, y):
        
        if y > self.bar.y + self.bar.h:
            self.bar.y += self.bar.h
            self.enforceConstrains()
        elif y < self.bar.y:
            self.bar.y -= self.bar.h
            self.enforceConstrains()
        elif y > self.bar.y and y < self.bar.y + self.bar.h:
            self.captureMouse()
            self.originalBarY = self.bar.y
            self.dragOrigin = y
    
    def onMouseButtonUp(self, button, x, y):
        self.dragOrigin = None
        self.releaseMouse()
        
    def onMouseMove(self, x, y):
            
        if self.dragOrigin != None:
            self.bar.y = self.originalBarY + y - self.dragOrigin
            self.enforceConstrains()

    def enforceConstrains(self):
            
        b = self.bar
        miny, maxy = self.minmax
        if b.y < miny: b.y = miny
        if b.y > maxy: b.y = maxy
        value = 1.0 - (float(b.y - miny) / (maxy - miny))
        if value != self.value:
            if self.action != None:
                self.action(value)
            self.value = value  
            
            
    def setValue(self, v):
        miny, maxy = self.minmax
        self.bar.y = int(miny + (maxy - miny) * v)
        self.enforceConstrains()

    def getValue(self):
        return self.value
        
    knobPosition = property(getValue, setValue)

class Slider(Scrollbar):
    def __init__(self, parent, name, x, y, w, h, action = None):
        Scrollbar.__init__(self, parent, name, x, y, w, h, action)        
        self.outline = Box(self, "outline", w, h, s = EngraveSettingsOuter)
        
        t = self.track = Box(self, "track", 8, h*3/4, s = EngraveSettingsInner)
        t.y = h / 8
        t.x = w /2 - 4
        
        k = self.bar = Box(self, "knob", 33, 33, s=KnobSettings)
        k.x = t.x - 12
        k.y = t.y - 15
        
        self.minmax = (self.track.y - 15, self.track.y + self.track.h - self.bar.h + 2 + 15)


class Videoplayer(Widget):
    def __init__(self, parent, name, filepath, x, y, w, h):
        Widget.__init__(self, parent, name, x, y, w, h)        
        self.video = Video(self, "video", filepath, x=0, y=0)
        self.video.speed=1
        self.slider = Slider(self, "slider", 0,0,w,40, action=self.onSliderUpdate)
        self.doLayout(w,h)
        self.suppressUpdateHandlerCall = False
        self.updatePC = PeriodicCall(self.updateSlider, 0) 
    
    def unref(self):
        # break up circular references
        self.updatePC = None
        self.slider.action = None
    
    def onSliderUpdate(self, v):
        if not self.suppressUpdateHandlerCall:
            self.video.progress = v
    
    def updateSlider(self):
        self.suppressUpdateHandlerCall = True
        self.slider.knobPosition = self.video.progress
        self.suppressUpdateHandlerCall = False
        return True
        
    def doLayout(self, w, h):
        self.video.w = w
        self.video.h = h
        self.slider.w = w
        self.slider.y = h - self.slider.h
        
class Button(Widget):
    def __init__(self, parent, name, x, y, w, h, text="button", handler = None, imagePath=None):
        Widget.__init__(self, parent, name, x, y, w, h)        
        self.handler = handler
        
        self.text = text        
        self.container = Widget(self, "container", 0,0, self.w, self.h)
        #self.outline = Box(self.container, "outline", w, h, s = EngraveSettingsOuter)        
        b = self.bar = Box(self.container, "bar", w, h, s=BarSettings)
        
        b.x, b.y = 1,1
        
        if imagePath:
            
            #self, p, name, path, x=0, y=0, w=None, h=None, color="#ffffff", opacity=1.0
            self.image = wrappers.Image(self, name, talkshowUtils.getRelativePath(imagePath)) #self.style.home.background_image[5:-2]
            
        
        else:
        
            label = self.label = Label(self,  "label", 0, 0, size=h*2.2/4.0, text = text)
            label.x = (self.w - label.w) / 2
            label.y = (self.h - label.h) / 2 
            label.progress=1
       
    def onMouseButtonDown(self, button, x, y):
        self.bar.parent = None
        b = self.bar = Box(self.container, "bar", self.w, self.h, s=HighlightBarSettingsPressed)
        b.x, b.y = 3,3
        self.captureMouse()
         
    def onMouseButtonUp(self, button, x, y):
        self.bar.parent = None
        b = self.bar = Box(self.container, "bar", self.w, self.h, s=BarSettings)
        b.x, b.y = 1,1
        if self.handler != None:
            self.handler()
        self.releaseMouse()
        
#    def onMouseMove(self, x, y):
#        if x > 0 and  y > 0 and x < self.w  and y < self.h:
#            self.bar = Box(self.container, "bar", self.w, self.h, s=HighlightBarSettings)
#        else:
#            self.bar = Box(self.container, "bar", self.w, self.h, s=BarSettings)
#        
        
        
       

class LED(Group):
    def __init__(self, parent, name, x, y):
        Group.__init__(self, parent, name, x, y, 33, 33)        
        k = self.knob = Box(self, "led", 33, 33, s=LEDSettings)
        self.highlight= RoundRect(
                self, 
                "highlight", 
                3, 3, 
                12, 12, 
                3, 6, 
                color="#eeeeee")
                
        self.inner_glow= RoundRect(
                self, 
                "glow", 
                5, 5, 
                20, 18, 
                3, 9, 
                color="#a0ff50")
                
        self.outer_glow= RoundRect(
                self, 
                "glow", 
                0, 0, 
                33, 33, 
                0, 16, 
                color="#a0ff50")
                
        self.STATE = 1
                                
    def _setSTATE(self, s):
        self.STATE = s
        if s==0:
            self.outer_glow.hidden=1
            self.inner_glow.hidden=1
        if s==1:
            self.outer_glow.hidden=0
            self.inner_glow.hidden=0        
    def _getSTATE(self):
        return self.STATE        
    state = property(_getSTATE, _setSTATE)
    
    def toggle(self):
        self.state = 1-self.state
        return True
      