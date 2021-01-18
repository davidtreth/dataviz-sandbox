#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import corona_python_text_csv_api 

audiodir = "audiofiles"
graphdir = "graphfiles"
videodir = "videofiles"

def create_video(areaname, clearpng=True):
    png_pattern = f"{os.path.join(graphdir, areaname)}_%05d.png"
    audiofile = f"{os.path.join(audiodir, areaname.lower())}.mp3"
    videofile = f"{os.path.join(videodir, areaname)}.mp4"
    ffmpeg_cmd = (f"ffmpeg -r 8 -f image2 -s 1920x1080 -i {png_pattern}"
                 f" -i {audiofile} -vcodec libx264 -crf 25 -pix_fmt yuv420p"
                 f" -acodec copy {videofile}")
    subprocess.call(ffmpeg_cmd, shell=True)
    # remove png files from graphdir
    rmpng_cmd = f'rm -v {png_pattern.replace("%05d", "*")}'
    subprocess.call(rmpng_cmd, shell=True)
    
        
    

nations = corona_python_text_csv_api.cases_by_country
regions = corona_python_text_csv_api.cases_by_region
UTLAs = corona_python_text_csv_api.cases_by_UTLA

for areaname in nations:
    create_video(areaname)
for areaname in regions:
    create_video(areaname)
for areaname in UTLAs:
    create_video(areaname)
