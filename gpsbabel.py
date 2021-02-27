#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

def exe(*args):
    if os.name == 'posix':
        cmd = 'gpsbabel'
    else:
        assert(os.name == 'nt')
        cmd = 'C:\Program Files (x86)\GPSBabel\gpsbabel.exe'
    try:
        subprocess.run([cmd, *args], check=True)
    except subprocess.CalledProcessError:
        print('外部プログラム ' + cmd + ' の実行に失敗しました', file=sys.stderr)
        sys.exit(1)

def main():
    """for debug only."""
    exe('-V')

if __name__ == '__main__':
    main()

# __END__
