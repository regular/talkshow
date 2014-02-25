import os
import sys
from talkshowLogger import logger

def getRelativePath(path):
    '''
    Get the right path irrespective whether the file is within the compiled .exe or in source
    '''
    logger.debug("sys.executable under {0} ABSOLUTE={1}".format(os.path.dirname(sys.executable), os.path.abspath(os.path.dirname(sys.executable))))
    logger.debug("__file__ under {0} ABSOLUTE={1}".format(os.path.dirname(__file__), os.path.abspath(os.path.dirname(__file__))))

    application_path = os.path.dirname(__file__)

    if getattr(sys, 'frozen', False):
        logger.debug("starting from frozen .exe file")
    elif __file__:
        logger.debug("starting from python source")
    else:
        logger.warn("talkshow.getRelativePath function has a problem...")

    returnpath = os.path.join(application_path, path)

    logger.debug("returnpath = {0} ABS={1}".format(returnpath, os.path.abspath(returnpath)))

    return returnpath