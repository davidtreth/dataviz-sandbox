#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import glob

outdir = "endframes"

videos = glob.glob("*mp4")

for vfile in videos:
    outfile = vfile.replace(".mp4", ".png")
    outfile = os.path.join(outdir, outfile)
    ffmpeg_cmd = f"ffmpeg -sseof -3 -i {vfile} -frames:v 1 -q:v 1 {outfile}"
    subprocess.call(ffmpeg_cmd, shell=True)
