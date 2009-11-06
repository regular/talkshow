from round_rect import RoundRect
from wrappers import *
   
class Widget(Group):
    def __init__(self, p, name, x = 0, y = 0, w = 10, h = 10, ox = 0, oy = 0):
        Group.__init__(self, p, name, x, y, w, h, ox, oy)
        self.mouseOwner = None
    
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
            for child in self:
                if child.contains(x, y):
                    if hasattr(child, "onMouseButtonDown"):
                        child.onMouseButtonDown(button, x - child.x, y - child.y)
                    
    def onMouseButtonUp(self, button, x, y):
        if self.mouseOwner != None:
            self.mouseOwner.onMouseButtonUp(button, x, y)
        else:
            for child in self:
                if child.contains(x, y):
                    if hasattr(child, "onMouseButtonUp"):
                        child.onMouseButtonUp(button, x - child.x, y - child.y)
                    
    def onMouseMove(self, x, y):
        if self.mouseOwner != self:
            for child in self:
                if hasattr(child, "onMouseMove"):
                    child.onMouseMove(x - child.x, y - child.y)
        else:
            for child in self:
                if child.contains(x, y):
                    if hasattr(child, "onMouseMove"):
                        child.onMouseMove(x - child.x, y - child.y)
                        

class Label(Widget):
    FONT = "Helvetica"
    WEIGHT = -100
    def __init__(self, parent, name, x, y, size, text=None, font=None, color="#ffffff"):
        self.shadow = Text(None, "shadow", 2, 2, h=size, text=text if text else name, color="#000000", opacity = 0.4, font=font if font else self.FONT) 
        self.fg = Text(None, "text", 0,0, h=size, text=text if text else name, color=color, opacity=0.9,font=font if font else self.FONT) 

        Widget.__init__(self, parent, name, x = x, y = y, w = self.shadow.w + 2, h = self.shadow.h + 2)
        self.shadow.parent = self.fg.parent = self

    def doLayout(self, w, h):
        self.shadow.w = self.fg.w = w - 2
        self.shadow.h = self.fg.h = h - 2
        
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

                   
class DefaultSettings:
    inner_radius = 30
    outer_radius = 32
    
    shadow_offset = 7
    shadow_blur = 15
    
    border_thickness = 2
    border_color= "#000000"
    
    bevel_size = 6
    highlight_amount = 0.1
    lowlight_amount = 0.3
    
    color="#3030c0"

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
        

class EngraveSettingsOuter:
    inner_radius = 14
    outer_radius = 16
    
    shadow_offset = 0
    shadow_blur = 15
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 4
    highlight_amount = -0.3
    lowlight_amount = -0.3
    
    color="#6f6f6f"

class EngraveSettingsInner:
    inner_radius = 1
    outer_radius = 2
    
    shadow_offset = 0
    shadow_blur = 15
    
    border_thickness = 0
    border_color= "#000000"
    
    bevel_size = 2
    highlight_amount = -0.1
    lowlight_amount = -0.1
    
    color="#4f4f4f"

class KnobSettings:
    inner_radius = 10
    outer_radius = 12
    
    shadow_offset = 5
    shadow_blur = 4
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 2
    highlight_amount = 0.1
    lowlight_amount = 0.3
    
    color="#c0c0c0"

class BarSettings:
    inner_radius = 12
    outer_radius = 14
    
    shadow_offset = 4
    shadow_blur = 4
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 4
    highlight_amount = 0.1
    lowlight_amount = 0.3
    
    color="#c0c0c0"
    
class HighlightBarSettings(BarSettings):
    inner_radius = 12
    outer_radius = 14
    
    shadow_offset = 2
    shadow_blur = 2
    
    border_thickness = 1
    border_color= "#c0c0c0"
    
    bevel_size = 4
    highlight_amount = 0.2
    lowlight_amount = 0.3
    
    color="#c0c0f0"

