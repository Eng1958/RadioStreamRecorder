#!/usr/bin/env python3
# vim: number tabstop=4 expandtab shiftwidth=4 softtabstop=4 autoindent

"""
    rsrhelper.py - Recording internet radio streams
    Copyright (C) 2017  Dieter Engemann <dieter@engemann.me>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    I found a lot of help with this tag example
        https://github.com/nicfit/eyed3/blob/master/examples/tag_example.py

"""

import argparse
import configparser
import sys
import os
import re
import errno
import subprocess
from time import strftime, localtime
try:
    import eyed3
except ImportError:
    print('eyed3 is not installed, please install it!')
    sys.exit(1)

## MP3SPLT = '/usr/bin/mp3splt'
## CVLC = '/usr/bin/cvlc'

def print_args(args):
    """
        Print the arguments if verbose is true
    """
    if args.verbose:
        print("artist:   " + str(args.artist))
        print("album:    " + str(args.album))
        print("duration: " + str(args.duration))
        print("station:  " + args.station)


def check_duration(value):
    """
        value:  Duration of recording time in minutes. the duration must be a
                positive integer
    """
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Duration must be a positive integer.')

    if value < 1:
        raise argparse.ArgumentTypeError('Duration must be a positive integer.')
    else:
        return value


def read_settings():
    """
        read settings from configuration file
    """

    settings_base_dir = ''
    if sys.platform.startswith('linux'):
        settings_base_dir = os.getenv('HOME') + os.sep + '.config' \
            + os.sep + 'RadioStreamRecorder'
    elif sys.platform == 'win32':
        settings_base_dir = os.getenv('LOCALAPPDATA') + os.sep + \
            'RadioStreamRecorder'
    settings_base_dir += os.sep
    config = configparser.ConfigParser()

    try:
        config.read_file(open(settings_base_dir + 'settings.ini'))
    except FileNotFoundError as err:
        print(str(err))
        print('Please copy/create the settings file to/in the appropriate location.')
        sys.exit()
    return dict(config.items())


def set_mp3_tags(mp3_file, args, recording_date, url, icy_tags):
    """
        Set some tags for recorded mp3 file

        recording_date has date and time YYYY-MM-DD_HH-MM-SS
    """

    audiofile = eyed3.load(mp3_file)
    if audiofile.tag is None:
        audiofile.initTag()

    if args.artist is None:
        artist = 'Undefined'
    else:
        artist = args.album

    if args.album is None:
        album = 'Undefined'
    else:
        album = args.album

    audiofile.tag.album = album
    audiofile.tag.artist = artist
    audiofile.tag.album_artist = artist
    audiofile.tag.title = album + ' - ' + artist
    audiofile.tag.track_num = (1, 1)
    audiofile.tag.recording_date = recording_date[:4]
    audiofile.tag.original_release_date = recording_date[:10]
    audiofile.tag.release_date = recording_date[:10]
    audiofile.tag.encoding_date = recording_date[:10]
    audiofile.tag.tagging_date = recording_date[:10]
    audiofile.tag.comments.set(os.getenv('USER', '????'), u'User')
    audiofile.tag.comments.set(recording_date, u'Recording Time')
    ## comment = '\n'.join(icy_tags)

    # audiofile.tag.comments.set(comment, u'ICY-Tags')
    audiofile.tag.comments.set(icy_tags, u'ICY-Tags')
    audiofile.tag.user_text_frames.set(u"****", u"Rating")
    audiofile.tag.internet_radio_url = bytes(url, 'utf-8')


    audiofile.tag.save()
    print(audiofile.tag.version)


def get_mp3_tags(mp3_file):
    """
       show mp3 tags with a little help from eyeD3
    """

    output = subprocess.check_output('eyeD3 --no-color \"%s\"' % (mp3_file),
                                     shell=True, universal_newlines=True)
    return output

def remove_cvlc_log(log):
    """ remove logfile because cvlc appends log.
        check if a file exists on disk
        if exists, delete it else show message on screen
    """
    if os.path.exists(log):
        try:
            os.remove(log)
        except OSError as error:
            ## print ("Error: %s - %s." % (e.log,e.strerror))
            if error.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred
    else:
        print("Sorry, I can not find %s file." % log)


def create_log(log, args):
    """
        Create a logfile and write some information to this logfile.
    """

    file = open(log, 'w')

    file.write('Station: ' + args.station + '\n')
    file.write('Album: ' + args.album + '\n')
    file.write('Artist: ' + args.artist + '\n')
    file.write('\n')

    file.close()

def list_stations():
    """
        list all radio stations in settings.ini
    """

    settings = read_settings()
    for key in sorted(settings['STATIONS']):
        print(key)


def icy_tag(log):
    """ Search for Icy-Tags in Log-File
        return string with Icy-Tags
    """
    icy_list = []

    with open(log) as fds:
        content = fds.readlines()
        for line in content:
            line = re.sub('http debug: ', '', line)
            if 'Icy' in line:
                icy_list.append(line.rstrip('\n'))
                print(line, end='')
            if 'icy' in line:
                icy_list.append(line.rstrip('\n'))
                print(line, end='')
        fds.close()

        return '\n'.join(icy_list)
        ### return icy_list

