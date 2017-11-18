#!/usr/bin/env python3
# vim: number tabstop=4 expandtab shiftwidth=4 softtabstop=4 autoindent


import subprocess

def split_mp3(mp3_file):
    """Splits the recorded mp3 file into smaller pieces. Using mp3splt

        mp3splt -a -f -t 15.0 -o "@n-@f" -f blabla.mp3

        -a Die Option -a kann zusätzlich zum Anpassen der Splitpunkte genutzt
            werden, um mit der automatischen Erkennung von stillen Passagen
            die Präzision noch zu verbessern
        -f Frame-Modus
        -t Mit diesem Schalter erstellt mp3splt einfach eine endliche Zahl
            an Einzelteilen, die alle die vorgegebene Dauer haben
        -o
    """
    splittime = 1.0

    cmd = ['/usr/bin/mp3splt']
    cmd += ['-a']
    cmd += ['-f']
    cmd += ['-q']   # quit mode
    cmd += ['-t']
    cmd += ['1.0']
    cmd += ['-o']
    cmd += ['@n-@f']
    cmd += ['%s' % (mp3_file)]

    print('mp3splt: Splittime %s' % (splittime))
    print(cmd)

    # Uebergabe des Kommandos und der Parameter muss als Liste erfolgen
    try:
        out = subprocess.check_output(cmd, shell=False,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
        print(out)
    except subprocess.CalledProcessError as error:
        print(error.output)

if __name__ == '__main__':
    split_mp3('/home/dieter/Musik/Recording/wdr3-2017-11-18_19-30-(Test-Artist - Test-Album).mp3')
