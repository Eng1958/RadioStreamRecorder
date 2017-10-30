#!/usr/bin/env python3
# vim: number tabstop=4 expandtab shiftwidth=4 softtabstop=4 autoindent

"""
    RadioStreamRecorder.py – Recording internet radio streams
    with a liitle help from vlc/cvlc and some other useful tool
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
## from configparser import SafeConfigParser
import sys
import os
import subprocess
from time import gmtime, strftime
import eyed3

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

    ## parser = SafeConfigParser(os.environ)
    ## parser.read('config.ini')

    try:
        config.read_file(open(settings_base_dir + 'settings.ini'))
    except FileNotFoundError as err:
        print(str(err))
        print('Please copy/create the settings file to/in the appropriate location.')
        sys.exit()
    return dict(config.items())


def radio_stream_recording(args):
    """
        run recording of stream with a little help from cvlc
    """

    streamurl = ''
    cvlclog = 'cvlc.log'

    print("Radio Stream-Recorder")

    if args.verbose:
        print("artist:   " + str(args.artist))
        print("album:    " + str(args.album))
        print("duration: " + str(args.duration))
        print("station:  " + args.station)

    settings = read_settings()

    # get radio station
    try:
        streamurl = settings['STATIONS'][args.station]
        if args.verbose:
            print(streamurl)
    except KeyError:
        print('Unkown station name: ' + args.station)
        sys.exit()

    # get target_dir for recorded file
    try:
        ## recording_directory = settings['GLOBAL']['target_dir']
        recording_directory = os.path.expandvars(
            settings['GLOBAL']['target_dir'])
        if args.verbose:
            print(recording_directory)
    except KeyError:
        print('Unkown Recording directoy: ')
        sys.exit()

    # create recording directory if it doesn't exist
    if not os.path.isdir(recording_directory):
        print('No dir')
        try:
            os.makedirs(recording_directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                print(e.errno)
                raise
        exit(1)

    recording_date = strftime("%Y-%m-%d_%H-%M", gmtime())
    file = '%s-%s-(%s - %s)' % (args.station, \
                                recording_date,
                                args.artist, args.album)
    mp3_file = recording_directory + '/' + file + '.mp3'
    log_file = recording_directory + '/' + file + '.log'
    if args.verbose:
        print(mp3_file)
        print(log_file)

    remove_log(cvlclog)

    # build command to record a stream with cvlc
    cmd = ['/usr/bin/cvlc']
    cmd += ['--verbose=2']
    cmd += ['--extraintf=http:logger']
    cmd += ['--file-logging']
    cmd += ['--logfile=%s' % (cvlclog)]
    cmd += [streamurl]
    cmd += ['--sout=#std{access=file,mux=raw,dst=%s' % (mp3_file)]
    ## cmd += ['--sout=#std{access=file,mux=raw,dst=%s/%s' %
    ##        (recording_directory, mp3_file)]
    print(cmd)

    # Uebergabe des Kommandos und der Parameter muss als Liste erfolgen
    try:
        subprocess.check_output(cmd, shell=False,
                                stderr=subprocess.STDOUT,
                                timeout=(args.duration * 60))
    except subprocess.TimeoutExpired as e:
        print('recording is finished')
        print(e)

    icy_tags = icy_tag(cvlclog)
    recording_log(log_file, args.station, args.album, args.artist, icy_tags)

    set_mp3_tags(mp3_file, args.artist, args.album, recording_date, streamurl)

    show_mp3_tags(mp3_file)

def set_mp3_tags(mp3_file, artist, album, recording_date, url):
    """
        Set some tags for recorded mp3 file

        recording_date has date and time YYYY-MM-DD_HH-MM-SS
    """

    audiofile = eyed3.load(mp3_file)
    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.album_artist = artist
    audiofile.tag.title = album + ' - ' + artist
    audiofile.tag.track_num = (1, 1)
    ## audiofile.tag.recording_date = 2017
    audiofile.tag.recording_date = recording_date[:4]
    audiofile.tag.original_release_date = recording_date[:10]
    audiofile.tag.release_date = recording_date[:10]
    audiofile.tag.encoding_date = recording_date[:10]
    audiofile.tag.tagging_date = recording_date[:10]
    audiofile.tag.comments.set(os.getenv('USER', '????'), u'User')
    ## audiofile.tag.comments.set(u"Brownsville, Brooklyn", u"Origin")
    audiofile.tag.comments.set(recording_date, u'Recording Time')
    audiofile.tag.user_text_frames.set(u"****", u"Rating")
    audiofile.tag.internet_radio_url = bytes(url, 'utf-8')

    ## print(audiofile.version)
    ## print(audiofile.tag)

    ## print(dir(audiofile.tag))
    audiofile.tag.save()
    print(audiofile.tag.version)

def show_mp3_tags(mp3_file):
    """

    """
    cmd = 'eyeD3' + ' ' + '\"' + mp3_file + '\"'
    print(cmd)
    os.system(cmd)


def remove_log(log):
    """ remove logfile because cvlc appends log.
        check if a file exists on disk
        if exists, delete it else show message on screen
    """
    if os.path.exists(log):
        try:
            os.remove(log)
        except OSError as e:
            ## print ("Error: %s - %s." % (e.log,e.strerror))
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred
    else:
        print("Sorry, I can not find %s file." % log)

def recording_log(log, station, album, artist, tags):
    """
        Write some information and the ICY-Tags to a logfile.
    """

    file = open(log, 'w')

    file.write('Station: ' + station + '\n')
    file.write(album + '\n')
    file.write(artist + '\n')
    for i in tags:
        file.write(str(i) + '\n')

    file.close()

def list(args):
    """
        list all radio stations in settings.ini
    """

    settings = read_settings()
    for key in sorted(settings['STATIONS']):
        print(key)

def icy_tag(log):
    """ Serch for Icy-Tags in Log-File
        return list with Icy-Tags
    """
    icy_list = []

    print(log)
    with open(log) as f:
        content = f.readlines()
        for line in content:
            if 'Icy' in line:
                icy_list.append(line.rstrip('\n'))
                print(line, end='')
            if 'icy' in line:
                icy_list.append(line.rstrip('\n'))
                print(line, end='')
        f.close()
        return icy_list

def main():
    """
        this is the main function
    """

    # -----------------------------------------------------------------
    # get options
    #   -r --radiostation       Shortcut of radio station
    #   -l --recordinglength    Lenght of recording (in minutes)
    #   --album                  set ID-Tag album
    #   --artist                 set ID-Tag artist
    # -----------------------------------------------------------------

    parser = argparse.ArgumentParser(
        description='This program records internet radio streams. '
        'It is free software and comes with ABSOLUTELY NO WARRANTY.')

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_record = subparsers.add_parser('record', help='Record a station')
    parser_record.add_argument('station',
                               type=str, help='Name of the radio station '
                               '(see `radiorec.py list`)')
    parser_record.add_argument('duration',
                               type=check_duration,
                               help='Recording time in minutes')
    parser_record.add_argument('name',
                               nargs='?', type=str,
                               help='A name for the recording')
    parser_record.add_argument('-p', '--public',
                               action='store_true',
                               help="Public write permissions (Linux only)")
    parser_record.add_argument('-v', '--verbose',
                               action='store_true',
                               help="Verbose output")
    parser_record.add_argument('-a', '--album',
                               type=str,
                               help="album name")
    parser_record.add_argument('-t', '--artist',
                               type=str,
                               help="artist name")
    parser_record.set_defaults(func=radio_stream_recording)

    parser_list = subparsers.add_parser('list', help='List all known stations')
    parser_list.set_defaults(func=list)

    args = parser.parse_args()
    args.func(args)

    # print(args)


if __name__ == '__main__':
    main()
