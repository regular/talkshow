# -*- coding: utf-8 -*-
'''
Configuration file for talkshow. Change global settings such as scan mode or fullscreen here.
You may also change directory and file name for the style sheet used.

@author: Joé
'''


# Scan mode: 1 = on initially; 0 = off initially
# DEFAULT: scanOnDefault = 0
scanOnDefault = 0

# Full Screen: 1 = on ; 0 = off 
# DEFAULT: fullScreen = 0
fullScreen = 0

# noTextIfImageAvailable: set to 1 in order not to display any text when there
# is an image (.png) in the folder.
#DEFAULT: noTextIfImageAvailable = 0
noTextIfImageAvailable = 1


# Window size: if fullScreen is off, you can put a height and width here
# if set to 0, the default from the style file is used (800x600); otherwise the values here are used
# DEFAULT: windowWidth = 0
# DEFAULT: windowHeight = 0
windowWidth = 0
windowHeight = 0

# The directory containing menu images and the .CSS style file:
#DEFAULT: styleDirectory = "style"
styleDirectory = 'style'

# The filename of the .CSS style file
#DEFAULT: styleFilename = 'theme1.css'
styleFilename = 'theme1.css'









# do not change the code below!

import os
import parseCSS

class config(object):    
    
    ## other default sizes that *could* be changed     
    ## but these sizes are overridden by those in the style.css anyway.
    FONT_SIZE_DEFAULT = 32
    FONT_SIZE_VOL = 16
    
    try: NO_TEXT_IF_IMAGE_AVAILABLE = bool(noTextIfImageAvailable)
    except: NO_TEXT_IF_IMAGE_AVAILABLE = 0
    
    def __init__(self):
        self.path = os.path.join(styleDirectory, styleFilename)
        self.parser = parseCSS.CSSParser(self.path)
        self.style = self.parser.style
