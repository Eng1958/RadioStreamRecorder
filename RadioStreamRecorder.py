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
import sys
import os
import subprocess
from time import gmtime, strftime

import rsrhelper

def radio_stream_recording(args):
    """
        run recording of stream with a little help from cvlc
    """

    print("Radio Stream-Recorder")

    streamurl = ''
    cvlclog = 'cvlc.log'

    rsrhelper.print_args(args)

    settings = rsrhelper.read_settings()

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

    rsrhelper.remove_log(cvlclog)

    # build command to record a stream with cvlc. Some informatione
    # during recording will be logged in cvlc.log
    cmd = ['/usr/bin/cvlc']
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
    except subprocess.TimeoutExpired as e:
        print('recording is finished')
        print(e)

    icy_tags = rsrhelper.icy_tag(cvlclog)
    rsrhelper.recording_log(log_file, args.station, args.album, args.artist,
                            icy_tags)

    rsrhelper.set_mp3_tags(mp3_file, args.artist, args.album, recording_date,
                           streamurl, icy_tags)

    rsrhelper.show_mp3_tags(mp3_file)


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
    parser_record.set_defaults(func=radio_stream_recording)

    parser_list = subparsers.add_parser('list', help='List all known stations')
    parser_list.set_defaults(func=rsrhelper.list_stations)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
