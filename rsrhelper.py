#!/usr/bin/env python3
# vim: number tabstop=4 expandtab shiftwidth=4 softtabstop=4 autoindent

"""
    rsrhelper.py – Recording internet radio streams
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
import eyed3

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

    ## parser = SafeConfigParser(os.environ)
    ## parser.read('config.ini')

    try:
        config.read_file(open(settings_base_dir + 'settings.ini'))
    except FileNotFoundError as err:
        print(str(err))
        print('Please copy/create the settings file to/in the appropriate location.')
        sys.exit()
    return dict(config.items())


def set_mp3_tags(mp3_file, artist, album, recording_date, url, icy_tags):
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
    audiofile.tag.recording_date = recording_date[:4]
    audiofile.tag.original_release_date = recording_date[:10]
    audiofile.tag.release_date = recording_date[:10]
    audiofile.tag.encoding_date = recording_date[:10]
    audiofile.tag.tagging_date = recording_date[:10]
    audiofile.tag.comments.set(os.getenv('USER', '????'), u'User')
    audiofile.tag.comments.set(recording_date, u'Recording Time')
    c = '\n'.join(icy_tags)

    ## audiofile.tag.comments.set(str(icy_tags), u'ICY-Tags')
    audiofile.tag.comments.set(c, u'ICY-Tags')
    audiofile.tag.user_text_frames.set(u"****", u"Rating")
    audiofile.tag.internet_radio_url = bytes(url, 'utf-8')


    audiofile.tag.save()
    print(audiofile.tag.version)


def show_mp3_tags(mp3_file):
    """
       show mp3 tags with a little help from eyeD3
    """

    ## cmd = 'eyeD3' + ' ' + '\"' + mp3_file + '\"'
    ## print(cmd)
    os.system('eyeD3' + ' ' + '\"' + mp3_file + '\"')


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
    file.write('Album: ' + album + '\n')
    file.write('Artist: ' + artist + '\n')
    file.write('\n')
    for i in tags:
        file.write(str(i) + '\n')

    file.close()

def list_stations(args):
    """
        list all radio stations in settings.ini
    """

    settings = read_settings()
    for key in sorted(settings['STATIONS']):
        print(key)


def icy_tag(log):
    """ Search for Icy-Tags in Log-File
        return list with Icy-Tags
    """
    icy_list = []

    ## print(log)
    with open(log) as f:
        content = f.readlines()
        for line in content:
            line = re.sub('http debug: ', '', line)
            if 'Icy' in line:
                icy_list.append(line.rstrip('\n'))
                print(line, end='')
            if 'icy' in line:
                icy_list.append(line.rstrip('\n'))
                print(line, end='')
        f.close()
        return icy_list

