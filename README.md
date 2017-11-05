RadioStreamRecorder
===================


## Synopsis

RadioStreamRecorder.py **records a stream** from a given internet radio url. You
can stop recordng after a given time and you can tag some important ID3 tags at the
recorded mp3 file.
Recording ist done with "a little help" from cvlc.
You can start recording with the Unix at-command (see man at)


## Code Example

usage: ./RadioStreamRecorder.py .... (TODO: describe arguments)


## Motivation

I haven't found a stream recorder under Linux (Ubuntu) 

## Installation

Install eyeD3 (See: [link to eyeD3!](http://https://eyed3.readthedocs.io/)
Install vlc  (See: [link to vlc!](http://vlc.com)

```
Give examples
```
## Configuration

See settings.ini

Example of settings.ini (~/.config/RadioStreamRecorder/settings.ini)

'''
[GLOBAL]
target_dir = ${HOME}/Musik/Recording

[STATIONS]
WDR3 = http://wdr-wdr3-live.icecast.wdr.de/wdr/wdr3/live/mp3/256/stream.mp3
DLF = http://www.deutschlandradio.de/streaming/dlf.m3u
DKULTUR = http://www.deutschlandradio.de/streaming/dkultur.m3u
'''

## API Reference

Depending on the size of the project, if it is small and simple enough 
the reference docs can be added to the README. For medium size to 
larger projects it is important to at least provide a link to where 
the API reference docs live.

## Tests

Describe and show how to run the tests with code examples.

```
Give examples

./RadioStreamRecorder.py record wdr3 1 --verbose --album "Jazz im WDR3"
--artist "Jaco Pastorius"
```

## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License

A short snippet describing the license (MIT, Apache, etc.)

## ToDo
- [x] Configure directory to save recorded mp3 file (Done)
- [ ] Read arguments from file with argument --file <filename>
- [ ] Create file with RadioStreamRecorder.py to run with at command (at -f
  file)
- [ ] Recording time as an argument (running at command)


