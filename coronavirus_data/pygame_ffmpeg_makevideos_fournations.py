#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import corona_python_text_csv_api 

audiodir = "audiofiles"
graphdir = "graphfiles"
videodir = "videofiles"

def create_video(areaname):
    png_pattern = f"{os.path.join(graphdir, areaname)}_%05d.png"
    audiofile = f"{os.path.join(audiodir, areaname.lower())}.mp3"
    videofile = f"{os.path.join(videodir, areaname)}.mp4"
    ffmpeg_cmd = (f"ffmpeg -r 2 -f image2 -s 1920x1080 -i {png_pattern}"
                 f" -i {audiofile} -vcodec libx264 -crf 25 -pix_fmt yuv420p"
                 f" -acodec copy {videofile}")
    subprocess.call(ffmpeg_cmd, shell=True)
        

create_video("four_nations")
create_video("four_nations_globalmax")
