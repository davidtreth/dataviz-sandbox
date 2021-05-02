sh concatvideos_short.sh
sh concatvideos_NI.sh
sh concatvideos_wales.sh
sh concatvideos_scotland.sh
sh concatvideos_London.sh
sh concatvideos_eng.sh
sh concatvideos_eng_ltla.sh
sh concatvideos.sh
python pygame_concatvideos_duration.py
rm -v endframes/*png
python ffmpeg_extract_endframes.py
cd ..
pygame_ffmpeg_makevideo_endframes.py
