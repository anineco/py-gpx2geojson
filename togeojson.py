#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import extensions
import iconlut
from const import GPX

def get_point_feature(pt):
    """get point feature from 'wpt' or 'rtept'."""
    icon = extensions.icon(pt)
    feature = {
        'type': 'Feature',
        'properties': {
            'name': pt.find(GPX + 'name').text,
            '_iconUrl': iconlut.url(icon),
            '_iconSize': iconlut.size(icon),
            '_iconAnchor': iconlut.anchor(icon)
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [float(pt.get('lon')), float(pt.get('lat'))]
        }
    }
    if cmt := pt.find(GPX + 'cmt').text:
        for s in cmt.split(','):
            key, value = s.strip().split('=')
            if key:
                feature['properties'][key] = value
    return feature

# kashmir3d:line_style: dashArray
dash = {
    '11': [4,2],        # short dash
    '12': [6,2],        # long dash
    '13': [1,2],        # dot
    '14': [1,2,5,2],    # dot-dash (one dot chain)
    '15': [1,2,1,2,6,2] # dot-dot-dash (two-dot chain)
}

def get_linestring_properties(t, line_size, line_style, opacity):
    """get linestring properties from 'rte' or 'trk'."""
    m = re.match(r'(..)(..)(..)', extensions.line_color(t))
    c = '#' + m.group(3) + m.group(2) + m.group(1)
    w = int(line_size if line_size != '0' else extensions.line_size(t))
    properties = {
        'name': t.find(GPX + 'name').text,
        '_color': c,
        '_weight': w,
        '_opacity': float(opacity)
    }
    s = line_style if line_style != '0' else extensions.line_style(t)
    if s in dash:
        properties['_dashArray'] = ','.join(map(lambda x: str(w * x), dash[s]))
    return properties

def get_linestring_feature(segment, tag, properties):
    """get linestring feature from 'rte' or 'trkseg'."""
    feature = {
        'type': 'Feature',
        'properties': properties,
        'geometry': {
            'type': 'LineString',
            'coordinates': []
        }
    }
    for pt in segment.findall(GPX + tag):
        lon = float(pt.get('lon'))
        lat = float(pt.get('lat'))
        feature['geometry']['coordinates'].append([lon, lat])
    return feature

def togeojson(tree, line_size, line_style, opacity):
    """convert element tree of gpx to geojson."""
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    root = tree.getroot()

    # Waypoint
    for wpt in root.findall(GPX + 'wpt'):
        feature = get_point_feature(wpt)
        geojson['features'].append(feature)

    # Route
    for rte in root.findall(GPX + 'rte'):
        for rtept in rte.findall(GPX + 'rtept'):
            if extensions.icon(rtept) == '903001':
                continue
            feature = get_point_feature(rtept)
            geojson['features'].append(feature)

        properties = get_linestring_properties(rte, line_size, line_style, opacity)
        feature = get_linestring_feature(rte, 'rtept', properties)
        geojson['features'].append(feature)

    # Track
    for trk in root.findall(GPX + 'trk'):
        properties = get_linestring_properties(trk, line_size, line_style, opacity)
        for trkseg in trk.findall(GPX + 'trkseg'):
            feature = get_linestring_feature(trkseg, 'trkpt', properties)
            geojson['features'].append(feature)

    return geojson

# __END__
