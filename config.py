#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys

class Config:
    line_style = '0'
    line_size = '0'
    opacity = '0.5'
    xt_state = '1'
    xt_error = '0.005'
    indir = ''
    outdir = ''
    outext = '.geojson'

    def __init__(self):
        self.__dotfile = os.path.join(os.path.expanduser('~'), '.gpx2geojson')
        self.line_style = self.__class__.line_style
        self.line_size = self.__class__.line_size
        self.opacity = self.__class__.opacity
        self.xt_state = self.__class__.xt_state
        self.xt_error = self.__class__.xt_error
        self.indir = self.__class__.indir
        self.outdir = self.__class__.outdir
        self.outext = self.__class__.outext

    def load(self):
        with open(self.__dotfile, 'r') as f:
            for row in f:
                [key, value] = row.strip().split('=')
                if key.isupper():
                    continue
                if hasattr(self, key):
                    setattr(self, key, value)

    def save(self):
        with open(self.__dotfile, 'w') as f:
            for key in vars(self).keys():
                if key.isupper():
                    continue
                value = getattr(self, key)
                f.write(key + '=' + value + '\n')

    def list(self):
        for key in vars(self).keys():
            if key.isupper():
                continue
            value = getattr(self, key)
            print(key + '=' + value)


    def usage(self):
        help = '''\
        Usage: gpx2geojson gpxfiles...
        Options:
            -a opacity      between 0 and 1
            -s line_style   0: use value specified in GPX file
            -w line_size    0: use value specified in GPX file
            -x xt_error     decimate track points. set cross-track error [km]
            -f format       output format (gpx, kml, geojson)
            -h              print this message.\
        '''
        print(help, file=sys.stderr)

    def parse(self, argv):
        try:
            opts, args = getopt.getopt(argv, 'a:s:w:x:f:h')
        except getopt.GetoptError as err:
            print(err)
            self.__class__.usage()
            sys.exit(1)
        for o, a in opts:
            if o == '-a':
                cf.opacity = a
            elif o == '-s':
                cf.line_style = a
            elif o == '-w':
                cf.line_size = a
            elif o == '-x':
                cf.xt_error = a
            elif o == '-f':
                cf.outext = '.' + a
            else:
                self.usage()
                sys.exit(1)
        #
        return args

cf = Config()  # type: Config # 初期化

def main():
    global cf
    cf.load()
    args = cf.parse(sys.argv[1:])
    cf.list()
    print(args)
    cf.save()

if __name__ == '__main__':
    main()

# __END__
