#!/usr/bin/env python3
# vim: number tabstop=4 noexpandtab shiftwidth=4 softtabstop=4 autoindent

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

"""

import argparse
import configparser
import sys
import os
from subprocess import call
from subprocess import run
import subprocess
from time import gmtime, strftime
import eyed3

def check_duration(value):
	"""
		value:	Duration of recording time in minutes. the duration must be a 
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

def radio_stream_recording(args):
	"""
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
		recording_directory = settings['GLOBAL']['target_dir']
		if args.verbose:
			print(recording_directory)
	except KeyError:
		print('Unkown Recording directoy: ')
		sys.exit()

	File = '%s-%s-(%s - %s)' % (args.station, \
				strftime("%Y-%m-%d_%H-%M", gmtime()),
				args.artist, args.album)
	MP3File = File + '.mp3'
	LogFile = File + '.log'
	if args.verbose:
		print(MP3File)
		print(LogFile)

	remove_log(cvlclog)

	# build command to record a stream with cvlc
	cmd = ['/usr/bin/cvlc']
	cmd += ['--verbose=2']
	cmd += ['--extraintf=http:logger']
	cmd += ['--file-logging']
	cmd += ['--logfile=%s' % (cvlclog)]
	cmd += [streamurl]
	cmd += ['--sout=#std{access=file,mux=raw,dst=%s' % (MP3File)]
	print(cmd)

	# Uebergabe des Kommandos und der Parameter muss als Liste erfolgen
	try:
	## call(cmd, shell=False, timeout=20)
		### call(cmd, shell=False, timeout=(args.duration * 60))
		t = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT, timeout=(args.duration * 60))
	except subprocess.TimeoutExpired as e:
		print('recording is finished')
		print(e)

	Icy_tags = Icy_Tags(cvlclog)
	recording_log(LogFile, args.station, args.album, args.artist, Icy_tags)

	audiofile = eyed3.load(MP3File)
	if audiofile.tag is None:
		audiofile.initTag()
		## audiofile.tag.save()

	audiofile.tag.artist = args.artist
	audiofile.tag.album = args.album
	audiofile.tag.album_artist = args.artist
	audiofile.tag.title = args.album + ' - ' + args.artist
	audiofile.tag.track_num = 1
	audiofile.tag.year = 2017

	audiofile.tag.save()

		

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
	""" list all radio stations in settings.ini
	"""

	settings = read_settings()
	for key in sorted(settings['STATIONS']):
		print(key)

def	Icy_Tags(log):
	""" Serch for Icy-Tags in Log-File
		return list with Icy-Tags
	"""
	Icy_list = []

	print(log)
	with open(log) as f:
		content = f.readlines()
		for line in content:
			if 'Icy' in line:
				Icy_list.append(line.rstrip('\n'))
				print(line, end='')
			if 'icy' in line:
				Icy_list.append(line.rstrip('\n'))
				print(line, end='')
		f.close()
		return Icy_list

def main():


	# -----------------------------------------------------------------             
	# get options                                                                   
	#   -r --radiostation       Shortcut of radio station                           
	#   -l --recordinglength    Lenght of recording (in minutes)                    
	#   --album                  set ID-Tag album                                   
	#   --artist                 set ID-Tag artist                                  
	# -----------------------------------------------------------------             

	parser = argparse.ArgumentParser(description='This program records internet radio streams. '
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
