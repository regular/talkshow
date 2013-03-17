import talkshowConfig
import pyglet

#from widget import Widget
   
class CommandBar(object):
    
    def __init__(self, screen, orientation):

        self.style = talkshowConfig.config().parser.style
    
        # 0 = landscape; 1 = vertical
        self.orientation = orientation
        
        # calculate bar size by orientation property
        if self.orientation == 0:
            self.height = screen.h * self.style.commandBar.height #(int(self.style.commandBar.height.replace('%','')) / 100)
            self.width = screen.w * self.style.commandBar.width #(int(self.style.commandBar.width.replace('%','')) / 100)
        else:
            self.height = screen.h * self.style.sideBar.height #(int(self.style.sideBar.height.replace('%','')) / 100)
            self.width = screen.w * self.style.sideBar.width #(int(self.style.sideBar.width.replace('%','')) / 100)

        self.increaseX = 0;
        self.increaseY = 0;

class MenuBar(CommandBar):

    def __init__(self, screen, orientation=0):
        
        super(MenuBar, self).__init__(screen, orientation=0)
        
        # TODO: CALCULATE IT
        x = 0
        y = 0
        
        if self.orientation == 0:
            print "orientation 0"
            increaseX = int(self.style.warning.width.replace('px',''))
            increaseY = 0
        else:
            
            print "orientation 1"
            increaseX = 0            
            increaseY = int(self.style.warning.height.replace('px',''))            
        
        # create the warning button properties
        self.warningImage = pyglet.image.load(self.style.warning.background_image[5:-2])
        self.warningHeight = int(self.style.warning.height.replace('px',''))
        self.warningWidth = int(self.style.warning.width.replace('px',''))
        self.warningX = x
        self.warningY = y
        self.warningSprite = pyglet.sprite.Sprite(self.warningImage, self.warningX, self.warningY)

        x = x + increaseX
        y = y + increaseY
    
        # create the home button properties
        self.homeImage = pyglet.image.load(self.style.home.background_image[5:-2])
        self.homeHeight = int(self.style.home.height.replace('px',''))
        self.homeWidth = int(self.style.home.width.replace('px',''))
        self.homeX = x
        self.homeY = y
        self.homeSprite = pyglet.sprite.Sprite(self.homeImage, self.homeX, self.homeY)

        x = x + increaseX
        y = y + increaseY
    
        # create the back button properties
        self.backImage = pyglet.image.load(self.style.back.background_image[5:-2])
        self.backHeight = int(self.style.back.height.replace('px',''))
        self.backWidth = int(self.style.back.width.replace('px',''))
        self.backX = x
        self.backY = y
        self.backSprite = pyglet.sprite.Sprite(self.backImage, self.backX, self.backY)

        x = x + increaseX
        y = y + increaseY
    
        # create the settings button properties
        self.settingsImage = pyglet.image.load(self.style.settings.background_image[5:-2])
        self.settingsHeight = int(self.style.settings.height.replace('px',''))
        self.settingsWidth = int(self.style.settings.width.replace('px',''))
        self.settingsX = x
        self.settingsY = y
        self.settingsSprite = pyglet.sprite.Sprite(self.settingsImage, self.settingsX, self.settingsY)

        x = x + increaseX
        y = y + increaseY
    
        # create the shutDown button properties
        self.shutDownImage = pyglet.image.load(self.style.shutDown.background_image[5:-2])
        self.shutDownHeight = int(self.style.shutDown.height.replace('px',''))
        self.shutDownWidth = int(self.style.shutDown.width.replace('px',''))
        self.shutDownX = x
        self.shutDownY = y
        self.shutDownSprite = pyglet.sprite.Sprite(self.shutDownImage, self.shutDownX, self.shutDownY)


class PlayerBar(CommandBar):
    
    def __init__(self, screen, orientation=0):
        
        super(PlayerBar, self).__init__(screen, orientation=0)
        
        # TODO: CALCULATE IT
        x = 0
        y = 0
        
        if self.orientation == 0:
            increaseX = int(self.style.volumeDown.width.replace('px',''))
            increaseY = 0
        else:
            increaseX = 0
            increaseY = int(self.style.volumeDown.height.replace('px',''))            
        
        # create the volumeDown button properties
        self.volumeDownImage = pyglet.image.load(self.style.volumeDown.background_image[5:-2])
        self.volumeDownHeight = int(self.style.volumeDown.height.replace('px',''))
        self.volumeDownWidth = int(self.style.volumeDown.width.replace('px',''))
        self.volumeDownX = x
        self.volumeDownY = y
        self.volumeDownSprite = pyglet.sprite.Sprite(self.volumeDownImage, self.volumeDownX, self.volumeDownY)

        x = x + increaseX
        y = y + increaseY
    
        # create the volumeUp button properties
        self.volumeUpImage = pyglet.image.load(self.style.volumeUp.background_image[5:-2])
        self.volumeUpHeight = int(self.style.volumeUp.height.replace('px',''))
        self.volumeUpWidth = int(self.style.volumeUp.width.replace('px',''))
        self.volumeUpX = x
        self.volumeUpY = y
        self.volumeUpSprite = pyglet.sprite.Sprite(self.volumeUpImage, self.volumeUpX, self.volumeUpY)

        x = x + increaseX
        y = y + increaseY
    
        # create the playPrevious button properties
        self.playPreviousImage = pyglet.image.load(self.style.playPrevious.background_image[5:-2])
        self.playPreviousHeight = int(self.style.playPrevious.height.replace('px',''))
        self.playPreviousWidth = int(self.style.playPrevious.width.replace('px',''))
        self.playPreviousX = x
        self.playPreviousY = y
        self.playPreviousSprite = pyglet.sprite.Sprite(self.playPreviousImage, self.playPreviousX, self.playPreviousY)

        x = x + increaseX
        y = y + increaseY
    
        # create the play button properties
        self.playImage = pyglet.image.load(self.style.play.background_image[5:-2])
        self.playHeight = int(self.style.play.height.replace('px',''))
        self.playWidth = int(self.style.play.width.replace('px',''))
        self.playX = x
        self.playY = y
        self.playSprite = pyglet.sprite.Sprite(self.playImage, self.playX, self.playY)

        x = x + increaseX
        y = y + increaseY
    
        # create the playNext button properties
        self.playNextImage = pyglet.image.load(self.style.playNext.background_image[5:-2])
        self.playNextHeight = int(self.style.playNext.height.replace('px',''))
        self.playNextWidth = int(self.style.playNext.width.replace('px',''))
        self.playNextX = x
        self.playNextY = y
        self.playNextSprite = pyglet.sprite.Sprite(self.playNextImage, self.playNextX, self.playNextY)
    
