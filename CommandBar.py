import talkshowConfig
import pyglet

from talkshowLogger import logger

debug = logger.debug
info = logger.info
warn = logger.warn
   
class CommandBar(object):
    
    def __init__(self, screen, orientation):

        self.style = talkshowConfig.config().parser.style
        self.screen = screen
        
        
        # expecting a list of 4 values for the padding values. no css shorthands allowed.
        self.imagePadding = self.style.commandImage.padding
        self.pagePadding = map(lambda x:x/100.0, self.style.page.padding)
        
        self.leftPadding = self.screen.w * self.pagePadding[3] + self.imagePadding[3]
        self.topPadding = self.screen.w * self.pagePadding[0] + self.imagePadding[0]
    
        # 0 = landscape; 1 = vertical
        self.orientation = orientation
        
        # calculate bar size by orientation property
        if self.orientation == 0:
            self.height = screen.h * self.style.commandBar.height / 100.0
            self.width = screen.w * self.style.commandBar.width / 100.0
        else:
            self.height = screen.h * self.style.sideBar.height / 100.0
            self.width = screen.w * self.style.sideBar.width / 100.0

        self.increaseX = 0;
        self.increaseY = 0;

class MenuBar(CommandBar):

    def __init__(self, screen, orientation=0):
        
        super(MenuBar, self).__init__(screen, orientation)
        
        
        
        x = self.leftPadding
        y = self.topPadding
        
        
        if self.orientation == 0:
            debug("orientation 0")
            increaseX = int(self.style.warning.width) + self.imagePadding[1] + self.imagePadding[3]
            increaseY = 0
            
        else:            
            debug("orientation 1")
            increaseX = 0            
            increaseY = int(self.style.warning.height) + self.imagePadding[0] + self.imagePadding[2]      
        
        # create the warning button properties
        self.warningImage = pyglet.image.load(self.style.warning.background_image[5:-2])
        self.warningHeight = int(self.style.warning.height)
        self.warningWidth = int(self.style.warning.width)
        self.warningX = x
        self.warningY = y
        self.warningSprite = pyglet.sprite.Sprite(self.warningImage, self.warningX, self.warningY)

        x = x + increaseX
        y = y + increaseY
    
        # create the home button properties
        self.homeImage = pyglet.image.load(self.style.home.background_image[5:-2])
        self.homeHeight = int(self.style.home.height)
        self.homeWidth = int(self.style.home.width)
        self.homeX = x
        self.homeY = y
        self.homeSprite = pyglet.sprite.Sprite(self.homeImage, self.homeX, self.homeY)

        x = x + increaseX
        y = y + increaseY
    
        # create the back button properties
        self.backImage = pyglet.image.load(self.style.back.background_image[5:-2])
        self.backHeight = int(self.style.back.height)
        self.backWidth = int(self.style.back.width)
        self.backX = x
        self.backY = y
        self.backSprite = pyglet.sprite.Sprite(self.backImage, self.backX, self.backY)

        x = x + increaseX
        y = y + increaseY
    
        # create the shutDown button properties        
        self.shutDownImage = pyglet.image.load(self.style.shutDown.background_image[5:-2])
        self.shutDownHeight = int(self.style.shutDown.height)
        self.shutDownWidth = int(self.style.shutDown.width)
        self.shutDownX = x
        self.shutDownY = y
        self.shutDownSprite = pyglet.sprite.Sprite(self.shutDownImage, self.shutDownX, self.shutDownY)

        x = x + increaseX
        y = y + increaseY    
        
        # create the settings button properties
        self.settingsImage = pyglet.image.load(self.style.settings.background_image[5:-2])
        self.settingsHeight = int(self.style.settings.height)
        self.settingsWidth = int(self.style.settings.width)
        self.settingsX = x
        self.settingsY = y
        self.settingsSprite = pyglet.sprite.Sprite(self.settingsImage, self.settingsX, self.settingsY)


class PlayerBar(CommandBar):
    
    def __init__(self, screen, orientation=0):
        
        super(PlayerBar, self).__init__(screen, orientation)
        
        y = self.topPadding
        
        if self.orientation == 0:
            increaseX = int(self.style.volumeDown.width) + self.imagePadding[1] + self.imagePadding[3]
            increaseY = 0
            x = self.screen.w - 5*increaseX
        else:
            x = self.imagePadding[3] + self.screen.w - self.width
            increaseX = 0
            increaseY = int(self.style.volumeDown.height)  + self.imagePadding[0] + self.imagePadding[2]             
        
        # create the volumeDown button properties
        self.volumeDownImage = pyglet.image.load(self.style.volumeDown.background_image[5:-2])
        self.volumeDownHeight = int(self.style.volumeDown.height)
        self.volumeDownWidth = int(self.style.volumeDown.width)
        self.volumeDownX = x
        self.volumeDownY = y
        self.volumeDownSprite = pyglet.sprite.Sprite(self.volumeDownImage, self.volumeDownX, self.volumeDownY)

        x = x + increaseX
        y = y + increaseY
    
        # create the volumeUp button properties
        self.volumeUpImage = pyglet.image.load(self.style.volumeUp.background_image[5:-2])
        self.volumeUpHeight = int(self.style.volumeUp.height)
        self.volumeUpWidth = int(self.style.volumeUp.width)
        self.volumeUpX = x
        self.volumeUpY = y
        self.volumeUpSprite = pyglet.sprite.Sprite(self.volumeUpImage, self.volumeUpX, self.volumeUpY)

        x = x + increaseX
        y = y + increaseY
        
        self.volumeHeight = int(self.style.volumeUp.height)
        self.volumeWidth = int(self.style.volumeUp.width)
        self.volumeX = x
        self.volumeY = y
        self.volumeSize = 50
        
        x = x + increaseX
        y = y + increaseY        
        
    
        # create the playPrevious button properties
        self.playPreviousImage = pyglet.image.load(self.style.playPrevious.background_image[5:-2])
        self.playPreviousHeight = int(self.style.playPrevious.height)
        self.playPreviousWidth = int(self.style.playPrevious.width)
        self.playPreviousX = x
        self.playPreviousY = y
        self.playPreviousSprite = pyglet.sprite.Sprite(self.playPreviousImage, self.playPreviousX, self.playPreviousY)

        x = x + increaseX
        y = y + increaseY
    
        # create the play button properties
        self.playImage = pyglet.image.load(self.style.play.background_image[5:-2])
        self.playHeight = int(self.style.play.height)
        self.playWidth = int(self.style.play.width)
        self.playX = x
        self.playY = y
        self.playSprite = pyglet.sprite.Sprite(self.playImage, self.playX, self.playY)

        x = x + increaseX
        y = y + increaseY
    
        # create the playNext button properties
        self.playNextImage = pyglet.image.load(self.style.playNext.background_image[5:-2])
        self.playNextHeight = int(self.style.playNext.height)
        self.playNextWidth = int(self.style.playNext.width)
        self.playNextX = x
        self.playNextY = y
        self.playNextSprite = pyglet.sprite.Sprite(self.playNextImage, self.playNextX, self.playNextY)
    
