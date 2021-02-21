#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class IconLut:
    def __init__(self):
        pass

    @classmethod
    def url(cls, icon):
        return f'https://map.jpn.org/icon/{icon}.png'

    @classmethod
    def size(cls, icon):
        return [24, 24]

    @classmethod
    def anchor(cls, icon):
        return [12, 12]

# __END__
