#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from app import App
from config import cf
from gpx2geojson_cli import Gpx2GeoJSON

def main():
    global cf
    cf.load()
    if len(sys.argv) > 1:
        args = cf.parse(sys.argv[1:])
#       cf.list()
        Gpx2GeoJSON.convert(args)
    else:
        app = App()

if __name__ == '__main__':
    main()

# __END__
