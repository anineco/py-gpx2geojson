#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gpx2geojson: GPX to GeoJSON / KML converter.

    GUI application for merging kashmir3d-generated multiple
    GPX files into a single file, decimating track points,
    and converting into a GeoJSON or KML file,
    both of which are specified in
    https://maps.gsi.go.jp/development/sakuzu_siyou.html.
    Originally written in Perl, and rewritten in Python3.
"""

import sys
import tkinter as tk

from app import App
from config import Config
from gpx2geojson_cli import convert

def main():
    if len(sys.argv) > 1:
        cf = Config()
        args = cf.parse(sys.argv[1:])
        convert(args, None,
                xt_state=cf.xt_state,
                xt_error=cf.xt_error,
                outext=cf.outext,
                line_size=cf.line_size,
                line_style=cf.line_style,
                opacity=cf.opacity
        )
    else:
        root = tk.Tk()
        app = App(master=root)
        app.mainloop()

if __name__ == '__main__':
    main()

# __END__
