# Novel Coronavirus Data #

Using data published at coronavirus.data.gov.uk (initially)

corona_python_test.py
=====================
text-based output of cases and deaths

uk-covid19-API-download_all_nation.py
=====================================
downloads as CSV files from API at Public Health England all nations, regions of England and upper and lower tier local authorities
data is put in folder data_all/

corona_python_text_csv_api.py
=============================
puts the data into python dictionary objects

pygame_apidata.py
=================
the main file producing the graphs, which are saved as a load of png files in graphfiles/
Audio files are saved in the audiofiles/ as .wav files. 
I use the program soundconverter to convert to .mp3 (I should really do that programaticcally but haven't done yet)

pygame_ffmpeg_makevideos.py
===========================
use the ffmpeg command to make a video out of the png files and the mp3 files

pygame_nations_apidata.py
=========================
this program creates a pygame window with 4 areas at the same time tiled. 
still in development, at present hard-coded to use England, Wales, Scotland and Northern Ireland. the duration of each musical note is always the same in contrast to the main file pygame_apidata.py where it may vary

pygame_ffmpeg_makevideos_fournations.py
=======================================
use the ffmpeg command to make a video out of the png files and the mp3 files. slightly different options are used because of the constant musical note duration (therefore there is always only 1 frame per day)








