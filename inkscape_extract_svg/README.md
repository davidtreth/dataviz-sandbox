This is a Python script to extract the SVG icons as individual files
from the SVG files containing icon libraries in the
Inkscape Open Symbols library: https://github.com/Xaviju/inkscape-open-symbols

This makes them usable for example in QGIS

Set SVG paths in the Settings: https://docs.qgis.org/2.18/en/docs/user_manual/introduction/qgis_configuration.html#system-settings

The path to where Inkscape stores its SVG icon libraries is coded
in the variable inkscapesvgpath

on some systems it may be ~/.config/inkscape/symbols
For Windows, it would be in %APPDATA%\inkscape\symbols