#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from getopt import GetoptError, getopt

class Config:
    """load, save configuration parameters and parse them from command line.

    Attributes:
        line_style (str): line style.
        line_size (str): line size (width) of track and route.
        opacity (str): opacity of line.
        xt_state (str): '0' or '1'. switch track point decimation.
        xt_error (str): allowable error of cross track decimation. unit [km].
        indir (str): initial directory of input files.
        outdir (str): initial directory of output file.
        outext (str): extension of output file. '.geojson', '.kml' or '.gpx'
    """
    def __init__(self):
        self.__dotfile = os.path.join(os.path.expanduser('~'), '.gpx2geojson')
        self.line_style = '0'
        self.line_size = '0'
        self.opacity = '0.5'
        self.xt_state = '0'
        self.xt_error = '0.005'
        self.indir = ''
        self.outdir = ''
        self.outext = '.geojson'
        # for backward compatibility
        self.title = 'GPS Track Log'

    def load(self):
        """load configuration parameters from dot-file."""
        try:
            with open(self.__dotfile, 'r') as f:
                for row in f:
                    key, value = row.strip().split('=')
                    if not key.startswith('_') and hasattr(self, key):
                        setattr(self, key, value)
        except Exception as e:
            pass

    def save(self):
        """save configuration parameters to dot-file."""
        with open(self.__dotfile, 'w') as f:
            for key, value in vars(self).items():
                if not key.startswith('_'):
                    f.write(key + '=' + value + '\n')

    def list(self):
        """list configuration parameters to stdout."""
        for key, value in vars(self).items():
            if not key.startswith('_'):
                print(key + '=' + value)

    @staticmethod
    def usage():
        """display help message to stderr."""
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
        """parse command line options."""
        try:
            opts, args = getopt(argv, 'a:s:w:x:f:h')
        except GetoptError as e:
            print(e, file=sys.stderr)
            self.usage()
            sys.exit(1)

        self.xt_state = '0'
        for opt, arg in opts:
            if opt == '-a':
                self.opacity = arg
            elif opt == '-s':
                self.line_style = arg
            elif opt == '-w':
                self.line_size = arg
            elif opt == '-x':
                self.xt_state = '1'
                self.xt_error = arg
            elif opt == '-f':
                self.outext = '.' + arg
            else:
                self.usage()
                sys.exit(1)
        return args

def main():
    """for debug only."""
    cf = Config()
    cf.load()
    cf.list()
    args = cf.parse(sys.argv[1:])
    print(args)
    cf.list()
    cf.save()

if __name__ == '__main__':
    main()

# __END__