class Scrollbar(Widget):
    def __init__(self, parent, name, x, y, w, h, action=None):
        Widget.__init__(self, parent, name, x, y, w, h)        
        self.outline = Box(self, "outline", w, h, s = EngraveSettingsOuter)        
        b = self.bar = Box(self, "bar", w/2, 39, s=BarSettings)
        b.x, b.y = 2,2
        self.dragOrigin = None
        self.action = action
        self.value = None
        self.minmax = (2, self.outline.x + self.outline.w - self.bar.w + 2)
       
    def onMouseButtonDown(self, button, x, y):
        print "Scrollbar click at ", x, y
 
        if x > self.bar.x + self.bar.w:
            self.bar.x += self.bar.w
            self.enforceConstrains()
        elif x < self.bar.x:
            self.bar.x -= self.bar.w
            self.enforceConstrains()
        elif x > self.bar.x and x < self.bar.x + self.bar.w:
            self.captureMouse()
            self.originalBarX = self.bar.x
            self.dragOrigin = x
    
    def onMouseButtonUp(self, button, x, y):
        self.dragOrigin = None
        self.releaseMouse()
        
    def onMouseMove(self, x, y):
        if self.dragOrigin != None:
            self.bar.x = self.originalBarX + x - self.dragOrigin
            self.enforceConstrains()

    def enforceConstrains(self):
        b = self.bar
        minx, maxx = self.minmax
        if b.x < minx: b.x = minx
        if b.x > maxx: b.x = maxx
        value = float(b.x - minx) / (maxx - minx)
        if value != self.value:
            if self.action != None:
                self.action(value)
            self.value = value 
            
    def setValue(self, v):
        minx, maxx = self.minmax
        self.bar.x = int(minx + (maxx - minx) * v)
        self.enforceConstrains()

    def getValue(self):
        return self.value
        
    knobPosition = property(getValue, setValue)

class Slider(Scrollbar):
    def __init__(self, parent, name, x, y, w, h, action = None):
        Scrollbar.__init__(self, parent, name, x, y, w, h, action)        
        self.outline = Box(self, "outline", w, h, s = EngraveSettingsOuter)
        t = self.track = Box(self, "track", w*3/4, 8, s = EngraveSettingsInner)
        t.x = w / 8
        t.y = h /2 - 4
        k = self.bar = Box(self, "knob", 33, 33, s=KnobSettings)
        k.x = t.x - 15
        k.y = t.y - 12
        self.minmax = (self.track.x - 15, self.track.x + self.track.w - self.bar.w + 2 + 15 )


class Button(Widget):
    def __init__(self, parent, name, x, y, w, h, text="button", handler = None):
        Widget.__init__(self, parent, name, x, y, w, h)        
        self.handler = handler
        self.container = Widget(self, "container", 0,0, self.w, self.h)
        self.outline = Box(self.container, "outline", w, h, s = EngraveSettingsOuter)        
        b = self.bar = Box(self.container, "bar", w, h, s=BarSettings)
        b.x, b.y = 1,1
        
        label = self.label = Label(self,  "label", 0, 0, size=h*2.2/4.0, text = text)
        label.x = (self.w - label.w) / 2
        label.y = (self.h - label.h) / 2 
        #label.text = text        
        label.progress=1
       
    def onMouseButtonDown(self, button, x, y):
        b = self.bar = Box(self.container, "bar", self.w-4, self.h-4, s=HighlightBarSettings)
        b.x, b.y = 3,3
        self.captureMouse()
         
    def onMouseButtonUp(self, button, x, y):
        b = self.bar = Box(self.container, "bar", self.w, self.h, s=BarSettings)
        b.x, b.y = 1,1
        if self.handler != None:
            self.handler()
        self.releaseMouse()
       
class LEDSettings:
    inner_radius = 10
    outer_radius = 12
    
    shadow_offset = 6
    shadow_blur = 8
    
    border_thickness = 1
    border_color= "#000000"
    
    bevel_size = 3
    highlight_amount = 0.5
    lowlight_amount = 0.3
    
    color="#10a010"

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
      