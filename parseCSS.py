'''
Created on 9 Feb 2013

@author: Joe Schaul <joe.schaul@gmail.com>
'''

import tinycss
import os

from talkshowLogger import logger

debug = logger.debug
info = logger.info
warn = logger.warn

class Struct(object):
    '''Struct to convert a python dict (which you access by myDict["key1"]) into a class, 
    so that you can access properties by myDict.key1    
    '''
    def __init__(self, **entries): 
        self.__dict__.update(entries)    

class CSSParser(object):
    '''
    parses css file using tinycss and obtains a "style" object containing css elements that you can access by
    style.page.width if you have a css file like
    #page { width: 50% }
    
    Note that # and . prefixes of css attributes are removed.
    Note that attributes such as background-color are changed to background_color (dashes replaced by underscores)
    
    percentage values are parsed to floating point numbers, everything else remains a string. (also e.g. 5px remains a string)
    
    '''

    def __init__(self, filename):

        self.filename=filename
        if os.path.exists(filename):
            self.parseFile()
        else:
            warn( "filename %s not found" % filename)
        
    def parseFile(self):
        parser = tinycss.make_parser()
        stylesheet = parser.parse_stylesheet_file(self.filename)
        
        self.basicDict = {rule.selector.as_css():{declaration.name:declaration.value.as_css() for declaration in rule.declarations  } for rule in stylesheet.rules}
        try:
            self.dict = {removeHashesAndDots(rule.selector.as_css()):{declaration.name:makeFloatsOutOfPercentages(declaration.value.as_css()) for declaration in rule.declarations  } for rule in stylesheet.rules}
        except Exception, e:
            warn( "problem with submethod, only generating basicDict")
            raise e
        try:
            self.style = Struct(**{removeHashesAndDots(rule.selector.as_css()):Struct(**{declaration.name.replace('-','_'):makeFloatsOutOfPercentages(declaration.value.as_css()) for declaration in rule.declarations  }) for rule in stylesheet.rules})
        except Exception, e:
            warn( "problem with submethod, only generating basicDict and dict")
            raise e
            
            
def makeFloatsOutOfPercentages(css_value_string):
    '''take a css attribute value, and if it's a percentage value, e.g. "25%" (for width)
      or "20% 50%" (for padding), and return float type (25.0) or list of floats ([20.0, 50.0]).
      otherwise just return the string as it was.
    '''
    if '%' in css_value_string:
        results = css_value_string.replace('%', '').split()       
        
        if len(results) ==1:
            return float(results[0])
        else:
            return map(float, results) 
    elif 'px' in css_value_string :        
        results = css_value_string.replace('px', '').split()
        
        if len(results) ==1:
            return int(results[0])
        else:
            return map(int, results)
    else:        
        return css_value_string
        
        
        

def removeHashesAndDots(css_attribute):
    return css_attribute.replace('#', '').replace('.','').replace(':','')


