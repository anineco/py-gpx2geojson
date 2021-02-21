#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from config import cf
from const import Const
from togeojson import ToGeoJSON
from tokml import ToKML

ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')
ET.register_namespace('kashmir3d', 'http://www.kashmir3d.com/namespace/kashmir3d')
ET.register_namespace('kml', 'http://www.opengis.net/kml/2.2')

class Gpx2GeoJSON:
    def __init__(self):
        pass

    @classmethod
    def merge(cls, files):
        tree = ET.parse(files.pop(0))
        root = tree.getroot()
        for file in files:
            t = ET.parse(file)
            r = t.getroot()
            for tag in ['wpt', 'rte', 'trk']:
                for x in r.findall(Const.GPX + tag):
                    root.append(x)
        #
        return tree

    @classmethod
    def decimate_segment(cls, trkseg):
        global cf
        temp = tempfile.TemporaryDirectory()
        tmp1 = os.path.join(temp.name, 'tmp1.gpx')
        tmp2 = os.path.join(temp.name, 'tmp2.gpx')
        cmd = f'gpsbabel -t -i gpx -f {tmp1} -x simplify,error={cf.xt_error}k -o gpx,gpxver=1.1 -F {tmp2}'

        root = ET.Element('gpx')
        ET.SubElement(root, 'trk').append(trkseg)
        tree = ET.ElementTree(root)
        tree.write(tmp1)

        subprocess.run(cmd.split(), check=True)

        tree = ET.parse(tmp2)
        root = tree.getroot()
        trk = root.find(Const.GPX + 'trk')
        trkseg = trk.find(Const.GPX + 'trkseg')
        temp.cleanup()
        return trkseg

    @classmethod
    def decimate(cls, tree):
        root = tree.getroot()
        for trk in root.findall(Const.GPX + 'trk'):
            for i, child in enumerate(trk):
                if child.tag == Const.GPX + 'trkseg':
                    trk[i] = cls.decimate_segment(child)

    @classmethod
    def convert(cls, args):
        global cf
        tree = cls.merge(args)
        if cf.xt_state:
            cls.decimate(tree)
        if cf.outext == '.geojson':
            geojson = ToGeoJSON.convert(tree)
            with open('routemap' + cf.outext, 'w') as f:
                f.write(json.dumps(geojson, indent=2, ensure_ascii=False))
        else:
            xml = ToKML.convert(tree) if cf.outext == '.kml' else tree
            xml.write('routemap' + cf.outext, encoding='UTF-8')

def main():
    global cf
    cf.load()
    args = cf.parse(sys.argv[1:])
#   cf.list()
    Gpx2GeoJSON.convert(args)

if __name__ == '__main__':
    main()

# __END__
