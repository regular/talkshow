import os
import math
import glob
import sys

from talkshowLogger import logger
# function alias
debug = logger.debug
info = logger.info
warn = logger.warn
error = logger.error
info("Initialising talkshow. Version of Python: %s" % str(sys.version))


try:
    import pyglet
    info("pyglet seems installed and working fine.")
except:
    logger.error("Pyglet (a python library) is not installed. Talkshow cannot work. Please install pyglet")

try:
    import tinycss
    info("tinyCSS seems installed and working fine.")
except:
    logger.error("TinyCSS (a python library) is not installed. Talkshow cannot work. Please install tinyCSS")

try:
    import vlc
    vlc_test_instance = vlc.Instance()
    info("VLC seems available and working fine. Audio playback should work.")
except:
    logger.error("There is a problem with VLC. Either you are using the wrong version of talkshow (32/64 bit), or there is a bug in the code, or you can try and install VLC.")

try:
    os.path.isdir
except:
    logger.error("There is a problem with VLC. Either you are using the wrong version of talkshow (32/64 bit), or there is a bug in the code, or you can try and install VLC.")


try:
    import CommandBar
    from wrappers import *
    from widget import *
    import animated_property
    if sys.platform == 'win32':
        import _winreg

    from talkshowConfig import config as configClass
    from vlcPlayer import vlcPlayer

except Exception as e:
    logger.exception("exception! Details: {0}".format(e))
    raise








#TODO: make this configurable
ORIENTATION = 1

