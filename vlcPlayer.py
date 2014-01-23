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


    def stop(self):
        self.player.stop()


    def play(self, path_to_media_file):
        if not os.path.isfile(path_to_media_file):
            warn("This file: {0} does not exist. Full path: {1}".format(path_to_media_file, os.path.abspath(path_to_media_file)))
            return
        try:
            media = self.instance.media_new(path_to_media_file)
        except Exception as e:
            logger.exception("exception! {0}".format(e))
            warn('NameError: %s (LibVLC %s)' % (sys.exc_info()[1],vlc.libvlc_get_version()))
        self.player.set_media(media)
        self.player.play()


AUDIO_FORMATS = ["*.2sf", "*.2sflib", "*.3ga", "*.4mp", "*.669", "*.6cm", "*.8cm",
                 "*.8med", "*.8svx", "*.a2b", "*.a2i", "*.a2m", "*.a2p", "*.a2t",
                 "*.a2w", "*.a52", "*.aa", "*.aa3", "*.aac", "*.aax", "*.ab", "*.abc",
                 "*.abm", "*.ac3", "*.acd", "*.acd-bak", "*.acd-zip", "*.acm", "*.acp",
                 "*.act", "*.adg", "*.adt", "*.adts", "*.adv", "*.afc", "*.agm", "*.agr",
                 "*.ahx", "*.aif", "*.aifc", "*.aiff", "*.aimppl", "*.ais", "*.akp", "*.al",
                 "*.alac", "*.alaw", "*.alc", "*.all", "*.als", "*.amf", "*.amr", "*.ams",
                 "*.ams", "*.amxd", "*.amz", "*.aob", "*.ape", "*.apf", "*.apl", "*.aria",
                 "*.ariax", "*.asd", "*.ase", "*.at3", "*.atrac", "*.au", "*.au", "*.aud",
                 "*.aup", "*.avastsounds", "*.avr", "*.awb", "*.ay", "*.b4s", "*.band",
                 "*.bap", "*.bcs", "*.bdd", "*.bidule", "*.bnk", "*.bonk", "*.box",
                 "*.brstm", "*.bun", "*.bwf", "*.bwg", "*.bww", "*.c01", "*.caf",
                 "*.caff", "*.cda", "*.cdda", "*.cdlx", "*.cdo", "*.cdr", "*.cel",
                 "*.cfa", "*.cfxr", "*.cgrp", "*.cidb", "*.ckb", "*.ckf", "*.cmf",
                 "*.conform", "*.copy", "*.cpr", "*.cpt", "*.csh", "*.cts", "*.cwb",
                 "*.cwp", "*.d00", "*.d01", "*.dcf", "*.dcm", "*.dct", "*.ddt", "*.dewf",
                 "*.df2", "*.dfc", "*.dff", "*.dig", "*.dig", "*.djr", "*.dls", "*.dm",
                 "*.dmc", "*.dmf", "*.dmsa", "*.dmse", "*.dra", "*.drg", "*.ds", "*.ds2",
                 "*.dsf", "*.dsm", "*.dsp", "*.dss", "*.dtm", "*.dts", "*.dtshd", "*.dvf",
                 "*.dw", "*.dwa", "*.dwd", "*.ear", "*.efa", "*.efe", "*.efk", "*.efq",
                 "*.efs", "*.efv", "*.emd", "*.emp", "*.emx", "*.emy", "*.eop", "*.esps",
                 "*.evr", "*.expressionmap", "*.f2r", "*.f32", "*.f3r", "*.f4a", "*.f64",
                 "*.far", "*.fda", "*.fdp", "*.fev", "*.fff", "*.flac", "*.flp", "*.fls",
                 "*.fpa", "*.frg", "*.fsb", "*.fsm", "*.ftm", "*.ftm", "*.ftmx", "*.fzb",
                 "*.fzf", "*.fzv", "*.g721", "*.g723", "*.g726", "*.gbproj", "*.gbs",
                 "*.gig", "*.gio", "*.gio", "*.gm", "*.gp5", "*.gpbank", "*.gpk",
                 "*.gpx", "*.gro", "*.groove", "*.gsm", "*.gsm", "*.h0", "*.hdp",
                 "*.hma", "*.hmi", "*.hsb", "*.iaa", "*.ics", "*.iff", "*.igp",
                 "*.igr", "*.imf", "*.imp", "*.ins", "*.ins", "*.ins", "*.isma",
                 "*.it", "*.iti", "*.itls", "*.its", "*.jam", "*.jam", "*.jo",
                 "*.jo-7z", "*.k25", "*.k26", "*.kar", "*.kfn", "*.kin", "*.kit",
                 "*.kmp", "*.koz", "*.koz", "*.kpl", "*.krz", "*.ksc", "*.ksf",
                 "*.ksm", "*.kt2", "*.kt3", "*.ktp", "*.l", "*.la", "*.lof",
                 "*.logic", "*.lqt", "*.lso", "*.lvp", "*.lwv", "*.m1a", "*.m3u",
                 "*.m3u8", "*.m4a", "*.m4b", "*.m4p", "*.m4r", "*.ma1", "*.mbr",
                 "*.mdc", "*.mdl", "*.med", "*.mgv", "*.mid", "*.midi", "*.mini2sf",
                 "*.minincsf", "*.minipsf", "*.minipsf2", "*.miniusf", "*.mka",
                 "*.mlp", "*.mmf", "*.mmm", "*.mmp", "*.mmp", "*.mmpz", "*.mo3",
                 "*.mod", "*.mogg", "*.mp1", "*.mp2", "*.mp3", "*.mp_", "*.mpa",
                 "*.mpc", "*.mpdp", "*.mpga", "*.mpu", "*.mscx", "*.mscz", "*.msv",
                 "*.mt2", "*.mt9", "*.mte", "*.mtf", "*.mti", "*.mtm", "*.mtp",
                 "*.mts", "*.mu3", "*.mui", "*.mus", "*.mus", "*.mus", "*.musa",
                 "*.musx", "*.mux", "*.mux", "*.muz", "*.mwand", "*.mws", "*.mx3",
                 "*.mx4", "*.mx5", "*.mx5template", "*.mxl", "*.mxmf", "*.myr",
                 "*.mzp", "*.nap", "*.narrative", "*.nbs", "*.ncw", "*.nkb",
                 "*.nkc", "*.nki", "*.nkm", "*.nks", "*.nkx", "*.nml", "*.note", "*.npl",
                 "*.nra", "*.nrt", "*.nsa", "*.nsf", "*.nst", "*.ntn", "*.nvf", "*.nwc",
                 "*.obw", "*.odm", "*.ofr", "*.oga", "*.ogg", "*.okt", "*.oma", "*.omf",
                 "*.omg", "*.omx", "*.opus", "*.orc", "*.ots", "*.ove", "*.ovw", "*.ovw",
                 "*.pac", "*.pandora", "*.pat", "*.pbf", "*.pca", "*.pcast", "*.pcg", "*.pcm",
                 "*.pd", "*.peak", "*.pek", "*.pho", "*.phy", "*.pk", "*.pkf", "*.pla", "*.pls",
                 "*.plst", "*.ply", "*.pna", "*.pno", "*.ppc", "*.ppcx", "*.prg", "*.prg", "*.psf",
                 "*.psf1", "*.psf2", "*.psm", "*.psy", "*.ptcop", "*.ptf", "*.ptm", "*.pts",
                 "*.ptx", "*.pvc", "*.q1", "*.q2", "*.qcp", "*.r", "*.r1m", "*.ra", "*.rad",
                 "*.ram", "*.raw", "*.rax", "*.rbs", "*.rbs", "*.rcy", "*.record", "*.rex",
                 "*.rfl", "*.rgrp", "*.rip", "*.rmf", "*.rmi", "*.rmj", "*.rmm", "*.rmx",
                 "*.rng", "*.rns", "*.rol", "*.rsf", "*.rsn", "*.rso", "*.rta", "*.rti",
                 "*.rtm", "*.rts", "*.rvx", "*.rx2", "*.s3i", "*.s3m", "*.s3z", "*.saf",
                 "*.sam", "*.sap", "*.sb", "*.sbg", "*.sbi", "*.sbk", "*.sc2", "*.scs11",
                 "*.sd", "*.sd", "*.sd2", "*.sd2f", "*.sdat", "*.sdii", "*.sds", "*.sdt",
                 "*.sdx", "*.seg", "*.seq", "*.ses", "*.sesx", "*.sf", "*.sf2", "*.sfap0",
                 "*.sfk", "*.sfl", "*.sfpack", "*.sfs", "*.sgp", "*.shn", "*.sib", "*.sid",
                 "*.slp", "*.slx", "*.sma", "*.smf", "*.smp", "*.smp", "*.smpx", "*.snd",
                 "*.snd", "*.snd", "*.sng", "*.sng", "*.sns", "*.snsf", "*.sou", "*.sph",
                 "*.sppack", "*.sprg", "*.spx", "*.sseq", "*.sseq", "*.ssnd", "*.stap",
                 "*.stm", "*.stx", "*.sty", "*.sty", "*.svd", "*.svx", "*.sw", "*.swa", "*.swav",
                 "*.sxt", "*.syh", "*.syn", "*.syn", "*.syw", "*.syx", "*.tak", "*.tak", "*.td0",
                 "*.tfmx", "*.tg", "*.thx", "*.tm2", "*.tm8", "*.tmc", "*.toc", "*.trak", "*.tsp",
                 "*.tta", "*.tun", "*.txw", "*.u", "*.u8", "*.uax", "*.ub", "*.ulaw", "*.ult",
                 "*.ulw", "*.uni", "*.usf", "*.usflib", "*.ust", "*.uw", "*.uwf", "*.v2m",
                 "*.vag", "*.val", "*.vap", "*.vb", "*.vc3", "*.vdj", "*.vgm", "*.vgz",
                 "*.vlc", "*.vmd", "*.vmf", "*.vmf", "*.vmo", "*.voc", "*.voi", "*.vox",
                 "*.voxal", "*.vpl", "*.vpm", "*.vpw", "*.vqf", "*.vrf", "*.vsq", "*.vtx",
                 "*.vyf", "*.w01", "*.w64", "*.wand", "*.wav", "*.wav", "*.wave", "*.wax",
                 "*.wem", "*.wfb", "*.wfd", "*.wfm", "*.wfp", "*.wma", "*.wow", "*.wpk",
                 "*.wpp", "*.wproj", "*.wrk", "*.wtpl", "*.wtpt", "*.wus", "*.wut", "*.wv",
                 "*.wvc", "*.wve", "*.wwu", "*.wyz", "*.xa", "*.xa", "*.xfs", "*.xi", "*.xm",
                 "*.xmf", "*.xmi", "*.xmz", "*.xp", "*.xpf", "*.xrns", "*.xsb", "*.xsp", "*.xspf",
                 "*.xt", "*.xwb", "*.ym", "*.yookoo", "*.zpa", "*.zpl", "*.zvd", "*.zvr"]