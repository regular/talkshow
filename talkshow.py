import os
import math
import wrappers
from wrappers import *
from widget import *
import glob
import subprocess
import pyglet
from delayed_call import *
import animated_property
import time
if sys.platform == 'win32':
    import _winreg


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

def WindowsPath(path):
    path = path.replace("/", "\\")
    # return absolute path
    return os.getcwd() + path[1:]

def ExpandPath(path):
    path = os.path.expandvars(path[:-4].replace('%','$')).replace('$','')
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
        l = self.label = Label(self, "label", x=20, y=20, size=h/5, text=text)        
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

        rows = int(rows)
        cols = int(cols)
        #print cols, rows

        w = int(parent.w / cols)
        h = int(parent.h / rows)

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
        if talkshow.ScanOn:
            
            if talkshow.CurrentField < len(talkshow.grid.fields):
                field = self.fields[talkshow.CurrentField]
            else:
                print 'Den Knopf ', talkshow.CurrentButton+1,' ausfuehren...'
                talkshow.HandlerList[talkshow.CurrentButton]()
                
        else:
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
                
        self.screen = screen
        self.SetLayout('Vertical')
        
        #self.DoLayout()
        
        self.count = 9    
        
        # TODO: FIX in order to avoid crashes
        self.pathPrefix   = "./Content/"
        self.path         = ""
        self.grid         = None
        self.videoplayer  = None
        self.MenuFlag     = 0
        self.PlaybackFlag = 0
        self.gridFromPath ()
        self.SetPlayer    ('WMP')
        
        self.TimeOld = 0.
        #self.newGrid()
        
        self.ColorOld     = '#FFF000'
        try:
            self.ScanOn       = bool(talkshowConfig.scanOnDefault)
        except:
            self.ScanOn       = 0
        self.TimeStep = 2000
        
        #l.animate("progress", 0, 1, 0, 3000)
        
    def GetWidgetSize(self,name,Alignment):
        if Alignment == 'Vertical':            
            self.Headwidth          = 0
            self.Footwidth          = 0
            self.Rightwidth         = self.w/10
            self.Leftwidth          = self.Rightwidth
            
        else: 
            self.Headwidth          = self.h/10
            self.Footwidth          = self.Headwidth
            self.Rightwidth         = 0
            self.Leftwidth          = 0
        
        self.screenmarginvert   = self.h/100 #10
        self.screenmarginhoriz  = self.screenmarginvert
        
        self.bgmarginvert       = self.h/100 #10
        self.bgmarginhoriz      = self.bgmarginvert  
            
        ButtonSize              = self.Rightwidth  + self.Headwidth
        if name == 'bg':
            w = self.BackGroundWidth    = self.w - 2 * self.screenmarginhoriz - self.Rightwidth - self.Leftwidth 
            h = self.BackGroundHeigth   = self.h - 2 * self.screenmarginvert  - self.Headwidth  - self.Footwidth
            x = self.BackGroundPosX     = self.screenmarginhoriz + self.Leftwidth
            y = self.BackGroundPosY     = self.screenmarginvert  + self.Headwidth
            handler = None
            text = ''
            isbutton = 0

        elif name == 'gridContainer':
            w = self.GridContainerWidth  = self.BackGroundWidth  - 2 * self.bgmarginhoriz
            h = self.GridContainerHeigth = self.BackGroundHeigth - 2 * self.bgmarginvert
            x = self.GridContainerPosX   = self.BackGroundPosX + self.bgmarginhoriz
            y = self.GridContainerPosY   = self.BackGroundPosY + self.bgmarginvert
            handler = None
            text = ''
            isbutton = 0
         
        elif name == 'quitbutton': 
            w = self.quitButtonWidth    = ButtonSize
            h = self.quitButtonHeight   = ButtonSize
            x = self.quitButtonPosX     = self.w - self.screenmarginhoriz - self.quitButtonWidth
            y = self.quitButtonPosY     = self.screenmarginvert
            handler = self.quit
            text = 'X'
            isbutton = 1
            
        elif name == 'menubutton':
            w = self.menuButtonWidth    = ButtonSize
            h = self.menuButtonHeight   = ButtonSize
            x = self.menuButtonPosX     = self.w - self.screenmarginhoriz - self.Rightwidth - 2 * self.Headwidth
            y = self.menuButtonPosY     = self.screenmarginvert + 2 * self.Rightwidth
            handler = self.menu
            text = 'M'
            isbutton = 1
        
        elif name == 'attentionbutton':
            w = self.AttButtonWidth     = ButtonSize
            h = self.AttButtonHeight    = ButtonSize
            x = self.AttButtonPosX      = self.screenmarginhoriz
            y = self.AttButtonPosY      = self.screenmarginvert
            handler = self.DrawAttention
            text = '!'
            isbutton = 1
        
        elif name == 'homebutton':
            w = self.homeButtonWidth    = ButtonSize
            h = self.homeButtonHeight   = ButtonSize
            x = self.homeButtonPosX     = self.screenmarginhoriz 
            y = self.homeButtonPosY     = self.h - self.screenmarginvert - ButtonSize
            handler = self.home
            text = '<<'
            isbutton = 1
        
        elif name == 'backbutton':
            w = self.backButtonWidth    = ButtonSize
            h = self.backButtonHeight   = ButtonSize
            x = self.backButtonPosX     = self.screenmarginhoriz + self.Footwidth
            y = self.backButtonPosY     = self.h - self.screenmarginvert - ButtonSize    - self.Leftwidth
            handler = self.back
            text = '<'
            isbutton = 1
        
        elif name == 'volume':
            w = self.VolumeSliderWidth  = self.Rightwidth  + self.Headwidth
            h = self.VolumeSliderHeight = 2 * self.Rightwidth
            x = self.VolumeSliderPosX   = self.w - self.screenmarginhoriz - self.VolumeSliderWidth
            y = self.VolumeSliderPosY   = self.h - self.screenmarginvert - self.Footwidth - self.VolumeSliderHeight
            handler = self.setVolume
            text = ''
            isbutton = 0
        else:
            x = 0
            y = 0
            w = 0
            h = 0
            handler = None
            text = ''
            isbutton = 0
            