# Constants
COLUMNS = 2
MAX_ROW_NUMBER = 4

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
    path = os.path.expandvars(path[:-4])
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
        bg = self.bg = Rect(self, "bg", 2, 2, w, h)        
        self.bg.color = style.box.background_color  
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
        self.bg.extent = new_w, new_h        
        self.label.size = new_h
        if hasattr(self, "icon"):
            self.icon.x = (self.w - self.icon.w) / 2.0
            self.icon.y = (self.h - self.icon.h) / 2.0
            if conf.NO_TEXT_IF_IMAGE_AVAILABLE:
                self.label.text = ""

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

    def onMouseMove(self, x, y):
        grey = Talkshow.ColorOld
        
        if not Talkshow.ScanOn:
            if x > 0 and  y > 0 and x < self.w  and y < self.h:
                self.bg.color = Talkshow.highlightingColours[self.index]
            else:
                self.bg.color = grey

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
            cols = 1
            warn("!ERROR: No field")
        else:                
            cols = int(COLUMNS)
            
        # calculate number of rows and columns
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
        if Talkshow.ScanOn:
            
            if self.delegate.CurrentField < len(self.delegate.grid.fields):
                field = self.fields[self.delegate.CurrentField]
            else:
                debug( 'Den Knopf ' + str(self.delegate.CurrentButton+1) + ' ausfuehren...')
                self.delegate.HandlerList[self.delegate.CurrentButton]()
                
        else:
            for f in self:
                if f.contains(x,y):
                    field = f
            
        if field != None:
            self.delegate.onFieldClicked(field)

    def enterFIeld(self, field):
        info("enterFIeld" + str(field) +" "+ str(field.color))
        field.color = style.page.background_color
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
    
    VOLUME_MAX = 1
    ScanOn = 0
    
    ColorOld     = style.box.background_color
    highlightingColours = {0 : style.divhoverbox1.background_color,
               1 : style.divhoverbox2.background_color,
               2 : style.divhoverbox3.background_color,
               3 : style.divhoverbox4.background_color,
               4 : style.divhoverbox5.background_color,
               5 : style.divhoverbox6.background_color,
               6 : style.divhoverbox7.background_color,
               7 : style.divhoverbox8.background_color}
    

    def __init__(self, config, screen, player):
        Widget.__init__(self, screen, "Talkshow", w=screen.w, h=screen.h)
                
                
        self.screen = screen
        self.config = config
        self.initializeConfig()
        
        self.menuBar = CommandBar.MenuBar(self.screen, ORIENTATION)
        self.playerBar = CommandBar.PlayerBar(self.screen, ORIENTATION)


        self.player = player

        #self.player.play("content/Drei/nicht_nur_europa.wav")
        
        #self.DoLayout()
        
        self.count = 9    
        
        # TODO: FIX in order to avoid crashes
        self.pathPrefix   = config.CONTENT_DIRECTORY
        self.MenuPrefix = "Menu"
        self.path         = ""
        self.grid         = None
        self.videoplayer  = None
        self.MenuFlag     = 0
        self.PlaybackFlag = 0
        
        self.TimeOld = 0.
        #self.newGrid()
        
        self.volume = 0.8
        self.volumeIncrease = 0.1
        
        try:
            Talkshow.ScanOn       = bool(talkshowConfig.scanOnDefault)
        except:
            Talkshow.ScanOn       = 0
        self.TimeStep = 2000 #TODO set back to 2000
        
        
        
        # create layout
        self.SetLayout('Vertical')
        
        # create grid
        self.gridFromPath()

    def initializeConfig(self):
        # set content directory
        if not os.path.isdir(self.config.CONTENT_DIRECTORY):
            possible_content_paths = ["Content", "content", "Inhalt", "inhalt"]
            warn("{0} is not a valid content directory. Trying defaults...".format(os.path.abspath(self.config.CONTENT_DIRECTORY)))
            path_set = False
            for path in possible_content_paths:
                if os.path.isdir(path):
                    info("setting content Path to : {0}".format(os.path.abspath(path)))
                    self.config.CONTENT_DIRECTORY = os.path.abspath(path)
                    path_set = True
                    break
            if not path_set:
                error("{0} is not a valid content directory. Unable to find content.".format(os.path.abspath(self.config.CONTENT_DIRECTORY)))

        #set alarm directory
        alarmDir = os.path.join(self.config.CONTENT_DIRECTORY, 'Alarm')
        if os.path.isdir(alarmDir):
            self.ALARM_DIRECTORY = alarmDir
            info("Alarm sound is loaded from {0}".format(self.ALARM_DIRECTORY))
        else:
            self.ALARM_DIRECTORY = 'alarm'
            warn("Expected folder {1} under {0} does not exist. \
            Please create a folder named 'Alarm' under your content directory and place an alarm sound file into it. \
            Defaulting back to inbuilt alarm sound.".format(alarmDir, self.config.CONTENT_DIRECTORY))

        
    def onResize(self, width, height):
        
        if width != self.w or height != self.h:            
            self.h = height
            self.w = width
            self.menuBar = CommandBar.MenuBar(self.screen, ORIENTATION)
            self.playerBar = CommandBar.PlayerBar(self.screen, ORIENTATION)
        
            # create layout & grid
            self.SetLayout('Vertical')
            self.gridFromPath ()
        
                
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
        
        
        #set page background:
        self.page = Rect(self, "page", w=self.w, h= self.h, x=0, y=0, color = style.page.background_color)
        
        name = 'bg'
        self.GetWidgetSize(name,Alignment)
        self.bg              = Rect  (self, name,  w = self.BackGroundWidth , h=self.BackGroundHeigth, x=self.BackGroundPosX, y=self.BackGroundPosY, color="#7D7D7D")
        
        name = 'gridContainer'
        self.GetWidgetSize(name,Alignment)
        self.gridContainer   = Widget(self, 'gridContainer',  w = self.GridContainerWidth, h = self.GridContainerHeigth, x = self.GridContainerPosX, y = self.GridContainerPosY)
       
        
        ### add buttons from menuBar        
        self.homeButton = Button(self, "", w=self.menuBar.homeWidth, h=self.menuBar.homeHeight, x=self.menuBar.homeX, y=self.menuBar.homeY, handler=self.home, text="HOMEHOME", imagePath=self.menuBar.style.home.background_image[5:-2])   
        self.backButton = Button(self, "", w=self.menuBar.backWidth, h=self.menuBar.backHeight, x=self.menuBar.backX, y=self.menuBar.backY, handler=self.back, text="backback", imagePath=self.menuBar.style.back.background_image[5:-2])     
        
        #self.menuButton = Button(self, "", w=self.menuBar.settingsWidth, h=self.menuBar.settingsHeight, x=self.menuBar.settingsX, y=self.menuBar.settingsY, handler=self.menu, text="menumenu", imagePath=self.menuBar.style.settings.background_image[5:-2])     
        self.quitButton = Button(self, "", w=self.menuBar.shutDownWidth, h=self.menuBar.shutDownHeight, x=self.menuBar.shutDownX, y=self.menuBar.shutDownY, handler=self.quit, text="quitquit", imagePath=self.menuBar.style.shutDown.background_image[5:-2])     
        self.warningButton = Button(self, "", w=self.menuBar.warningWidth, h=self.menuBar.warningHeight, x=self.menuBar.warningX, y=self.menuBar.warningY, handler=self.DrawAttention, text="warningwarning", imagePath=self.menuBar.style.warning.background_image[5:-2])     
        
        self.ButtonList.append(self.warningButton)
        self.ButtonList.append(self.homeButton)
        self.ButtonList.append(self.backButton)
        #self.ButtonList.append(self.menuButton)
        self.ButtonList.append(self.quitButton)
        
        ### add buttons from playerBar        
        self.volumeDownButton = Button(self, "", w=self.playerBar.volumeDownWidth, h=self.playerBar.volumeDownHeight, x=self.playerBar.volumeDownX, y=self.playerBar.volumeDownY, handler=self.volumeDown, text="playplay", imagePath=self.playerBar.style.volumeDown.background_image[5:-2])     
        self.volumeUpButton = Button(self, "", w=self.playerBar.volumeUpWidth, h=self.playerBar.volumeUpHeight, x=self.playerBar.volumeUpX, y=self.playerBar.volumeUpY, handler=self.volumeUp, text="playplay", imagePath=self.playerBar.style.volumeUp.background_image[5:-2])     
        self.ButtonList.append(self.volumeDownButton)
        self.ButtonList.append(self.volumeUpButton)
                
        self.volumeLabel = Label(self, "name", self.playerBar.volumeX, self.playerBar.volumeY, self.playerBar.volumeSize, text=self.setVolumeText(), font_size=conf.FONT_SIZE_VOL)     
        
        
        # player stop/start/pause controls?        
        self.play = None
        self.playPrevious = None        
