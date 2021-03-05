# py-gpx2geojson
This is a desktop GUI application for merging Kashmir3D-generated multiple GPX files into a single file, decimating track points, and converting into stylized GeoJSON or KML profile for web maps. Both of these formats are proposed by GSI (the Geospatial Information Authority of Japan) and can be viewed on [GSI maps](https://maps.gsi.go.jp/).

[Kashmir3D](http://www.kashmir3d.com/) is a Windows application with GPS data editing and map display functions, and favorably used among Japanese mountaineers.

Originally [gpx2geojson](https://github.com/anineco/gpx2geojson) was written in Perl, and rewritten in Python3.

See the [github-page](https://anineco.github.io/py-gpx2geojson/) (in Japanese) for more information on how to use the GUI.

## Operating conditions
To run gpx2geojson, you need [Python](https://www.python.org/), [lxml](https://lxml.de) and [GPSBabel](https://www.gpsbabel.org/). Gpx2geojson works on Windows, macOS, and Linux.

## How to install
Download the ZIP archive to an appropriate folder and extract it, or clone this repository.

## How to launch
**gpx2geojson.pyw** is the main program, which can be run as a CUI from a terminal application. If you run gpx2geojson.pyw with a option '-h', it will display a simple usage as follows:
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
If there are no command line arguments, GUI will be invoked. It can also be directly launched as a desktop application with GUI, as described below.

### Windows
Open the installed folder with **Explorer** and double-click the icon of gpx2geojson.pyw.

### macOS
Open the installed folder with **Finder**, right-click the icon of gpx2geojson.pyw and select **Python Launcher.app** from "Open with this application" menu.

### GNOME desktop environment on Linux
Run the following commands in a terminal application.
```
cp gnome/*.desktop ~/.local/share/applications/
cp gnome/python_94570.png ~/.local/share/icons/hicolor/256x256/apps/
```
Open the copied org.jpn.map.gpx2geojson.desktop by a editor, rewrite FULL_PATH_TO and save the file.
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
The icon image python_94570.png is copied from [Thousands of free icons](https://icon-icons.com/) and redistributed for convenience.
