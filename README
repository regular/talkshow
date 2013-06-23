README for KommHELP Talkshow

Talkshow is a hierarchical sound board application for portable touch screen computers. It is meant to help non-speaking people.

Talkshow is based on python and the pyglet library. It runs on Windows, OS X and Linux (not tested yet)

MOTIVATION

Non-speaking people depend on special devices to communicate with the people that surround them. There are devices on the market that play pre-recorded sound samples by pressing a button and allow the user to change sample sets according to context. However, these special device are ridiculously expensive.

With Talkshow, we try to provide a solution based solely on Open Source software that runs on a cheap Netbook with a touch screen.

LICENCE

Talkshow is licensed under the terms of the GPL. This means you can use it for whatever purpose you like. If you make changes to the code however, you need to make these changes available to the public.

INSTALLATION

You need to install a python interpreter for your platform (ActivePython for Windows for example) and the pyglet library, and the tinyCSS library.
I suggest Python version 2.7.XX for now, this module has not been tested on Python 3 and may fail.
Pyglet can be found here: http://www.pyglet.org/download.html
TinyCSS can be found here: http://pythonhosted.org/tinycss/ or here: https://pypi.python.org/pypi/tinycss
After you have installed these components, simply put the files that make up Talkshow into a new directory, open a command line and type:
<path-to-python-interpreter>/python talkshow.py

On windows, this might look like this:

c:\Python27\python talkshow.py
 
USGAE / CREATING CONTENT

The user interface consists of colored rectangles that either play a sound or contain more colored rectangles.
All rectangles have a caption and optionally may have an associated icon.
You create this hierarchy of rectangles by creating a hierarchy of subdirectories in the content directory, one subdirectory per rectangle. Each subdirectory may contain more subdirectories or a sound file in wav format and an image in png format that will be used as the rectangle's icon. The sound file will be played once the rectangle is touched in the UI. The name of the directory will be used as the caption of the rectangle.
See the provided content directory structure as an example.

If you create sample sets this way, please make them available to the public. I would be happy to hear about it. (my email address is at the end of this file)

The buttons to the left have the following meaning: 1) Play an alarm signal, 2) go to upper directory ("content"), 3) go back one level, 4) quit the program.
The buttons to the right allow you to set the volume of the program (it's the program's internal volume, not your computer master volume)

TROUBLESHOOTING

If you encounter an error message like this:
"TypeError: unsupported operand type(s) for -: 'NoneType' and 'float'", read about it here http://overooped.com/post/93720695/deathtroid-crash 
A log file called warn.log is created in the folder of the executable: any errors occurring will be logged there. In case of issues, send me (Joé) an email and attach the warn.log file, so it's easier for me to figure out what the problem is.

BACKGROUND

KommHELP is a non-profit association based in Berlin, Germany that develops hardware and software solutions for people with special communication needs. More information (in German) can be found here: http://kommhelp.de/


-- November, 7th 2009 -- Jan Bölsche <jan@muskelfisch.com>

-- 23rd June 2013 -- Joé Schaul <joe.schaul     gmail.com  (replace the spaces with an @)>