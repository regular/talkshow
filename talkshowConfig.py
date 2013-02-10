# -*- coding: utf-8 -*-
'''
Created on 9 Feb 2013

@author: Joé
'''

import os
import parseCSS

dir = "style"
filename = 'theme1.css'

class config(object):
    def __init__(self):
        self.path = os.path.join(dir, filename)
        self.parser = parseCSS.CSSParser(self.path)
        self.style = self.parser.style

