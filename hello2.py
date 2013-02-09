# -*- coding: utf-8 -*-
'''
Created on 9 Feb 2013

@author: Joé
'''

import os
import parseCSS

dir = "prototype"
filename = 'theme1.css'

def main():
    
    
    path = os.path.join(dir, filename)
    parser = parseCSS.CSSParser(path)
    print parser.style.leftSide.width
    



if __name__ == '__main__':
    main()