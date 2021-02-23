#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from getopt import GetoptError, getopt


class Config:

    def __init__(self):
        self.__dotfile = os.path.join(os.path.expanduser('~'), '.gpx2geojson')
        self.line_style = '0'
        self.line_size = '0'
        self.opacity = '0.5'
        self.xt_state = 'normal' # or 'disabled'
        self.xt_error = '0.005'
        self.indir = ''
        self.outdir = ''
        self.outext = '.geojson'

    def load(self):
        """ load configuration parameters from ~/.gpx2geojson """
        with open(self.__dotfile, 'r') as f:
            for row in f:
                key, value = row.strip().split('=')
                if not key.startswith('_') and not hasattr(self, key):
                    setattr(self, key, value)

    def save(self):
        """ save configuration parameters to ~/.gpx2geojson """
        with open(self.__dotfile, 'w') as f:
            for key, value in vars(self).items():
                if not key.startswith('_'):
                    f.write(key + '=' + value + '\n')

    def list(self):
        """ list configuration parameters to stdout """
        for key, value in vars(self).items():
            if not key.startswith('_'):
                print(key + '=' + value)

    @staticmethod
    def usage():
        """ display help message. """
        help = """\
Usage: gpx2geojson gpxfiles...
Options:
    -a opacity      between 0 and 1
    -s line_style   0: use value specified in GPX file
    -w line_size    0: use value specified in GPX file
    -x xt_error     decimate track points. set cross-track error [km]
    -f format       output format (gpx, kml, geojson)
    -h              print this message.\
"""
        print(help, file=sys.stderr)

    def parse(self, argv):
        """ parse command line arguments and options. """
        try:
            opts, args = getopt(argv, 'a:s:w:x:f:h')
        except GetoptError as e:
            print(e, file=sys.stderr)
            self.usage()
            sys.exit(1)
        for opt, arg in opts:
            if opt == '-a':
                self.opacity = arg
            elif opt == '-s':
                self.line_style = arg
            elif opt == '-w':
                self.line_size = arg
            elif opt == '-x':
                self.xt_error = arg
            elif opt == '-f':
                self.outext = '.' + arg
            else:
                self.usage()
                sys.exit(1)
        return args

def main():
    """ for debug only. """
    cf = Config()
    cf.load()
    args = cf.parse(sys.argv[1:])
    cf.list()
    print(args)
    cf.save()

if __name__ == '__main__':
    main()

# __END__
