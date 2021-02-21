#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const import Const

class Extensions:
    def __init__(self):
        pass

    @classmethod
    def icon(cls, t):
        assert(e := t.find(Const.GPX + 'extensions'))
        return e.find(Const.KASHMIR3D + 'icon').text

    @classmethod
    def line_color(cls, t):
        assert(e := t.find(Const.GPX + 'extensions'))
        return e.find(Const.KASHMIR3D + 'line_color').text

    @classmethod
    def line_size(cls, t):
        assert(e := t.find(Const.GPX + 'extensions'))
        return e.find(Const.KASHMIR3D + 'line_size').text

    @classmethod
    def line_style(cls, t):
        assert(e := t.find(Const.GPX + 'extensions'))
        return e.find(Const.KASHMIR3D + 'line_style').text

# __END__
