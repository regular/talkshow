# -*- coding: utf-8 -*-
'''
Configuration file for talkshow. Change global settings such as scan mode or fullscreen here.
You may also change directory and file name for the style sheet used.

@author: Joé
'''


# The directory containing menu images and the .CSS style file:
styleDirectory = "style"

# The filename of the .CSS style file
styleFilename = 'theme1.css'


# Scan mode: 1 = on initially; 0 = off initially
# DEFAULT: scanOnDefault = 0
scanOnDefault = 0

# Full Screen: 1 = on ; 0 = off 
# DEFAULT: fullScreen = 0
fullScreen = 0

# Window size: if fullScreen is off, you can put a height and width here
# if set to 0, the default from the style file is used; otherwise the values here are used
# recommended to leave these values at 0.
# DEFAULT: windowWidth = 0
# DEFAULT: windowHeight = 0
windowWidth = 0
windowHeight = 0





import os
import parseCSS

class config(object):
    def __init__(self):
        self.path = os.path.join(styleDirectory, styleFilename)
        self.parser = parseCSS.CSSParser(self.path)
        self.style = self.parser.style
