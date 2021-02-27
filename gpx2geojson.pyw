#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gpx2geojson: GPX to GeoJSON / KML converter.

    GUI application for merging kashmir3d-generated multiple
    GPX files into a single file, decimating track points,
    and converting into a GeoJSON or KML file,
    both of which are specified in
    https://maps.gsi.go.jp/development/sakuzu_siyou.html.
    Originally written in Perl, and rewritten in Python3.
"""

import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

from config import Config
from gpx2geojson_cli import convert

VERSION = '2.0'

class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(padding=5)
        self.pack()

        self.cf = Config()
        self.cf.load()

        self.line_style = StringVar(value=self.cf.line_style)
        self.line_size = StringVar(value=self.cf.line_size)
        self.opacity = StringVar(value=self.cf.opacity)
        self.xt_state = StringVar(value=self.cf.xt_state)
        self.xt_error = StringVar(value=self.cf.xt_error)
        self.outext = StringVar(value=self.cf.outext)
        self.outfile = StringVar(value='')
        self.n_point = StringVar(value='')

        self.gpxfiles = None
        self.xt = None
        self.create_widgets()

    def save_config(self):
        """save configuration parameters."""
        self.cf.line_style = self.line_style.get()
        self.cf.line_size = self.line_size.get()
        self.cf.opacity = self.opacity.get()
        self.cf.xt_state = self.xt_state.get()
        self.cf.xt_error = self.xt_error.get()
        self.cf.outext = self.outext.get()
        self.cf.save()

    def create_widgets(self):
        """create gui widgets."""
        l = Label(self, text='GPX→GeoJSONコンバータ Ver.'+VERSION)
        l.grid(row=0, column=0, columnspan=5)

        l = Label(self, text='GPXファイル')
        l.grid(row=1, column=0, sticky='e')

        l = Label(self, text='出力形式')
        l.grid(row=4, column=0, sticky='e')

        l = Label(self, text='出力ファイル')
        l.grid(row=5, column=0, sticky='e')

        l = Label(self, text='変換設定', anchor='center')
        l.grid(row=6, column=1, sticky='ew')

        l = Label(self, text='線の透過率')
        l.grid(row=7, column=0, sticky='e')

        l = Label(self, text='線種')
        l.grid(row=8, column=0, sticky='e')

        l = Label(self, text='線幅')
        l.grid(row=9, column=0, sticky='e')

        l = Label(self, text='許容誤差[km]')
        l.grid(row=7, column=2, sticky='e')

        l = Label(self, text='変換結果情報', anchor='center')
        l.grid(row=8, column=3, sticky='ew')

        l = Label(self, text='軌跡点数')
        l.grid(row=9, column=2, sticky='e')

        # GPXファイル
        f = Frame(self)
        f.grid(row=1, column=1, rowspan=3, columnspan=3, sticky='nsew')

        l = Listbox(f, width=75, height=3, selectmode='single')
        b = Scrollbar(f, orient='vertical')
        l['yscrollcommand'] = b.set
        b['command'] = l.yview
        l.pack(side='left', fill='y')
        b.pack(side='right', fill='y')

        self.gpxfiles = l

        # 追加 除外 クリア
        b = Button(self, text='←追加')
        b['command'] = self.append_to_list
        b.grid(row=1, column=4, sticky='ew')

        b = Button(self, text='除外')
        b['command'] = self.remove_from_list
        b.grid(row=2, column=4, sticky='ew')

        b = Button(self, text='クリア')
        b['command'] = self.clear_list
        b.grid(row=3, column=4, sticky='ew')

        # 出力形式
        f = Frame(self, borderwidth=1, relief='sunken')
        f.grid(row=4, column=1, sticky='nsew')
        formats = [['GPX', '.gpx'], ['KML', '.kml'], ['GeoJSON', '.geojson']]
        for key, value in formats:
            b = Radiobutton(f, text=key, value=value)
            b['variable'] = self.outext
            b.pack(side='left')

        # 出力ファイル
        e = Entry(self)
        e['textvariable'] = self.outfile
        e.grid(row=5, column=1, columnspan=3, sticky='nsew')

        b = Button(self, text='選択')
        b['command'] = self.select_savefile
        b.grid(row=5, column=4, sticky='ew')

        # 線の透過率
        b = Spinbox(self, format='%3.1f', from_=0.0, to=1.0, increment=0.1)
        b['textvariable'] =self.opacity
        b.grid(row=7, column=1, sticky='nsew')

        # 線種
        f = Frame(self, borderwidth=1, relief='sunken')
        f.grid(row=8, column=1, sticky='nsew')
        styles = [['GPX', '0'], ['実線', '1'], ['破線', '11'], ['点線', '13']]
        for key, value in styles:
            b = Radiobutton(f, text=key, value=value)
            b['variable'] = self.line_style
            b.pack(side='left')

        # 線幅
        f = Frame(self, borderwidth=1, relief='sunken')
        f.grid(row=9, column=1, sticky='nsew')
        sizes =  [['GPX', '0'], [' 1pt', '1'], [' 3pt',  '3'], [' 5pt',  '5']]
        for key, value in sizes:
            b = Radiobutton(f, text=key, value=value)
            b['variable'] = self.line_size
            b.pack(side='left')

        # 許容誤差
        b = Spinbox(self, format='%5.3f', from_=0.001, to=9.999, increment=0.001)
        b['textvariable'] = self.xt_error
        b.grid(row=7, column=3, sticky='nsew')
        self.xt = b

        b = Checkbutton(self, text='軌跡を間引く', onvalue='1', offvalue='0')
        b['variable'] = self.xt_state
        b['command'] = self.set_xt
        b.grid(row=6, column=3, sticky='w')
        self.set_xt()

        # 軌跡点数
        e = Entry(self, state='readonly')
        e['textvariable'] = self.n_point
        e.grid(row=9, column=3, sticky='ew')

        # 変換
        b = Button(self, text='変換')
        b['command'] = self.conv
        b.grid(row=10, column=1)

        # 終了
        b = Button(self, text='終了')
        b['command'] = self.quit
        b.grid(row=10, column=4)

    def append_to_list(self):
        ret = filedialog.askopenfilenames(
            filetypes=[('GPXファイル', '*.gpx'), ('', '*')],
            initialdir=self.cf.indir
        )
        for path in ret:
            self.gpxfiles.insert('end', path)
            self.cf.indir = os.path.dirname(path)

    def remove_from_list(self):
        i = self.gpxfiles.curselection()
        self.gpxfiles.delete(i)

    def clear_list(self):
        self.gpxfiles.delete(0, 'end')

    def select_savefile(self):
        ext = self.outext.get()
        nam = { '.geojson': 'GeoJSON', '.kml': 'KML', '.gpx': 'GPX' }
        ret = filedialog.asksaveasfilename(
            filetypes=[(nam[ext] + 'ファイル', '*' + ext), ('', '*')],
            initialdir=self.cf.outdir,
            initialfile='routemap'
        )
        if ret:
            self.outfile.set(ret)

    def set_xt(self):
        self.xt.configure(state='normal' if self.xt_state.get() != '0' else 'disabled')

    def conv(self):
        args = list(self.gpxfiles.get(0, 'end'))
        if len(args) == 0:
            messagebox.showwarning(title='警告', message='GPXファイルが未設定')
            return
        outfile = self.outfile.get()
        if not outfile:
            messagebox.showwarning(title='警告', message='出力ファイルが未設定')
            return
        n_point = convert(args, outfile,
                xt_state=self.xt_state.get(),
                xt_error=self.xt_error.get(),
                outext=self.outext.get(),
                line_size=self.line_size.get(),
                line_style=self.line_style.get(),
                opacity=self.opacity.get()
        )
        if n_point < 0:
            messagebox.showerror(title='エラー', message='変換に失敗しました')
            return
        self.n_point.set(str(n_point))
        self.master.update()
        self.cf.outdir = os.path.dirname(outfile)
        messagebox.showinfo(title='成功', message='変換結果を'+outfile+'に出力しました')

    def quit(self):
        self.save_config()
        self.master.destroy()

def main():
    root = Tk()
    root.title('GPX2GeoJSON')
    root.resizable(False, False)
    app = App(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()

# __END__
