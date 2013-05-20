# -*- coding: utf-8 -*-
'''
Created on 20 May 2013

@author: Joé Schaul
'''

import logging

# create logger
logger = logging.getLogger('talkshow')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fileDebugLogger = logging.FileHandler('debug.log')
fileDebugLogger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fileWarnLogger = logging.FileHandler('warn.log')
fileWarnLogger.setLevel(logging.WARN)

# create console handler 
consoleLogger = logging.StreamHandler()
consoleLogger.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileDebugLogger.setFormatter(formatter)
consoleLogger.setFormatter(formatter)
fileWarnLogger.setFormatter(formatter)


# add the handlers to the logger
logger.addHandler(fileDebugLogger)
logger.addHandler(consoleLogger)
logger.addHandler(fileWarnLogger)

        