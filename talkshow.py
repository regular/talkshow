import os
import math
import glob


import wrappers
from wrappers import *
from widget import *

from delayed_call import *
import animated_property


# Constants #todo maybe put them elsewhere in the code.

COLUMNS = 2
MAX_ROW_NUMBER = 4

#from pyglet.media import avbin


#full screen mode can be set or unset in wrappers under the class "Screen" in the constructor



def popupErrorMessage(string):
    #TODO popup
    print string





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
        border = self.border = Rect(self, "border", 0, 0, w, h, color="#1f1f1f")        
        border.opacity=0
        bg = self.bg = Rect(self, "bg", 2, 2, w-4, h-4)        
        bg.color = "#7f7f7f"
        
        top_padding = style.box.padding[0]/100.0
        right_padding = style.box.padding[1]/100.0
        bottom_padding = style.box.padding[2]/100.0
        left_padding = style.box.padding[3]/100.0

        labelHeight = h*0.5 - top_padding*h - bottom_padding*h
       
        
        l = self.label = Label(self, "label", x=parent.x+parent.w*left_padding, y=parent.y+parent.h*top_padding, size=labelHeight, text=text)        
        self.PROGRESS = 0

    def startHighlight(self):
        #self.border.animate("opacity", 1, 0, 0, 250)
        self.bg.animate("opacity", 0, 1, 0, 250)

    def doLayout(self, new_w, new_h):
        self.border.extent = new_w, new_h
        self.bg.extent = new_w-4, new_h-4        
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
        
        self.bg.w = (self.w-4) * box_progress
        self.bg.h = (self.h-4) * box_progress
        self.bg.x = 2+ (self.w-4)/2 - ((self.w-4)/2 * box_progress)
        self.bg.y = 2+ (self.h-4)/2 - ((self.h-4)/2 * box_progress)
           
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
    
        if fieldCount == 1:
            cols = 1
        elif fieldCount == 0:
            popupErrorMessage("!ERROR: No field")
        
        # calculate number of rows and columns
        cols = int(COLUMNS)
        rows = int(math.ceil(fieldCount / (cols * 1.0))) # number of rows large enough for all elements. 
        if rows > MAX_ROW_NUMBER :
            rows = MAX_ROW_NUMBER # 8 is the maximum number of rows allowed.
            
        # calculate box heigth and width
        boxheight = {1:style.arrayRows1.height/100.0, 
                  2:style.arrayRows2.height/100.0, 
                  3:style.arrayRows3.height/100.0, 
                  4:style.arrayRows4.height/100.0, 
                  }  
        
        w = int(parent.w * style.box.width / 100.0)      
        if cols == 1:
            w = w * COLUMNS #full size if just one column
        if boxheight.has_key(rows):
            h = int(parent.h * boxheight[rows])
        else:
            h = parent.h / rows - 2 # to avoid crash of someone specifies more than 4 rows as max
        
        # calculate margin
        margin = style.box.margin /100.0

        i = 0
        # define box placement and content (text and icons)
        for r in range(rows):
            for c in range(cols):
                if i < fieldCount:
                    field = Field(self, w=w, h=h, x=(w+w*margin)*c, y=(h+h*margin)*r, text=delegate.getFieldText(i))
                    icon = delegate.getFieldIcon(i)
                    if icon != None:
                        field.icon = icon
                        icon.parent = field  
                        field.doLayout(field.w, field.h)      
                    field.progress=0                
                    field.animate("progress", 0, 1, 0, 250)
                    #field.color = "#%2X%2X00" % (int(255 * (c+1)/cols), int(255 * (r+1)/rows))
                    field.color = style.box.background_color
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
        print "enterFIeld", field
        if field != None:
            for f in self:
                if f != field:
                    f.animate("progress", f.progress, 0, 0, 250)
            
            delay = 125
            duration = 250
            field.animate("x", field.x, 0.0, delay, duration)
            field.animate("y", field.y, 0, delay, duration)
            field.animate("w", field.w, self.w, delay, duration)
            field.animate("h", field.h, self.h, delay, duration)
            field.animate("opacity", field.opacity, 0, delay+duration, duration)
            self.delegate.bg.animate("color", self.delegate.bg.color, field.color, delay+duration, duration)
            if hasattr(field, "icon"):
                field.icon.animate("opacity", field.opacity, 0, delay*2, duration)
                
       
