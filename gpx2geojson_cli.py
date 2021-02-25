#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET

import gpsbabel
from config import Config
from const import GPX
from togeojson import togeojson
from tokml import tokml

ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')
ET.register_namespace('kashmir3d', 'http://www.kashmir3d.com/namespace/kashmir3d')
ET.register_namespace('kml', 'http://www.opengis.net/kml/2.2')

def merge(files):
    """read gpx files and merge into one tree."""
    tree = ET.parse(files.pop(0))
    root = tree.getroot()
    for f in files:
        t = ET.parse(f)
        r = t.getroot()
        for tag in ['wpt', 'rte', 'trk']:
            for x in r.findall(GPX + tag):
                root.append(x)
    return tree

def decimate_segment(trkseg, xt_error):
    """decimate points in a track-segment using gpsbabel."""
    temp = tempfile.TemporaryDirectory()
    tmp1 = os.path.join(temp.name, 'tmp1.gpx')
    tmp2 = os.path.join(temp.name, 'tmp2.gpx')

    root = ET.Element('gpx')
    ET.SubElement(root, 'trk').append(trkseg)
    tree = ET.ElementTree(root)
    tree.write(tmp1)

    gpsbabel.exe(
        '-t', '-i', 'gpx', '-f', tmp1,
        '-x', 'simplify,error=' + xt_error,
        '-o', 'gpx,gpxver=1.1', '-F', tmp2
    )

    tree = ET.parse(tmp2)
    root = tree.getroot()
    trk = root.find(GPX + 'trk')
    trkseg = trk.find(GPX + 'trkseg')
    temp.cleanup()
    return trkseg

def decimate(tree, xt_error):
    """decimate track points in an element tree of gpx."""
    root = tree.getroot()
    for trk in root.findall(GPX + 'trk'):
        for i, child in enumerate(trk):
            if child.tag == GPX + 'trkseg':
                trk[i] = decimate_segment(child, xt_error)

def count_track_point(tree):
    """count track points in an element tree"""
    root = tree.getroot()
    n_point = 0
    for trk in root.findall(GPX + 'trk'):
        for trkseg in trk.findall(GPX + 'trkseg'):
            n_point += len(trkseg.findall(GPX + 'trkpt'))
    return n_point

def convert(args, outfile, xt_state=None, xt_error=None, outext=None,
        line_size=None, line_style=None, opacity=None):
    """convert multiple gpx into a geojson, kml or gpx and ouput."""
    tree = merge(args)
    if xt_state != '0':
        decimate(tree, xt_error)
    n_point = count_track_point(tree)
    if outext == '.geojson':
        geojson = togeojson(tree, line_size, line_style, opacity)
        s = json.dumps(geojson, indent=2, ensure_ascii=False) # serialize
        if outfile is None:
            print(s)
        else:
            with open(outfile, 'w') as f:
                f.write(s)
    else:
        if outext == '.kml':
            tree = tokml(tree, line_size, opacity)
        if outfile is None:
            print(ET.tostring(tree.getroot(), encoding='unicode'))
        else:
            tree.write(outfile, encoding='unicode')
    return n_point

def main():
    cf = Config()
    cf.load()
    args = cf.parse(sys.argv[1:])
    convert(args, None,
            xt_state=cf.xt_state,
            xt_error=cf.xt_error,
            outext=cf.outext,
            line_size=cf.line_size,
            line_style=cf.line_style,
            opacity=cf.opacity
    )

if __name__ == '__main__':
    main()

# __END__
