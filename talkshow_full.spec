# -*- mode: python -*-
a = Analysis(['talkshow.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)


def Datafiles(*filenames, **kw):
    import os

    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

def DataDir(directoryname, **kw):
    ''' recursively collect and add all files under a certain directory'''

    return data_files

import os
data_list = []
for dirname, dirnames, filenames in os.walk('plugins'):
    for filename in filenames:
        data_list.append(os.path.join(dirname, filename))
vlc_plugins = Datafiles(*data_list, strip_path=False)


data_list = []
for dirname, dirnames, filenames in os.walk('style'):
    for filename in filenames:
        data_list.append(os.path.join(dirname, filename))
style = Datafiles(*data_list, strip_path=False)


data_list = []
for dirname, dirnames, filenames in os.walk('alarm'):
    for filename in filenames:
        data_list.append(os.path.join(dirname, filename))
alarm = Datafiles(*data_list, strip_path=False)


# add static files
other_data_files = Datafiles('README.md')
other_vlc = Datafiles('libvlc.dll', 'libvlccore.dll', 'npvlc.dll', 'axvlc.dll')

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
		  vlc_plugins,
	      style,
	      alarm,
	      other_vlc,
	      other_data_files,
          name='talkshow_includingVLC.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