#        VolumeSliderWidth  = 2 * Footwidth
#        VolumeSliderHeight = Footwidth
#        VolumeSliderPosX   = self.w - screenmarginhoriz - VolumeSliderWidth
#        VolumeSliderPosY   = self.h - screenmarginvert  - VolumeSliderHeight
        
        return [x, y, w, h, handler, text, isbutton]
    
    def SetLayout(self,Alignment):
        self.ButtonList  = []
        self.HandlerList = []
        
        name = 'bg'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        self.bg              = Rect  (self, name,  w = self.BackGroundWidth , h=self.BackGroundHeigth, x=self.BackGroundPosX, y=self.BackGroundPosY, color="#202020")
        
        name = 'gridContainer'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        self.gridContainer   = Widget(self, name,  w = self.GridContainerWidth, h = self.GridContainerHeigth, x = self.GridContainerPosX, y = self.GridContainerPosY)
        
        name = 'attentionbutton'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        b = self.AttentionButton = Button(self, name,w = self.AttButtonWidth    , h = self.AttButtonHeight,     x = self.AttButtonPosX,     y = self.AttButtonPosY,    handler = handler, text=text)
        self.ButtonList.append (b)
        self.HandlerList.append(handler)        
        
        name = 'backbutton'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        b = self.backButton      = Button(self, name,     w = self.backButtonWidth   , h = self.backButtonHeight,    x = self.backButtonPosX,    y = self.backButtonPosY,   handler = handler, text=text)
        self.ButtonList.append (b)
        self.HandlerList.append(handler)        
        
        name = 'homebutton'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        b = self.homeButton      = Button(self, name,     w = self.homeButtonWidth   , h = self.homeButtonHeight,    x = self.homeButtonPosX,    y = self.homeButtonPosY,   handler = handler, text=text)
        self.ButtonList.append (b)
        self.HandlerList.append(handler)        
        
        name = 'quitbutton'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        b = self.quitButton      = Button(self, name   ,  w = self.quitButtonWidth   , h = self.quitButtonHeight,    x = self.quitButtonPosX,    y = self.quitButtonPosY,   handler = handler, text=text)        
        self.ButtonList.append (b)
        self.HandlerList.append(handler)        
        
        name = 'menubutton'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        b = self.menuButton      = Button(self, name   ,  w = self.menuButtonWidth   , h = self.menuButtonHeight,    x = self.menuButtonPosX,    y = self.menuButtonPosY,   handler = handler, text=text)
        self.ButtonList.append (b)
        self.HandlerList.append(handler)        
        
        name = 'volume'
        [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(name,Alignment)
        #self.volumeSlider   = Slider(self, "volume"    ,    w = self.VolumeSliderWidth , h = self.VolumeSliderHeight,  x = self.VolumeSliderPosX,  y = self.VolumeSliderPosY, action = self.setVolume)
        #self.volumeSlider.knobPosition = 0.0
        
        
        #x = self.GridContainerPosX + 10
        #y = self.GridContainerPosY
        
        size = self.h/30
        x    = self.w/2
        y    = self.screenmarginvert + 5 
        
        self.label           = Label (self, 'title', x, y, size, text = "KommHelp Talkshow", color = "#0030ff")
        
        self.label.x = self.w/2 - self.label.w/2
          
        
    def quit(self):
        if self.PlaybackFlag:
            process.terminate()
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
              #self.playPath_AudioRecorder(self.pathPrefix + self.pathForField(f.index))
    
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
            
    def playName(self, path):
        
        Name = glob.glob(path+"/*.nam")
        #print "sounds", sounds
        if Name:
            wave = normalizePath(Name[0])
            s = self.sound  = Sound(0, wave)
            s.speed=1
            
    def playPath(self, path):
        
        WaveSounds = glob.glob(path+"/*.wav")
        #print "sounds", sounds
        if WaveSounds:
            wave = normalizePath(WaveSounds[0])
            print 'playing: ', wave
            s = self.sound  = Sound(0, wave)
            s.speed=1
        else:
            Media = glob.glob(path+"/*.avi") + glob.glob(path+"/*.wmv") + glob.glob(path+"/*.mpg") + glob.glob(path+"/*.mp3") + glob.glob(path+"/*.wma") + glob.glob(path+"/*.asf") + glob.glob(path+"/*.midi") + glob.glob(path+"/*.aiff") + glob.glob(path+"/*.au")
        
            if Media:
                MediaString = ''
                for filename in Media:
                    WinName = WindowsPath(filename)
                    MediaString = MediaString + ' "' + WinName + '"'
                #print MediaString
                self.play_MediaPlayer(MediaString)
                return
            
            
    #def play_AudioRecorder(self, mp3):
    #    AudioRecorderExe = 'c:\WINDOWS\system32\sndrec32.exe '
    #    #Arguments        = '/embedding /play /close '
    #    Arguments        = '/play /close '
    #    os.system(AudioRecorderExe + Arguments + '"' + mp3 + '"')
    
    def Record_AudioRecorder(self, name):
        AudioRecorderExe = 'c:\WINDOWS\system32\sndrec32.exe '
        #Arguments        = '/embedding /play /close '
        Arguments        = '/record /close '
        os.system(AudioRecorderExe + Arguments + '"' + name + '"')
            
    def play_MediaPlayer(self, media):
        
        Arguments      = '--volume=1 '

        #screen.window.set_fullscreen(0)
        print 'Play command: ', self.MediaPlayerExe + Arguments + media
        
        si = subprocess.STARTUPINFO()
        si.dwFlags     = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        
        self.PlaybakcProc = subprocess.Popen(self.MediaPlayerExe + Arguments + media,startupinfo = si)

        self.PlaybackFlag = 1
        self.home()
        #screen = Screen('', "", 40, 80, "#00007f")#screen.on_resize(50,70)
        #screen.w = 200
        #screen.h = 200
        
        #screen.x = 100
        #screen.y = 10
        #screen.window.activate()
        
        #Running = 1
        #while Running:
        #    Running = self.process.poll()
        
        #self.process.wait()
        #screen.window.set_fullscreen(1)
    
    def SetPlayer(self,Player):
        if sys.platform == 'win32':
            if Player == 'VLC':
                KeyName = 'SOFTWARE\\VideoLAN\\VLC'
                AppName = ''
                print "VLC"
                
            elif Player == 'WMP':
                KeyName = 'Software\\Microsoft\\MediaPlayer\\Setup\\CreatedLinks'
                AppName = 'AppName'
                print "WMP"
                
            else: 
                print 'Media player not defined.'
            try:
                
                RegKey     = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,KeyName)
                Executable = ExpandPath(_winreg.QueryValueEx(RegKey,AppName)[0])
            except:
                try:
                    RegKey     = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,KeyName)
                    Executable = ExpandPath(_winreg.QueryValueEx(RegKey,AppName)[0])
                
                except:
                    print 'Sorry. Neither Windows Media Player nor VLC found in registry. Media playback disabelled.'
                    return
                
