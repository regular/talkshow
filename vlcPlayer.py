"""
Module to configure and use the python bindings of libVLC to play back audio files.

Requires vlc.py python bindings

Requires vlc installed, or for windows, for your (64 or 32 bit) architecture, the correct
"libvlc.dll" and "libvlccore.dll" and a "plugins" directory on the current system path
"""

import vlc
import sys
import os

from talkshowLogger import logger
debug = logger.debug
info = logger.info
warn = logger.warn

class vlcPlayer(object):

    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()


    def play(self, path_to_media_file):
        if not os.path.isfile(path_to_media_file):
            warn("This file: {} does not exist. Full path: {}".format(path_to_media_file, os.path.abspath(path_to_media_file)))
            return
        try:
            media = self.instance.media_new(path_to_media_file)
        except Exception as e:
            logger.exception("exception! {}".format(e))
            warn('NameError: %s (LibVLC %s)' % (sys.exc_info()[1],vlc.libvlc_get_version()))
        self.player.set_media(media)
        self.player.play()