class Talkshow(Widget):
    def __init__(self, screen):
        Widget.__init__(self, screen, "Talkshow", w=screen.w, h=screen.h)     
        self.bg = Rect(self, "bg",  w = self.w , h=self.h-100, x=0, y=40, color="#202020")
        #self.bg = Rect(self, "bg",  w = self.w , h=self.h-100, x=0, y=40, color=style.page.background_color)
        self.gridContainer = Widget(self, "gridContainer", w = self.w - 20, h=self.h-20-100, x=10, y=50)

        b = self.quitButton = Button(self, "quitbutton", self.w - 40, 0, 40, 40, handler = self.quit, text='X')        

        
        b = self.backButton = Button(self, "backbutton", 20, self.h - 100 + 50, 100, 50, handler = self.back, text='<<')        
        self.homeButton = Button(self, "homebutton", self.w/2 - 100 , self.h - 100 + 50, 200, 50, handler = self.home, text="Start")
       # self.homeButton = Button(self, "homebutton", self.w/2 - 100 , self.h - 100 + 50, 200, 50, handler = self.home, text="Start", image="")
        self.volumeSlider = Slider(self, "volume", self.w - 200 - 20 , self.h - 100 + 50, 200, 50, action = self.setVolume)
        self.volumeSlider.knobPosition = 1.0
        
        self.count = 9        
        
        # TODO: FIX in order to avoid crashes
        self.pathPrefix = "./Content/"
        self.path= ""
        self.grid = None
        self.videoplayer = None
        self.gridFromPath()
        #self.newGrid()
        
        warningImage = pyglet.image.load(style.warning.background_image[5:-2])
        
        
        l = self.label = Label(self, "title", x=20, y=10, size=20, text = "KommHelp Talkshow ", color = "#0030ff")        
        #l.animate("progress", 0, 1, 0, 3000)
        
    def quit(self):
        sys.exit(0)
    
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
            f.startHighlight()
            
            if f.index<len(self.items):
              subfields = self.subdirs(self.pathPrefix, self.pathForField(f.index))
              print "subfields", subfields
              if len(subfields)>0:
                  #self.path = self.pathForField(f.index)     

                  self.grid.enterFIeld(f)
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
          
    def cancelVideo(self):
        if self.videoplayer:
            self.videoplayer.unref()
            self.videoplayer.parent = None
            self.videoplayer = None
    
    def playPath(self, path):
        videos = glob.glob(path+"/*.mpg")
        if videos:
            path = normalizePath(videos[0])
            self.cancelVideo()
            self.videoplayer =  Videoplayer(self.gridContainer, "videoplayer", path, 0, 0, w=self.gridContainer.w, h=self.gridContainer.h)
            return
        
        sounds = glob.glob(path+"/*.wav")
        if not sounds: sounds = glob.glob(path+"/*.mp3")
        print "sounds", sounds
        if sounds:
            path = normalizePath(sounds[0])
            if os.path.isfile(path):
                print "correct path"
            else:
                print "nope, not correct path."
            #print path
            #r = Resource(path)
            #print r._obj.details

            #r = r.find("sound0")
            #print r._obj.details
            #if r != None:
            s = self.sound  = Sound(0, path)
            s.speed=1
            #else:
            #    print "Unable to decode wav"
            
        
    def setVolume(self, v):
        print "Volume", v
        #tubifex.volume = v
        Sound.setGlobalVolume(v)
        
    def back(self):
        l = self.path.split("/")
        if l:
            self.path= "/".join(l[:-1])
            self.gridFromPath()
            self.cleanUp()
  
    def home(self):
        l = self.path = ""
        self.gridFromPath()
        self.cleanUp()
              
    def subdirs(self, prefix, path):
        items = os.listdir(unicode(prefix+path))        
        items = filter(lambda x: os.path.isdir(prefix + path + "/" + x), items)            
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
        self.grid = Grid(self.gridContainer, self.count, self)
        print "instanceCount", Grid.instanceCount
        self.cleanupDC = DelayedCall(self.cleanUp, 375)

    def cleanUp(self):
        self.cancelVideo()
        
        # remove all children from gridCOntainer except the last one
        c = len(self.gridContainer)
        i = 0
        for x in self.gridContainer:
            if i<c-1:
                x.parent = None
            i+=1
            

    def key_sink(self, k):
        if k=="+":
            self.count += 1
            self.newGrid()
        if k=="-":
            self.count -= 1
            self.newGrid()


#environment.set("character_spacing", -2)                    

screen = Screen("Talkshow", "",
                int(style.page.width.replace('px','')),
                int(style.page.height.replace('px','')))
talkshow = Talkshow(screen)
# TODO: Add a method in Talkshow object to test if all is well configured.

#tubifex.keyboard_sink = talkshow.key_sink
screen.event_handler = talkshow

# boilerplate
def tick():
    animated_property.T = time.time()*1000
    animated_property.AnimatedProperty.tick()
    return True
    
pc = PeriodicCall(tick,0)
pyglet.app.run()