#            if Player == 'VLC':
#                Executable = Executable.replace('vlc','cvlc')
#                
            self.MediaPlayerExe = Executable + ' '
            
                
            print self.MediaPlayerExe
            
        else:
            print 'Sorry. Currently, media other than *.wav files can only be played back on Windows 32 systems.'
                
    def setVolume(self, v):
        #print "Volume", v
        #tubifex.volume = v
        Sound.setGlobalVolume(v)
        
    def back(self):
        l = self.path.split("/")
        
        if l:
            self.path= "/".join(l[:-1])
            self.gridFromPath(("#000000",self.path))
            self.cleanUp()
  
    def home(self):
        if self.MenuFlag:
            self.MenuFlag = 0
            self.pathPrefix = './Content/'
            
        l = self.path = ""
        self.gridFromPath()
        self.cleanUp()
              
    def subdirs(self, prefix, path):
        if self.PlaybackFlag:
            items = ['Quit']
        else:
            items = os.listdir(unicode(prefix+path))        
            items = filter(lambda x: os.path.isdir(prefix + path + "/" + x), items)     
               
        print 'Items: ',items
        return items
                
    def gridFromPath(self, color_and_path = None):
        path = ""
        color="#000000"
        if color_and_path:
            color, path = color_and_path
        self.path = path
        
        
        if self.MenuFlag:
            #self.pathPrefix = "./Menu"
            ok = self.MenuCommand(path[path.rfind('/')+1:])
            print 'OK: ',ok
            if ok == 1:
                #self.gridFromPath()
                self.home()
                return
            elif ok == 2:
                self.pathPrefix = './Menu/'
                self.path = 'Scan/Change settings'
        if self.PlaybackFlag:
            self.PlaybackCommand(path[path.rfind('/')+1:],self.PlaybakcProc)
            
            
        print self.pathPrefix+ path
        
        #print items
        self.items =  self.subdirs(self.pathPrefix, self.path)
        #print self.items
        self.count = len(self.items)
        if self.count:
            self.newGrid(color)
        
    def newGrid(self, color="#000000"):
        self.bg.color=color
        self.grid = Grid(self.gridContainer, self.count, self)
        print "instanceCount", Grid.instanceCount
        self.CurrentField  = -1#len(self.grid.fields)-1
        self.CurrentButton = -1
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
            
    def DrawAttention(self):
        self.playPath(self.pathPrefix + '/Alarm')
        
    def menu(self):

        #self.menuButton.h = 0
        #self.backButton.h = 0
        self.MenuFlag = 1
        self.pathPrefix = './Menu/'
        self.gridFromPath(("#000000",''))
        self.cleanUp()
    def PlaybackCommand(self, Command, process):
        print 'Playbakc Befehl: ',Command
        if Command == 'Quit':
            process.terminate()
            self.PlaybackFlag = 0
            self.home()
            
    def MenuCommand(self,Command):
        print 'Menu Befehl: ',Command
        TimeStepIncrement = 200
        TimeStepDefault   = 2000
        
        if Command == 'Horizontal' or Command == 'Vertical':
            
            for c in self.screen.__children__[0]:
                
                [x, y, w, h, handler, text, isbutton] = self.GetWidgetSize(c.name,Command)
                if not(x==0 and y==0 and w==0 and h==0):
                    if isbutton:
                        c.__init__(self, c.name, x=x, y=y, w=w, h=h, handler = handler,text=text)
                    else:
                        c.__init__(self, c.name, x=x, y=y, w=w, h=h)
            print 'ok'
            return 1

            
        elif Command == 'on':
            print 'Scan einschalten'
            self.ScanOn = 1
            print 'Scan is on.'
            #self.home()
            return 1
        elif Command == 'Very fast':
            talkshow.TimeStep = 500
            return 2
            
        elif Command == 'Very slow':
            talkshow.TimeStep = 5000
            return 2
            
        elif Command == 'Faster':
            talkshow.TimeStep = talkshow.TimeStep - TimeStepIncrement
            return 2
            
        elif Command == 'Slower':
            talkshow.TimeStep = talkshow.TimeStep + TimeStepIncrement
            return 2
            
        elif Command == 'Default':
            talkshow.TimeStep = TimeStepDefault
            return 2
        
        elif Command == 'OK':
            return 1
        
        elif Command == 'off':
            print 'Scan ausschalten'
            self.ScanOn = 0
            #self.home()
            return 1
        
        elif Command == 'Record sound':
            self.Record_AudioRecorder('')
            print 'Aufnahme'
            #self.home()
            return 1
        elif Command == 'Set volume':
            print 'Lautstaerke'
        elif Command == 'VLC':
            print 'VLC spielt'
            self.SetPlayer('VLC')
            return 1
        elif Command == 'Media Player':
            print 'Media'
            self.SetPlayer('WMP')
            return 1
        else:
            return 0
        
    def DoScan(self,TimeNow):
        NumButtons    = len(self.ButtonList)
        
        if self.ScanOn:
            
            if (self.CurrentField >= len(self.grid.fields)-1 and self.CurrentButton < NumButtons-1):
                LastField = self.grid.fields[-1]
                LastField.color = self.ColorOld
                self.CurrentField = len(self.grid.fields) + 1
                self.CurrentButton = self.CurrentButton + 1
                
                print 'Button ', self.CurrentButton+1, 'von', len(self.ButtonList)
                #self.homeButton.bar.parent = None
                Button     = self.ButtonList[self.CurrentButton]
                LastButton = self.ButtonList[self.CurrentButton-1]
                Button.bar     = Box(Button.container    , "bar", self.homeButtonWidth, self.homeButtonHeight, s=HighlightBarSettings)
                LastButton.bar = Box(LastButton.container, "bar", self.homeButtonWidth, self.homeButtonHeight, s=BarSettings)
                #b.x, b.y = 3,3
                
                
            else:
                if self.CurrentButton >= NumButtons-1:
                    self.ButtonList[self.CurrentButton].bar = Box(self.ButtonList[self.CurrentButton].container, "bar", self.homeButtonWidth, self.homeButtonHeight, s=BarSettings)
                    self.CurrentField = -1
                    self.CurrentButton = -1
                    
                self.CurrentField = self.CurrentField + 1
                
                Field     = self.grid.fields[self.CurrentField]
                LastField = self.grid.fields[self.CurrentField-1]
                a = self.grid
                print self.CurrentField+1, Field.text
                self.playName(unicode(self.pathPrefix + self.pathForField(Field.index)))
            
                #Field.startHighlight()
                LastField.color = self.ColorOld
                self.ColorOld = Field.color
                Field.color = '#F00000'
                
                
            
                
            self.TimeOld  = TimeNow
        
