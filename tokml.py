#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET

from config import cf
from const import Const
from extensions import Extensions
from iconlut import IconLut

class ToKML:
    using = {}
    count = 0

    def __init__(self):
        pass

    @classmethod
    def get_point_placemark(cls, pt): # wpt or rtept
        icon = Extensions.icon(pt)
        id = 'N' + icon
        cls.using[id] = IconLut.url(icon)
        p = ET.Element('Placemark')
        ET.SubElement(p, 'name').text = pt.find(Const.GPX + 'name').text
        if cmt := pt.find(Const.GPX + 'cmt').text:
            html = ''
            for s in cmt.split(','):
                [key, value] = s.strip().split('=')
                if key:
                    html += f'<tr><td>{key}</td><td>{value}</td></tr>'
            if html:
                html = '<table>' + html + '</table>'
                ET.SubElement(p, 'description').text = html

        ET.SubElement(p, 'styleUrl').text = '#' + id
        lon = float(pt.get('lon'))
        lat = float(pt.get('lat'))
        ET.SubElement(ET.SubElement(p, 'Point'), 'coordinates').text\
                = '{:.6f},{:.6f}'.format(lon, lat)
        return p

    @classmethod
    def get_linestring_style(cls, t): # trk or rte
        cls.count += 1
        s = ET.Element('Style', attrib={'id': 'id{:05d}'.format(cls.count)})
        l = ET.SubElement(s, 'LineStyle')
        a = int(float(cf.opacity) * 255)
        w = cf.line_size if cf.line_size != '0' else Extensions.line_size(t)
        ET.SubElement(l, 'color').text\
                = '{:02x}'.format(a) + Extensions.line_color(t)
        ET.SubElement(l, 'width').text = w
        return s

    @classmethod
    def get_linestring_placemark(cls, segment, tag, style, name):
        p = ET.Element('Placemark')
        ET.SubElement(p, 'name').text = name
        ET.SubElement(p, 'styleUrl').text = '#' + style.get('id')
        m = map(
            lambda x: '{:.6f},{:.6f}'.format(
                float(x.get('lon')),
                float(x.get('lat'))
            ),
            segment.findall(Const.GPX + tag)
        )
        ET.SubElement(ET.SubElement(p, 'LineString'), 'coordinates').text\
                = "\n".join(list(m))
        return p

    @classmethod
    def convert(cls, tree):
        root = tree.getroot()
        kml = ET.Element('kml',
            attrib={'xmlns': 'http://www.opengis.net/kml/2.2'}
        )
        doc = ET.SubElement(kml, 'Document')
        ET.SubElement(doc, 'name').text = Const.TITLE

        # Waypoint
        for wpt in root.findall(Const.GPX + 'wpt'):
            p = cls.get_point_placemark(wpt)
            doc.append(p)

        # Route
        for rte in root.findall(Const.GPX + 'rte'):
            for rtept in rte.findall(Const.GPX + 'rtept'):
                if Extensions.icon(rtept) != '903001':
                    p = cls.get_point_placemark(rtept)
                    doc.append(p)
            #
            n = rte.find(Const.GPX + 'name').text
            s = cls.get_linestring_style(rte)
            p = cls.get_linestring_placemark(rte, 'rtept', s, n)
            doc.append(s)
            doc.append(p)

        for id in cls.using.keys():
            url = cls.using[id]
            s = ET.Element('Style', attrib={'id': id})
            i = ET.SubElement(s, 'IconStyle')
            ET.SubElement(i, 'scale').text = '1'
            ET.SubElement(ET.SubElement(i, 'Icon'), 'href').text = url
            doc.append(s)

        # Track
        for trk in root.findall(Const.GPX + 'trk'):
            n = trk.find(Const.GPX + 'name').text
            s = cls.get_linestring_style(trk)
            doc.append(s)
            for trkseg in trk.findall(Const.GPX + 'trkseg'):
                p = cls.get_linestring_placemark(trkseg, 'trkpt', s, n)
                doc.append(p)

        return ET.ElementTree(kml)

# __END__
