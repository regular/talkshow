# README for KommHELP Talkshow

Talkshow is a hierarchical sound board application for portable touch screen computers. It is meant to help non-speaking people.

## MOTIVATION

Non-speaking people depend on special devices to communicate with the people that surround them. There are devices on the market that play pre-recorded sound samples by pressing a button and allow the user to change sample sets according to context. However, these special device are ridiculously expensive.

With Talkshow, we try to provide a solution based solely on Open Source software that runs on a cheap Netbook with a touch screen.

## LICENCE

Talkshow open source software licensed under the terms of the GPLv3, which guarantees end users (individuals, organizations, companies) the freedoms to use, study, share (copy), and modify the software. If you make changes to the code however, you need to make the source code of these changes available to the public.

## INSTALLATION

### Installation instructions when downloading windows exe:

* Download the talkshow.exe file
* Download and install the VLC media player from [this direct link](https://get.videolan.org/vlc/2.1.3/win32/vlc-2.1.3-win32.exe) or choose another version from [https://www.videolan.org/](https://www.videolan.org/). Please make sure it's 32 bit.
* Create a folder called "content" next to the talkshow.exe file, and fill it with subfolders containing media files and optionally png images (see usage instructions below).

You should now be able to use run talkshow. In case of problems, please send me (joe.schaul@gmail.com) the debug.log file that was created next to the talkshow.exe file.

### Advanced: install from source

Please see [installation from source](/doc/INSTALLATION_FROM_PYHON_SOURCE) if you want to run the python source version of KommHELP talkshow or if you want to make changes to the code.

## USAGE / CREATING CONTENT [usage]

The user interface consists of colored rectangles that either play a sound or contain more colored rectangles.
All rectangles have a caption and optionally may have an associated icon (.png).
You create this hierarchy of rectangles by creating a hierarchy of subdirectories in the content directory, one subdirectory per rectangle. Each subdirectory may contain more subdirectories or a sound file (see [supported formats](#formats) and an image that will be used as the rectangle's icon. The sound file will be played once the rectangle is touched in the User Interface. The name of the directory will be used as the caption of the rectangle if there is no image.

See the provided content directory structure as an example.

If you create sample sets this way, please make them available to the public. I would be happy to hear about it, please contact [http://kommhelp.de/](http://kommhelp.de/index.php/impressum-kontakt-top) info@kommhelp.de

The buttons to the left have the following meaning: 1) Play an alarm signal, 2) go to upper directory ("content"), 3) go back one level, 4) quit the program.
The buttons to the right allow you to set the volume of the program (it's the program's internal volume, not your computer master volume)

## TROUBLESHOOTING

A log file called `debug.log` and `warn.log` is created in the folder of the executable: any errors occurring will be logged there. In case of issues, send us an email and attach both files, so it's easier for us to find out what the problem is.

## Technical details

KommHELP Talkshow has been written in Python and requires :

* Python pyglet library (bundled with the .exe file, BSD licensed)
* Python tinycss library (bundled with the .exe file, BSD licensed)
* VLC media player (more precisely the libvlc part of VLC. VLC needs to be installed separately, GPL licensed)

It has been tested on Windows and linux, but should also work on Mac OS (not tested yet). It is based on 32bit Python 2.7 with the VLC 32 bit version. If both VLC and your version of Python are 64 bit, it can also work without further changes.

See [installation from source](doc/INSTALLATION_FROM_PYHON_SOURCE) for more details on dependencies. 

## BACKGROUND

KommHELP is a non-profit association based in Berlin, Germany that develops hardware and software solutions for people with special communication needs. More information (in German) can be found here: [http://kommhelp.de/](http://kommhelp.de/)

### Developers:

* November, 7th 2009 -- Jan Bölsche <jan@muskelfisch.com>
* ...?
* February 2013 - February 2014 -- Joé Schaul <joe.schaul@gmail.com>



















