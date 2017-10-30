#!/usr/bin/env python3
# vim: number tabstop=4 expandtab shiftwidth=4 softtabstop=4 autoindent

import os
import configparser

parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
parser.read('config_data.ini')
## vars = os.environ
## print(os.environ)
## print("===================================================")
## print(vars)

print(parser)


print( parser.get('server_details', 'User', vars=os.environ))
print( parser.get('server_details', 'userName', vars=os.environ))

parser.read_file(open('config_data.ini'))

## print( parser.get('log_path', 'mntPath', vars=os.environ))
exit(0)
