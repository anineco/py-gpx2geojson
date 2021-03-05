#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from lxml import etree as ET

import extensions
import iconlut
from const import GPX

using = None
seqno = None

def get_point_placemark(pt):
    """get point placemark from 'wpt' or 'rtept'."""
    global using
    icon = extensions.icon(pt)
    id = 'N' + icon
    using[id] = icon
    p = ET.Element('Placemark')
    ET.SubElement(p, 'name').text = pt.find(GPX + 'name').text
    if cmt := pt.find(GPX + 'cmt').text:
        html = ''
        for s in cmt.split(','):
            key, value = s.strip().split('=')
            if key:
                html += '<tr><td>' + key + '</td><td>' + value + '</td></tr>'
        if html:
            html = '<table>' + html + '</table>'
            ET.SubElement(p, 'description').text = ET.CDATA(html)

    ET.SubElement(p, 'styleUrl').text = '#' + id
    lon = float(pt.get('lon'))
    lat = float(pt.get('lat'))
    ET.SubElement(
        ET.SubElement(p, 'Point'), 'coordinates'
    ).text = '{:.6f},{:.6f}'.format(lon, lat)
    return p

def get_linestring_style(t, line_size, opacity):
    """get linestring style from 'trk' or 'rte'."""
    global seqno
    seqno += 1
    s = ET.Element('Style', attrib={'id':'id{:05d}'.format(seqno)})
    l = ET.SubElement(s, 'LineStyle')
    a = int(float(opacity) * 255)
    c = '{:02x}'.format(a) + extensions.line_color(t)
    w = line_size if line_size != '0' else extensions.line_size(t)
    ET.SubElement(l, 'color').text = c
    ET.SubElement(l, 'width').text = w
    return s

def get_linestring_placemark(segment, tag, style, name):
    """get linestring placemark from 'trkseg' or 'rte'."""
    p = ET.Element('Placemark')
    ET.SubElement(p, 'name').text = name
    ET.SubElement(p, 'styleUrl').text = '#' + style.get('id')
    l = ET.SubElement(p, 'LineString')
    m = map(
        lambda x: '{:.6f},{:.6f}'.format(
            float(x.get('lon')),
            float(x.get('lat'))
        ),
        segment.findall(GPX + tag)
    )
    ET.SubElement(l, 'coordinates').text = '\n'.join(list(m))
    return p

def tokml(tree, line_size, opacity):
    """convert element tree of gpx to kml."""
    global using, seqno
    using = {}
    seqno = 0

    root = tree.getroot()
    kml = ET.Element('kml', attrib={'xmlns':'http://www.opengis.net/kml/2.2'})
    doc = ET.SubElement(kml, 'Document')
    ET.SubElement(doc, 'name').text = 'GPS Track Log'

    # Waypoint
    for wpt in root.findall(GPX + 'wpt'):
        p = get_point_placemark(wpt)
        doc.append(p)

    # Route
    for rte in root.findall(GPX + 'rte'):
        for rtept in rte.findall(GPX + 'rtept'):
            if extensions.icon(rtept) != '903001':
                p = get_point_placemark(rtept)
                doc.append(p)

        name = rte.find(GPX + 'name').text
        s = get_linestring_style(rte, line_size, opacity)
        p = get_linestring_placemark(rte, 'rtept', s, name)
        doc.insert(1, s) # NOTE: next to 'GPS Track Log' element
        doc.append(p)

    for id, icon in using.items():
        s = ET.Element('Style', attrib={'id':id})
        i = ET.SubElement(s, 'IconStyle')
        ET.SubElement(i, 'scale').text = '1'
        ET.SubElement(ET.SubElement(i, 'Icon'), 'href').text = iconlut.url(icon)
        x, y = iconlut.anchor(icon)
        ET.SubElement(i, 'hotSpot', x=str(x), y=str(y), xunits='pixels', yunits='pixels')
        doc.insert(1, s)

    # Track
    for trk in root.findall(GPX + 'trk'):
        name = trk.find(GPX + 'name').text
        s = get_linestring_style(trk, line_size, opacity)
        doc.insert(1, s)
        for trkseg in trk.findall(GPX + 'trkseg'):
            p = get_linestring_placemark(trkseg, 'trkpt', s, name)
            doc.append(p)

    return ET.ElementTree(kml)

# __END__
