# -*- coding: utf-8 -*-
# David Trethewey
# this script uses Beautiful Soup to export individual files from the
# SVG icon libraries of the Inkscape Open Symbols Library
# https://github.com/Xaviju/inkscape-open-symbols
# to individual .svg files (one per icon)

from bs4 import BeautifulSoup
import glob
import os

# replace this if necessary on your system
# with the folder in which Inkscape stores the symbol libraries
inkscapesvgpath = "/usr/share/inkscape/symbols"

svgfiles = glob.glob(os.path.join(inkscapesvgpath, "*.svg"))

for svg in svgfiles:
    outdir = os.path.split(svg)[1][:-4]
    os.makedirs(outdir, exist_ok=True)
    os.chdir(outdir)
    print(svg)
    with open(svg, encoding='utf8') as f:
        raw = f.read()
        soup = BeautifulSoup(raw, "xml")
    svg_element = soup.find_all('svg')[0]
    svg_style = svg_element['style']
    svg_version = svg_element['version']
    try:
        metadata_elem = soup.find_all('metadata')[0]
    except:
        metadata_elem = None
    print("style = " + svg_style)
    for symbol in soup.find_all('symbol'):
        indivfilename = symbol['id']
        print(indivfilename)        
        outfilename = svg[:-4].replace(inkscapesvgpath+"/", '')+"_"+indivfilename+".svg"
        print(outfilename)
        outfile = open(outfilename, "w")
        outfile.write('<svg version="{v}" style="{s}">\n'.format(v=svg_version, s=svg_style))
        if metadata_elem:
            outfile.write(metadata_elem.prettify())
        outfile.write(symbol.prettify())
        outfile.write("</svg>")
        outfile.close()
    os.chdir("..")
    