def start_recording(args, recording_directory, streamurl, mp3splitter, recorder):
    """
        start recording directly or at a later time with a little help
        from the at-command
    """

    recording_date = strftime("%Y-%m-%d_%H-%M", localtime())
    file = '%s-%s-%s-%s' % (args.station, \
                            recording_date,
                            args.artist, args.album)
    file = file.replace(' ', '_')

    mp3_file = recording_directory + '/' + file + '.mp3'
    log_file = recording_directory + '/' + file + '.log'
    if args.verbose:
        print(mp3_file)
        print(log_file)

    if args.recordingtime is None:
        start_recording_direct(args, mp3_file, log_file, recording_date, streamurl, recorder, mp3splitter)

    else:
        start_recording_by_time(args)


def start_recording_direct(args, mp3_file, log_file, recording_date, streamurl, recorder, mp3splitter):
    """
        start recording directly
    """
    cvlclog = 'cvlc.log'

    # record the stream now
    remove_cvlc_log(cvlclog)

    if not os.path.exists(recorder):
        print('Error: %s is not installed' % (recorder))
        return ''

    # build command to record a stream with cvlc. Some informatione
    # during recording will be logged in cvlc.log
    cmd = [recorder]
    cmd += ['--verbose=2']
    cmd += ['--extraintf=http:logger']
    cmd += ['--file-logging']
    cmd += ['--logfile=%s' % (cvlclog)]
    cmd += [streamurl]
    cmd += ['--sout=#std{access=file,mux=raw,dst=%s' % (mp3_file)]

    if args.verbose:
        print(cmd)
    # Uebergabe des Kommandos und der Parameter muss als Liste erfolgen
    try:
        subprocess.check_output(cmd, shell=False,
                                stderr=subprocess.STDOUT,
                                timeout=(args.duration * 60))
    except subprocess.TimeoutExpired as error:
        print('recording is finished')
        print(error)


        icy_tags = icy_tag(cvlclog)
        create_log(log_file, args)

        ### add_to_log(icy_tags, log_file)

        set_mp3_tags(mp3_file, args, recording_date,
                     streamurl, icy_tags)

        out = get_mp3_tags(mp3_file)
        print(out)
        add_to_log(out, log_file)

        out = split_mp3(args, mp3_file, mp3splitter)
        print(out)
        add_to_log(out, log_file)


def start_recording_by_time(args):
    """
        Start recording with at command.  Build a script and run it with
        at command.
        at -f <script> time
    """

    # remove argument --recordingtime to run this script
    file = open("/tmp/at-script.sh", 'w')
    cmd = ''
    count = 0
    while count < len(sys.argv):
        print(count, sys.argv[count])
        if sys.argv[count] == '--recordingtime':
            count = count + 2
        # write cmd to file
        # run at cmd
        part = sys.argv[count]
        if ' ' in part:
            part = '\"' + part + '\"'
        cmd = cmd + str(part) + ' '
        file.write(part + ' ')

        count = count + 1

    file.write('\n')
    file.close()
    print(cmd)

    print("Start Recording at %s" % (args.recordingtime))
    os.system('at -f %s %s' % ('/tmp/at-script.sh', args.recordingtime))

def add_to_log(eyed3_output, log):
    """
        add eyeD3 output to logfile
    """

    file = open(log, 'a')
    file.write('\n')
    file.write(eyed3_output)
    file.close()

def split_mp3(args, mp3_file, mp3splitter):
    """Splits the recorded mp3 file into smaller pieces. Using mp3splt

        mp3splt -a -f -t 15.0 -o "@n-@f" -f blabla.mp3

        -q quit mode
        -a Die Option -a kann zusätzlich zum Anpassen der Splitpunkte genutzt
            werden, um mit der automatischen Erkennung von stillen Passagen
            die Präzision noch zu verbessern
        -f Frame-Modus
        -t Mit diesem Schalter erstellt mp3splt einfach eine endliche Zahl
            an Einzelteilen, die alle die vorgegebene Dauer haben
        -o Ausgabeformat
    """


    if not os.path.exists(mp3splitter):
        return ''

    if args.splittime is None:
        return ''

    cmd = [mp3splitter]
    cmd += ['-q']
    cmd += ['-a']
    cmd += ['-f']
    cmd += ['-t']
    cmd += ['%s' % (args.splittime)]
    cmd += ['-o']
    cmd += ['@f-@n']
    cmd += ['%s' % (mp3_file)]

    if args.verbose:
        print(cmd)

    # Uebergabe des Kommandos und der Parameter muss als Liste erfolgen
    try:
        output = subprocess.check_output(cmd, shell=False,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
        return output
    except subprocess.CalledProcessError as error:
        print(error.output)
        return

    # Remove original mp3-file after splitting
    os.remove(mp3_file)

