#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const import GPX, KASHMIR3D

def icon(t):
    e = t.find(GPX + 'extensions')
    return e.find(KASHMIR3D + 'icon').text


def line_color(t):
    e = t.find(GPX + 'extensions')
    return e.find(KASHMIR3D + 'line_color').text


def line_size(t):
    e = t.find(GPX + 'extensions')
    return e.find(KASHMIR3D + 'line_size').text


def line_style(t):
    e = t.find(GPX + 'extensions')
    return e.find(KASHMIR3D + 'line_style').text

# __END__
