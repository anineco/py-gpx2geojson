#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

def exe(*args):
    if os.name == 'posix':
        cmd = 'gpsbabel'
        flags = 0
    else:
        assert(os.name == 'nt')
        cmd = 'C:\Program Files\GPSBabel\gpsbabel.exe'
        flags = subprocess.CREATE_NO_WINDOW
    try:
        subprocess.run([cmd, *args], check=True, creationflags=flags, capture_output=True)
    except subprocess.CalledProcessError:
        print('外部プログラム ' + cmd + ' の実行に失敗しました', file=sys.stderr)
        sys.exit(1)

def main():
    """for debug only."""
    exe('-V')

if __name__ == '__main__':
    main()

# __END__