#        self.playButton = Button(self, "", w=self.playerBar.playWidth, h=self.playerBar.playHeight, x=self.playerBar.playX, y=self.playerBar.playY, handler=self.play, text="playplay", imagePath=self.playerBar.style.play.background_image[5:-2])     
#        self.playPreviousButton = Button(self, "", w=self.playerBar.playPreviousWidth, h=self.playerBar.playPreviousHeight, x=self.playerBar.playPreviousX, y=self.playerBar.playPreviousY, handler=self.playPrevious, text="playplay", imagePath=self.playerBar.style.playPrevious.background_image[5:-2])     
                
        ## TODO: label with "KommHelp Talkshow" ?
        #x = self.GridContainerPosX + 10
        #y = self.GridContainerPosY        
#        size = self.h/30
#        x    = self.w/2
#        y    = self.screenmarginvert + 5         
#        self.label           = Label (self, 'title', x, y, size, text = "KommHelp Talkshow", color = "#0030ff")#        
#        self.label.x = self.w/2 - self.label.w/2
        
        
        self.HandlerList = [button.handler for button in self.ButtonList]
          
        
    def quit(self):        
        if self.PlaybackFlag:
            try:
                self.PlaybakcProc.terminate()
            except Exception as e:
                logger.exception("Could not kill media player process... {0}".format(e))
                warn( "some process might not have exited! Use your task manager to kill the wmplayer.exe process if needed. ")
        sys.exit(0)
    
    def getFieldText(self, i):
        return self.items[i]
        
    def pathForField(self, i):
        path = self.path + "/" + self.items[i]
        if path[0] == "/": path = path[1:]
        return path
             
    def getFieldIcon(self, i):
        path = self.pathForField(i)
        return self.iconForPath(os.path.join(self.pathPrefix, path))
         
    def onFieldClicked(self, f):        
        if f != None:
            f.startHighlight()
            
            if f.index<len(self.items):
                subfields = self.subdirs(self.pathPrefix, self.pathForField(f.index))
                debug("subfields" + str(subfields))
                if len(subfields)>0:
                    #self.path = self.pathForField(f.index)     
                    self.grid.enterFIeld(f)
                    self.dc = DelayedCall(self.gridFromPath, 500, (style.page.background_color, self.pathForField(f.index)))
            self.playPath(os.path.join(self.pathPrefix, self.pathForField(f.index)))
            #self.playPath_AudioRecorder(self.pathPrefix + self.pathForField(f.index))
    
    def iconForPath(self, path):
        images = glob.glob(str(path) + "/*.png")
        if images:
            path = normalizePath(images[0])
            i = wrappers.Image(None, path, path)
            return i
        return None
          
    def cancelVideo(self):
        if self.videoplayer:
            self.videoplayer.unref()
            self.videoplayer.parent = None
            self.videoplayer = None
            
    def playName(self, path):
        
        Name = glob.glob(path+"/*.nam")
        if Name:
            wave = normalizePath(Name[0])
            s = self.sound  = Sound(0, wave)
            s.speed=1
            
    def playPath(self, path):

        mediaPatterns = ["*.wav", "*.avi", "*.wmv", "*.mpg", "*.mp3", "*.wma", "*.asf", "*.midi", "*.aiff", "*.au", "*.m4a"]
        mediaPatterns_uppercase = [pattern.upper() for pattern in mediaPatterns]
        mediaPatterns.extend(mediaPatterns_uppercase)
        mediaFiles = []
        for pattern in mediaPatterns:
            mediaFiles += glob.glob1(path, pattern)

        debug("audio files under {0}: {1}. Playing the first one if there is one...".format(path, mediaFiles))

        if mediaFiles:
            self.player.play(os.path.join(path, mediaFiles[0]))
        else:
            warn("no media file found under {0}".format(path))


                

        
        
    def setVolumeText(self, volume=None):
        if not volume:
            volume = self.player.getVolume()
        volumeText = "   " + str(int(volume/10))
        try: self.volumeLabel.text = volumeText
        except: pass
        return volumeText

    def volumeMax(self):
        self.player.volumeMax()
        self.setVolumeText(self.player.getVolume())
        
    def volumeDown(self):
        self.player.volumeDown()
        self.setVolumeText(self.player.getVolume())
        
    def volumeUp(self):
        self.player.volumeUp()
        self.setVolumeText(self.player.getVolume())
                 
    def back(self):

        self.player.stop()
        l = self.path.split("/")
        
        if l:
            self.path= "/".join(l[:-1])
            self.gridFromPath((style.page.background_color,self.path))
            self.cleanUp()
  
    def home(self):
        if self.MenuFlag:
            self.MenuFlag = 0
            self.pathPrefix = self.config.CONTENT_DIRECTORY
            
        l = self.path = ""
        self.gridFromPath()
        self.cleanUp()
              
    def subdirs(self, prefix, path):
        if self.PlaybackFlag:
            items = ['Quit']
        else:
            items = os.listdir(os.path.join(prefix, path))
            items = [unicode(i) for i in items]
            items = filter(lambda x: os.path.isdir(os.path.join(prefix, path, x)), items)
               
        debug( 'Items: ' + unicode(items))
        return items
                
    def gridFromPath(self, color_and_path = None):
        path = ""
        color= style.page.background_color
        if color_and_path:
            color, path = color_and_path
        self.path = path
        
        
        if self.MenuFlag:
            #self.pathPrefix = "./Menu"
            ok = self.MenuCommand(path[path.rfind('/')+1:])
            debug( 'OK: ' +str(ok))
            if ok == 1:
                #self.gridFromPath()
                self.home()
                return
            elif ok == 2:
                self.pathPrefix = './Menu/'
                self.path = 'Scan/Change settings'
        if self.PlaybackFlag:
            
            self.PlaybackCommand(path[path.rfind('/')+1:],self.PlaybakcProc)
            
            
        debug("prefix=[{0}] path =[{1}]".format(self.pathPrefix, self.path))
        debug(self.pathPrefix + path)
        
        self.items =  self.subdirs(self.pathPrefix, self.path)
        self.count = len(self.items)
        if self.count:
            self.newGrid(color)
        
    def newGrid(self, color=style.page.background_color):
                
        self.bg.color=color
        self.grid = Grid(self.gridContainer, self.count, self)
        debug("instanceCount" + str( Grid.instanceCount))
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
        debug( "drawattention?")
        self.volumeMax()
        self.playPath(self.ALARM_DIRECTORY)
        
    def menu(self):

        #self.menuButton.h = 0
        #self.backButton.h = 0
        self.MenuFlag = 1
        self.pathPrefix = './Menu/'
        self.gridFromPath((style.page.background_color,''))
        self.cleanUp()
    def PlaybackCommand(self, Command, process):
        info( 'Playbakc Befehl: ' + str(Command))
        if Command == 'Quit':
            process.terminate()
            self.PlaybackFlag = 0
            self.home()
            
    def MenuCommand(self,Command):
        debug( 'Menu Befehl: ' + str(Command))
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
            debug( 'ok')
            return 1

            
        elif Command == 'on':
            debug('Scan einschalten')
            Talkshow.ScanOn = 1
            debug('Scan is on.')
            #self.home()
            return 1
        elif Command == 'Very fast':
            self.TimeStep = 500
            return 2
            
        elif Command == 'Very slow':
            self.TimeStep = 5000
            return 2
            
        elif Command == 'Faster':
            self.TimeStep = self.TimeStep - TimeStepIncrement
            return 2
            
        elif Command == 'Slower':
            self.TimeStep = self.TimeStep + TimeStepIncrement
            return 2
            
        elif Command == 'Default':
            self.TimeStep = TimeStepDefault
            return 2
        
        elif Command == 'OK':
            return 1
        
        elif Command == 'off':
            debug('Scan ausschalten')
            Talkshow.ScanOn = 0
            #self.home()
            return 1
        
        elif Command == 'Record sound':
            self.Record_AudioRecorder('')
            debug('Aufnahme')
            #self.home()
            return 1
        elif Command == 'Set volume':
            debug('Lautstaerke')
        elif Command == 'VLC':
            debug('VLC spielt')
            self.SetPlayer('VLC')
            return 1
        elif Command == 'Media Player':
            debug('Media')
            self.SetPlayer('WMP')
            return 1
        else:
            return 0
        
        
    def DoScan(self,TimeNow):
        NumButtons    = len(self.ButtonList)

        if (self.CurrentField >= len(self.grid.fields)-1 and self.CurrentButton < NumButtons-1):
            # select & highlight a button

            LastField = self.grid.fields[-1]
            LastField.color = self.ColorOld
            self.CurrentField = len(self.grid.fields) + 1
            self.CurrentButton = self.CurrentButton + 1

            debug('Button ' + str(self.CurrentButton+1) + 'von' + str(len(self.ButtonList)))
            #self.homeButton.bar.parent = None
            Button     = self.ButtonList[self.CurrentButton]
            LastButton = self.ButtonList[self.CurrentButton-1]
            Button.bar     = Box(Button.container    , "bar", self.homeButton.w, self.homeButton.h, s=HighlightBarSettings)
            LastButton.bar = Box(LastButton.container, "bar", self.homeButton.w, self.homeButton.h, s=BarSettings)
            #b.x, b.y = 3,3


        else:
            # select & highlight a field (box)

            if self.CurrentButton >= NumButtons-1:
                self.ButtonList[self.CurrentButton].bar = Box(self.ButtonList[self.CurrentButton].container, "bar", self.homeButton.w, self.homeButton.h, s=BarSettings)
                self.CurrentField = -1
                self.CurrentButton = -1

            self.CurrentField = self.CurrentField + 1

            Field     = self.grid.fields[self.CurrentField]
            LastField = self.grid.fields[self.CurrentField-1]
            a = self.grid
            debug(str(self.CurrentField+1) + str(Field.text))
            self.playName(os.path.join(self.pathPrefix, self.pathForField(Field.index)))

            #Field.startHighlight()
            LastField.color = self.ColorOld
            self.ColorOld = Field.color
            Field.color = self.highlightingColours[self.CurrentField]
                
            self.TimeOld  = TimeNow

    # boilerplate
    def tick(self):

        TimeNow = time.time()*1000

        if animated_property.T == 0.0:
            # initializing
            TimeOld = TimeNow
        else:
            TimeOld = self.TimeOld

        animated_property.T = TimeNow
        animated_property.AnimatedProperty.tick()

        if Talkshow.ScanOn and (TimeNow - TimeOld > self.TimeStep):
            self.DoScan(TimeNow)
        return True


def main():
    """
    Start of talkshow execution
    """

    logger.debug("initialising talkshow.")


    # initialise screen heights and widths
    try:
        screenWidth = talkshowConfig.windowWidth
        screenHeight = talkshowConfig.windowHeight
        if screenHeight == 0 or screenWidth == 0:
            screenWidth = int(style.page.width)
            screenHeight = int(style.page.height)
    except:
        screenWidth = int(style.page.width)
        screenHeight = int(style.page.height)

    # screen object to be passed into Talkshow instance
    screen = Screen("KommHelp Talkshow", "", screenWidth, screenHeight)


    # initialise config and vlcPlayer
    config = configClass()
    player = vlcPlayer()

    # talkshow object and handler
    talkshow = Talkshow(config, screen, player)
    screen.event_handler = talkshow

    # periodicCall used for Scan mode
    pc = PeriodicCall(talkshow.tick,0)
    pyglet.app.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        #log all and any exceptions to file
        logger.exception("exception! {0}".format(e))
        raise