#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk

from config import Config, cf
from const import Const

class App:
    def __init__(self):
        cf = Config()
        cf.load()
        self.top = tk.Tk()
        self.top.title('GPX2GeoJSON')
        self.outfile = tk.StringVar()

        tk.Label(self.top, text=f'GPX→GeoJSONコンバータ Ver.{Const.VERSION}')\
                .grid(row=0, column=0, columnspan=5)
        tk.Label(self.top, text='GPXファイル')\
                .grid(row=1, column=0, sticky=tk.E)
        tk.Label(self.top, text='出力形式')\
                .grid(row=4, column=0, sticky=tk.E)
        tk.Label(self.top, text='出力ファイル')\
                .grid(row=5, column=0, sticky=tk.E)
        tk.Label(self.top, text='変換設定')\
                .grid(row=6, column=1, sticky=tk.EW)
        tk.Label(self.top, text='線の透過率')\
                .grid(row=7, column=0, sticky=tk.E)
        tk.Label(self.top, text='線種')\
                .grid(row=8, column=0, sticky=tk.E)
        tk.Label(self.top, text='線幅')\
                .grid(row=9, column=0, sticky=tk.E)
        tk.Label(self.top, text='許容誤差[km]')\
                .grid(row=7, column=2, sticky=tk.E)
        tk.Label(self.top, text='変換結果情報')\
                .grid(row=8, column=3, sticky=tk.W)
        tk.Label(self.top, text='軌跡点数')\
                .grid(row=8, column=2, sticky=tk.E)

        tk.Button(self.top, text='←追加')\
                .grid(row=1, column=4, sticky=tk.EW)
        tk.Button(self.top, text='除外')\
                .grid(row=2, column=4, sticky=tk.EW)
        tk.Button(self.top, text='クリア')\
                .grid(row=3, column=4, sticky=tk.EW)

        tk.Entry(self.top, textvariable=self.outfile)\
                .grid(row=5, column=1, columnspan=3, sticky=tk.NSEW)

        tk.Button(self.top, text='選択')\
                .grid(row=5, column=4, sticky=tk.EW)

        tk.Button(self.top, text='変換', command=lambda: self.top.destroy())\
                .grid(row=10, column=1)
        tk.Button(self.top, text='終了', command=lambda: self.top.destroy())\
                .grid(row=10, column=4)
        self.top.mainloop()

def main():
    app = App()

if __name__ == '__main__':
    main()

# __END__
