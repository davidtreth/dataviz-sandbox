#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import datetime
import glob

filelists = glob.glob("fileList*txt")

outfiledir = "concat"

for filelist in filelists:
    outfilename = os.path.join(outfiledir, "duration_"+filelist)
    outfile = open(outfilename, mode='w')
    filelist2 = open(filelist, mode='r')
    lines = filelist2.readlines()
    filenames = [l.split("'")[1] for l in lines]
    areanames = [a.split(".mp4")[0].replace("_", " ") for a in filenames]
    starttime = datetime.timedelta(seconds=0)
    for a, f in zip(areanames, filenames):
        print(f"{a}: {starttime}")
        outfile.write(f"{a}: {starttime}\n")
        exiftoolcmd = f"exiftool -Duration {f}"
        exif = subprocess.run(exiftoolcmd, shell=True, capture_output=True)
        duration = str(exif.stdout)
        duration = duration.split(":")
        h, m, s = duration[-3:]
        h = h.strip()
        h = int(h)
        m = int(m)
        s = s[:2]
        s = int(s)
        delta = datetime.timedelta(seconds=s, minutes=m, hours=h)
        # print(a, delta)
        starttime += delta
    outfile.close()
    

