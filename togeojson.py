#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from config import Config, cf
from const import Const
from extensions import Extensions
from iconlut import IconLut

class ToGeoJSON:
    def __init__(self):
        pass

    @classmethod
    def get_point_feature(cls, pt): # wpt or rtept
        icon = Extensions.icon(pt)
        feature = {
            'type': 'Feature',
            'properties': {
                'name': pt.find(Const.GPX + 'name').text,
                '_iconUrl': IconLut.url(icon),
                '_iconSize': IconLut.size(icon),
                '_iconAnchor': IconLut.anchor(icon)
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [ float(pt.get('lon')), float(pt.get('lat')) ]
            }
        }
        if cmt := pt.find(Const.GPX + 'cmt').text:
            for s in cmt.split(','):
                [key, value] = s.strip().split('=')
                if key:
                    feature['properties'][key] = value
        return feature

    @classmethod
    def get_linestring_properties(cls, t): # trk or rte
        global cf
        # kashmir3d:line_style: dashArray
        dash = {
            '11': [4,2],        # short dash
            '12': [6,2],        # long dash
            '13': [1,2],        # dot
            '14': [1,2,5,2],    # dot-dash (one dot chain)
            '15': [1,2,1,2,6,2] # dot-dot-dash (two-dot chain)
        }
        m = re.match(r'(..)(..)(..)', Extensions.line_color(t))
        c = '#' + m.group(3) + m.group(2) + m.group(1)
        if (w := int(cf.line_size)) == 0:
            w = int(Extensions.line_size(t))
        properties = {
            'name': t.find(Const.GPX + 'name').text,
            '_color': c,
            '_weight': w,
            '_opacity': float(cf.opacity)
        }
        if (s := cf.line_style) in dash or (s := Extensions.line_style(t)) in dash:
            properties['_dashArray'] = list(map(lambda x: w * x, dash[s]))
        return properties

    @classmethod
    def get_linestring_feature(cls, segment, tag, properties):
        feature = {
            'type': 'Feature',
            'properties': properties,
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            }
        }
        for pt in segment.findall(Const.GPX + tag):
            lon = float(pt.get('lon'))
            lat = float(pt.get('lat'))
            feature['geometry']['coordinates'].append([lon, lat])
        return feature

    @classmethod
    def convert(cls, tree):
        geojson = {
            'type': 'FeatureCollection',
            'features': []
        }
        root = tree.getroot()

        # Waypoint
        for wpt in root.findall(Const.GPX + 'wpt'):
            feature = cls.get_point_feature(wpt)
            geojson['features'].append(feature)

        # Route
        for rte in root.findall(Const.GPX + 'rte'):
            for rtept in rte.findall(Const.GPX + 'rtept'):
                if Extensions.icon(rtept) == '903001':
                    continue
                feature = cls.get_point_feature(rtept)
                geojson['features'].append(feature)

            properties = cls.get_linestring_properties(rte)
            feature = cls.get_linestring_feature(rte, 'rtept', properties)
            geojson['features'].append(feature)

        # Track
        for trk in root.findall(Const.GPX + 'trk'):
            properties = cls.get_linestring_properties(trk)
            for trkseg in trk.findall(Const.GPX + 'trkseg'):
                feature = cls.get_linestring_feature(trkseg, 'trkpt', properties)
                geojson['features'].append(feature)

        return geojson

# __END__