#environment.set("character_spacing", -2)                


try:
    screenWidth = talkshowConfig.windowWidth
    screenHeight = talkshowConfig.windowHeight
    print "aa"
    if screenHeight == 0 or screenWidth == 0:        
        print "bb"
        screenWidth = int(style.page.width.replace('px',''))
        screenHeight = int(style.page.height.replace('px',''))        
except:
    print "cc"
    screenWidth = int(style.page.width.replace('px',''))
    screenHeight = int(style.page.height.replace('px',''))
    

screen = Screen("Talkshow", "",screenWidth, screenHeight)
talkshow = Talkshow(screen)
# TODO: Add a method in Talkshow object to test if all is well configured.

#tubifex.keyboard_sink = talkshow.key_sink
screen.event_handler = talkshow

#talkshow.grid.fields[0].w = 20

# boilerplate
def tick():
    
    TimeNow = time.time()*1000
    
    if animated_property.T == 0.0:
        # initializing
        TimeOld = TimeNow
    else:
        TimeOld = talkshow.TimeOld
        
    animated_property.T = TimeNow
    animated_property.AnimatedProperty.tick()
    
    if TimeNow - TimeOld > talkshow.TimeStep:
        
        talkshow.DoScan(TimeNow)
        
    return True

pc = PeriodicCall(tick,0)
pyglet.app.run()