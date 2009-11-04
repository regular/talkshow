import os
import math
from wrappers import *
from widget import *
import glob

import pyglet
from delayed_call import *
import animated_property
import time

def normalizePath(path):
    path = path.replace("\\", "/")
    while "//" in path:
        path = path.replace("//", "/")
    return path

def clamp(v, low=0.0, high=1.0):
    if v>high: v = high
    if v<low: v = low
    return v

class Field(Widget):    
    def __init__(self, parent, x, y, w, h, text):
        Widget.__init__(self, parent, "Field", w = w, h = h, x = x, y = y)
        border = self.border = Rect(self, "border", 0, 0, w, h)        
        border.opacity=0
        bg = self.bg = Rect(self, "bg", 1, 1, w-2, h-2)        
        bg.color = "#7f7f7f"
        l = self.label = Label(self, "label", x=20, y=20, size=h/5, text=text)        
        self.PROGRESS = 0

    def startHighlight(self):
        self.border.animate("opacity", 1, 0, 0, 125)

    def doLayout(self, new_w, new_h):
        self.border.extent = new_w, new_h
        self.bg.extent = new_w-2, new_h-2        
        self.label.size = new_h/5
        if hasattr(self, "icon"):
            self.icon.x = (self.w - self.icon.w) / 2.0
            self.icon.y = (self.h - self.icon.h) / 2.0

    def _getTEXT(self):
        return self.label.text
    def _setTEXT(self, t):
        self.label.text = t        
    text = property(_getTEXT, _setTEXT)
    
    def _getCOLOR(self):
        return self.bg.color            
    def _setCOLOR(self, c):        
        self.bg.color = c
    color = property(_getCOLOR, _setCOLOR)
    
    def _getPROGRESS(self):
        return self.PROGRESS        
    def _setPROGRESS(self, p):
        self.PROGRESS = p
        self.label.progress = clamp((p - 0.5) / 0.5)        
        box_progress = clamp(p / 0.5)
        
        self.bg.w = (self.w-2) * box_progress
        self.bg.h = (self.h-2) * box_progress
        self.bg.x = 1+ (self.w-2)/2 - ((self.w-2)/2 * box_progress)
        self.bg.y = 1+ (self.h-2)/2 - ((self.h-2)/2 * box_progress)
           
        self.bg.opacity = box_progress          
        if hasattr(self, "icon"): self.icon.opacity = box_progress
    progress = property(_getPROGRESS, _setPROGRESS)


    def _getOPACITY(self):
        return self.bg.opacity
    def _setOPACITY(self, o):        
        self.bg.opacity = o        
    opacity = property(_getOPACITY, _setOPACITY)

class Grid(Widget):
    instanceCount = 0
    
    def __init__(self, parent, fieldCount, delegate):
        Widget.__init__(self, parent, "Grid", w = parent.w, h = parent.h)
        self.delegate = delegate
        self.fields = []
        cols = round(math.sqrt(fieldCount) * 1) #parent.w / parent.h)
        rows = fieldCount / cols
        if rows != int(rows):
            rows += 1

        rows = int(rows)
        cols = int(cols)
        #print cols, rows

        w = int(parent.w / cols)
        h = int(parent.h / rows)

        i = 0
        for r in range(rows):
            for c in range(cols):
                if i < fieldCount:
                    field = Field(self, w=w-4, h=h-4, x=w*c, y=h*r, text=delegate.getFieldText(i))
                    icon = delegate.getFieldIcon(i)
                    if icon != None:
                        field.icon = icon
                        icon.parent = field  
                        field.doLayout(field.w, field.h)                      
                    field.animate("progress", 0, 1, 0, 250)
                    field.color = "#%2X%2X00" % (int(255 * (c+1)/cols), int(255 * (r+1)/rows))
                    field.index = i
                    self.fields.append(field)
                    i += 1
                    
    def onMouseButtonDown(self, button, x, y):
        field = None
        for f in self:
            if f.contains(x,y):
                field = f
        
        if field != None:
            self.delegate.onFieldClicked(field)

    def enterFIeld(self, field):
        if field != None:
            for f in self:
                if f != field:
                    f.animate("progress", f.progress, 0, 0, 250)
            field.startHighlight()
            field.animate("x", field.x, 0, 125, 250)
            field.animate("y", field.y, 0, 125, 250)
            field.animate("w", field.w, self.w, 125, 250)
            field.animate("h", field.h, self.h, 125, 250)
            field.animate("opacity", field.opacity, 0, 250, 250)
        
       
