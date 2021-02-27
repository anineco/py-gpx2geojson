# py-gpx2geojson
A GUI application for merging kashmir3d-generated multiple GPX files into a single file, decimating track points, and converting into a GeoJSON or KML file, both of which are specified in https://maps.gsi.go.jp/development/sakuzu_siyou.html. Originally [gpx2geojson](https://github.com/anineco/gpx2geojson) was written in Perl, and rewritten in Python3.

## Operating conditions
To run gpx2geojson, you need [Python](https://www.python.org/) and [GPSBabel](https://www.gpsbabel.org/). Both are open software and can be downloaded and used free of charge. Gpx2geojson works on Windows, macOS, and Linux.

## How to install
Download the ZIP archive to an appropriate folder and extract it, or clone this repositry.

## How to launch
**gpx2geojson.pyw** is the main program, which can be run as a CUI from a terminal application. If you run **gpx2geojson.pyw** with a option '-h', it will display a simple usage as follows:
```
Usage: gpx2geojson gpxfiles...
Options:
    -a opacity      between 0 and 1
    -s line_style   0: use value specified in GPX file
    -w line_size    0: use value specified in GPX file
    -x xt_error     decimate track points. set cross-track error [km]
    -f format       output format (gpx, kml, geojson)
    -h              print this message.
```
If there are no command line arguments, GUI will be invoked. It can also be launched as a desktop application with GUI, as described below.

### Windows
Open the installed folder with **Explorer** and double-click **gpx2geojson.pyw**.

### macOS
Open the installed folder with **Finder**, right-click **gpx2geojson.pyw** and select **Python Launcher.app** from "Open with this application" menu.

### Linux

#### GNOME desktop environment
Copy **org.jpn.map.gpx2geojson.desktop** and **tk.desktop** files under the gnome folder to ~/.local/share/applications/ and **python_94570.png** to ~/. local/share/icons/hicolor/256x256/apps/.

Edit the copied **org.jpn.map.gpx2geojson.desktop**, Rewrite FULL_PATH_TO and save it.
```
[Desktop Entry]
Type=Application
Version=1.1
Name=GPX2GeoJSON
Comment=GPX to GeoJSON Converter
Exec=/FULL_PATH_TO/gpx2geojson.pyw
Icon=python_94570
Terminal=false
```
Finally, invoke command execution by pressing Alt+F2 and execute 'r' command to restart the Gnome shell. Now you will see the 'GPX2GeoJSON' icon in the list of applications and you can click on it to launch it.

## Credit
The icon image **python_94570.png** is copied from [Thousands of free icons](https://icon-icons.com/) and redistributed for convenience.
