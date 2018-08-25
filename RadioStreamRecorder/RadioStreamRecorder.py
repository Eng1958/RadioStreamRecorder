#!/usr/bin/env python3
# vim: number tabstop=4 expandtab shiftwidth=4 softtabstop=4 autoindent

"""
    RadioStreamRecorder.py - Recording internet radio streams
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

    You have to install the following modules and external applications
    1.  pip3 install eyed3
    2.  sudo apt-get install mp3splt
    3.  sudo apt-get install vlc
    4.  sudo apt-get install at

"""

import argparse
import sys
import os
import errno
## from time import strftime, localtime

## import RadioStreamRecorder.rsrhelper as rsrhelper
import rsrhelper as rsrhelper
### import rsrhelper

def radio_stream_recording(args):
    """
        run recording of stream with a little help from cvlc
    """

    print("Radio Stream-Recorder")

    rsrhelper.print_args(args)

    recording_directory, streamurl, mp3splitter, recorder = config(args.station)

    rsrhelper.start_recording(args, recording_directory, streamurl, mp3splitter, recorder)



def config(station):
    """
        returns: recording_directory, streamurl, mp3splitter, recorder
    """
    settings = rsrhelper.read_settings()

    # get MP3-Splitter
    try:
        mp3splitter = settings['GLOBAL']['MP3SPLT']
        if not os.path.isfile(mp3splitter):
            print('Warning: Mp3-Splitter [%s] doesn\'t exist' % (mp3splitter))
            sys.exit(1)
        else:
            print('Using Mp3-Splitter [%s]' % (mp3splitter))
    except KeyError:
        print('Warning: No Mp3-Splitter defined')
        pass

    # get vlc for recording
    try:
        recorder = settings['GLOBAL']['CVLC']
        if not os.path.isfile(recorder):
            print('Error: Recorder [%s] doesn\'t exist' % (recorder))
            sys.exit(1)
        else:
            print('Using Recorder [%s]' % (recorder))
    except KeyError:
        print('Error: No Recorder defined')
        pass


    # get radio station
    try:
        streamurl = settings['STATIONS'][station]
#        if args.verbose:
        print('Streaming-URL: %s' % (streamurl))
    except KeyError:
        print('Error: Unkown station name: ' + station)
        sys.exit()

    # get target_dir for recorded file
    try:
        recording_directory = os.path.expandvars(
            settings['GLOBAL']['target_dir'])
#        if args.verbose:
        print('Recording directory: %s' % (recording_directory))
    except KeyError:
        print('Unkown Recording directoy: ')
        sys.exit()

    # create recording directory if it doesn't exist
    if not os.path.isdir(recording_directory):
        try:
            os.makedirs(recording_directory)
        except OSError as err:
            if err.errno != errno.EEXIST:
                print(err.errno)
                raise
        exit(1)

    return recording_directory, streamurl, mp3splitter, recorder


def main():
    """
        this is the main function
    """

    # -----------------------------------------------------------------
    # get options
    # -----------------------------------------------------------------

    parser = argparse.ArgumentParser(
        description='This program records internet radio streams. '
        'It is free software and comes with ABSOLUTELY NO WARRANTY.')

    subparsers = parser.add_subparsers(help='sub-command help')

    # Parser for record argument and optional arguments
    parser_record = subparsers.add_parser('record', help='Record a station')
    parser_record.add_argument('station',
                               type=str, help='Name of the radio station '
                               '(see `radiorec.py list`)')
    parser_record.add_argument('duration',
                               type=rsrhelper.check_duration,
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
    parser_record.add_argument('-r', '--recordingtime',
                               type=str,
                               help="Recording time (at command)")
    parser_record.add_argument('-s', '--splittime',
                               type=str,
                               help="Split time")
    parser_record.set_defaults(func=radio_stream_recording)

    # Parser for list argument (no optional arguments)
    parser_list = subparsers.add_parser('list', help='List all known stations')
    parser_list.set_defaults(func=rsrhelper.list_stations)


    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()

if __name__ == '__main__':
    main()
