#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess



matplotlibdir = os.path.join("graphfiles","matplotlib")


png_pattern = f"*.png"

videofile = f"all_areas_endframes_matplotlib.mp4"
ffmpeg_cmd = (f"ffmpeg -pattern_type glob -r 0.25 -f image2 -s 1920x1440"
             f" -i '{png_pattern}' "
             f"-vcodec libx264 -crf 25 -pix_fmt yuv420p "
             f"{videofile}")
             
print(ffmpeg_cmd)
os.chdir(matplotlibdir)
subprocess.call(ffmpeg_cmd, shell=True)