class Talkshow(Widget):
    def __init__(self, screen):
        Widget.__init__(self, screen, "Talkshow", w=screen.w, h=screen.h)     
        self.bg = Rect(self, "bg", w=self.w, h=self.h-100, color = "#000000")
        self.gridContainer = Widget(self, "gridContainer", w = self.w - 20, h=self.h-20-100, x=10, y=10)
        
        b = self.backButton = Button(self, "backbutton", 20, self.h - 100 + 20, 100, 50, handler = self.back, text='<<')        
        self.homeButton = Button(self, "homebutton", self.w/2 - 100 , self.h - 100 + 20, 200, 50, handler = self.home, text="Start")
        self.volumeSlider = Slider(self, "volume", self.w - 200 - 20 , self.h - 100 + 20, 200, 50, action = self.setVolume)
        self.volumeSlider.knobPosition = 0.75
        
        self.count = 9        
        
        self.pathPrefix = "./Content/"
        self.path= ""
        self.grid = None
        self.gridFromPath()
        #self.newGrid()
        
        l = self.label = Label(self, "title", x=20, y=20, size=50, text = "KommHelp Talkshow", color = "#0030ff")        
        #l.animate("progress", 0, 1, 0, 3000)
    
    def getFieldText(self, i):
         return self.items[i]
        
    def pathForField(self, i):
        path = self.path + "/" + self.items[i]
        if path[0] == "/": path = path[1:]
        return path
             
    def getFieldIcon(self, i):
        path = self.pathForField(i)
        return self.iconForPath(self.pathPrefix + path)
         
    def onFieldClicked(self, f):        
        if f != None:
            if f.index<len(self.items):
              subfields = self.subdirs(self.pathPrefix, self.pathForField(f.index))
              print "subfields", subfields
              if len(subfields)>0:
                  #self.path = self.pathForField(f.index)     

                  self.grid.enterFIeld(f)
                  self.bg.animate("color", self.bg.color, f.color, 0, 500)
                  self.dc = DelayedCall(self.gridFromPath, 500, (f.color, self.pathForField(f.index)))
              self.playPath(self.pathPrefix + self.pathForField(f.index))
    
    def iconForPath(self, path):
        #print path
        images = glob.glob(path+"/*.png")
        if images:
            path = normalizePath(images[0])
            #print path
            i = Image(None, path, path)
            return i
        return None
        
    
    def playPath(self, path):
        sounds = glob.glob(path+"/*.wav")
        print "sounds", sounds
        if sounds:
            path = normalizePath(sounds[0])
            #print path
            r = Resource(path)
            print r._obj.details

            r = r.find("sound0")
            #print r._obj.details
            if r != None:
                s = self.sound  = tubifex.Sound(0, r._obj)
                s.speed=1
            else:
                print "Unable to decode wav"
            
        
    def setVolume(self, v):
        print "Volume", v
        #tubifex.volume = v
        
    def back(self):
        l = self.path.split("/")
        if l:
            self.path= "/".join(l[:-1])
            self.gridFromPath()
  
    def home(self):
        l = self.path = ""
        self.gridFromPath()  
              
    def subdirs(self, prefix, path):
        items = os.listdir(prefix+path)        
        items =  filter(lambda x: os.path.isdir(prefix + path + "/" + x), items)            
        #print items
        return items
                
    def gridFromPath(self, color_and_path = None):
        path = ""
        color="#000000"
        if color_and_path:
            color, path = color_and_path
        
        print self.pathPrefix+ path
        self.path = path
        #print items
        self.items =  self.subdirs(self.pathPrefix, self.path)
        print self.items
        self.count = len(self.items)
        if self.count:
            self.newGrid(color)
        
    def newGrid(self, color="#000000"):
        self.bg.color=color
        if self.grid != None:
            self.grid.parent = None
        self.grid = Grid(self.gridContainer, self.count, self)
        print "instanceCount", Grid.instanceCount

    def key_sink(self, k):
        if k=="+":
            self.count += 1
            self.newGrid()
        if k=="-":
            self.count -= 1
            self.newGrid()


#environment.set("character_spacing", -2)                    

screen = Screen("Talkshow", "", 800, 600)
talkshow = Talkshow(screen)

#tubifex.keyboard_sink = talkshow.key_sink
screen.event_handler = talkshow

# boilerplate
def tick():
    animated_property.T = time.time()*1000
    animated_property.AnimatedProperty.tick()
    return True
    
pc = PeriodicCall(tick,0)
pyglet.app.run()