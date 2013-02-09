# -*- coding: utf-8 -*-
'''
Created on 9 Feb 2013

@author: Joé
'''

import os
import parseCSS

dir = "prototype"
filename = 'theme1.css'

path = os.path.join(dir, filename)
parser = parseCSS.CSSParser(path)
style = parser.style



def main():    
    
    print parser.style.leftSide.width
    



if __name__ == '__main__':
    main()