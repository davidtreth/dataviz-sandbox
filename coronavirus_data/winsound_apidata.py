#!/usr/bin/python
# -*- coding: utf-8 -*-
# this version only works on Windows as it uses the winsound library
# this uses the API for the data
# publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/index.html
# first run uk-covid19-API-download_all_utla.py
# and uk-covid19-API-download_all_nation.py

import math
import numpy
from operator import itemgetter
import winsound
import time
import datetime
import argparse
import corona_python_text_csv_api 

# code partly copied from answers at
# stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound

     
def generate_sine_wave(frequency, duration):
    ''' Generate a tone at the given frequency.

        Limited to unsigned 8-bit samples at a given sample_rate.
        The sample rate should be at least double the frequency.
    '''
    winsound.Beep(int(frequency), int(duration*1000))

def generate_sine_wave_array(freq_arr, duration_arr, rest=0.2):
    ''' Generate a tone at the given frequency.

        Limited to unsigned 8-bit samples at a given sample_rate.
        The sample rate should be at least double the frequency.
    '''

    for frequency, duration in zip(freq_arr, duration_arr):
        winsound.Beep(int(frequency), int((duration*1000)*(1-rest)))
        time.sleep(rest*duration)

# octave = numpy.arange(13)
# octave = 2**(octave/12)
# octave = octave * 261.63

# tones = numpy.array([octave[0],octave[2],octave[4],octave[5],octave[7],octave[9],octave[11],octave[12]])

# for f in tones:
    # print(f)
    # generate_sine_wave(
    # # see http://www.phy.mtu.edu/~suits/notefreqs.html
        # frequency=float(f),   # Hz, waves per second C6
        # duration=1.0,       # seconds to play sound
        # volume=0.25,        # 0..1 how loud it is
        # sample_rate=22050,  # number of samples per second: 11025, 22050, 44100
    # )


notes = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def play_audio(cases_by_area, selected_area="", bass_octave = 3,
               range_octaves=4, scaling=1, shorttext=False, duration=1,
               textonly=False):
    textout = ""   
    bass_note = 261.63 / (5-bass_octave)
    # one octave below middle C if bass-octave is its default
    textout += "bass note = {h} Hz\n".format(h=bass_note)
    textout += "scaling={s}. freq prop. to (cases/max cases)^scaling\n".format(
                s=scaling)
    
    for area in sorted(cases_by_area):
        textout_a = ""
        if selected_area != "" and area != selected_area:
            continue
        area_cases = sorted(cases_by_area[area], key=itemgetter(0))        
        startDate = area_cases[0][0]
        endDate = area_cases[-1][0]
        startDate = datetime.datetime.fromisoformat(startDate)
        endDate = datetime.datetime.fromisoformat(endDate)
         
        datelist = [i[0] for i in area_cases]
        ncases_valslist = [i[1] if i[1] else 0 for i in area_cases]

        textout_a += area + "\n"
        max_cases = max(ncases_valslist)
        #print(max(ncases_valslist))
        textout_a += f"max cases = {max_cases}\n"
        if max_cases == 0:
            print(f"no cases in {area}, skipping")
            continue        
        
        freq_arr = []
        duration_arr = []
        for i, n in enumerate(zip(datelist, ncases_valslist)):
            # range of 4 octaves by default
            octaves = range_octaves*((n[1]/max_cases)**scaling)
            # quantise to the nearest semitone
            octaves = math.floor(octaves*12.0)/12.0
            # calculate frequency
            freq = bass_note*(2**octaves)
            
            if i > 0 and ncases_valslist[i-1]>0:
                if ncases_valslist[i] == ncases_valslist[i-1]:
                    duration_2 = duration / 4
                elif abs(
        (ncases_valslist[i]-ncases_valslist[i-1])/ncases_valslist[i-1]) < 0.2:
                    duration_2 = duration / 2
                else:
                    duration_2 = duration
            else:
                duration_2 = duration
            if duration_2 == duration:
                note = "♩"
            elif duration_2 == duration/2:
                note = "♪"
            elif duration_2 == duration/4:
                note = "𝅘𝅥𝅯 "
            else:
                note = "♫"
            if shorttext:
                textout_a += "{a}{b}{s} ".format(
                    a=notes[int((octaves*12) % 12)],
                    b=int(bass_octave+math.floor(octaves)), s=note)
                if (i % 14 == 0 and i > 0):
                    textout_a += "\n"
            else:
                textout_a += ("{d} {c} cases, {f:.3f} Hz, "
                              "{n:.3f} octaves, {a}{b}{s}\n").format(
                              d=n[0], c=n[1], f=freq, n=octaves,
                              a=notes[int((octaves*12) % 12)],
                              b=int(bass_octave+math.floor(octaves)),s=note)
            freq_arr.append(float(freq))
            duration_arr.append(duration_2)        
            # generate_sine_wave(
            # # see http://www.phy.mtu.edu/~suits/notefreqs.html
                # frequency=float(freq),   # Hz, waves per second C6
                # duration=duration_2,       # seconds to play sound
                # volume=0.25,        # 0..1 how loud it is
                # sample_rate=44100,
                # number of samples per second: 11025, 22050, 44100
            # )
            
        textout_a += "\n\n"
        textout += textout_a
        print(textout_a)
        if not(textonly):
            generate_sine_wave_array(freq_arr, duration_arr)
            time.sleep(3)
    return textout
        


if __name__ == '__main__':
    """
    If invoked at the command-line
    """
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("--short",action="store_true",
                        help=("shorter form text output with just "
                              "the note not date, cases, freq etc."))
    parser.add_argument("--textonly",action="store_true",
                        help="text only output (don't play audio)")
    parser.add_argument("-o", "--output", help=("Directs the text output to a "
                                                "filename of your choice"))
    args = parser.parse_args()    
    
    # play the UK and nations cases, with square root scaling            
    cases_by_area = corona_python_text_csv_api.cases_by_country
    #print(cases_by_area)
    
    notes_nations = play_audio(cases_by_area, "", 3, 5, 0.5,
                               args.short, 1, args.textonly)

    # play regions of England	
    cases_by_area = corona_python_text_csv_api.cases_by_region
    notes_regions = play_audio(cases_by_area, "", 3, 5, 0.5,
                               args.short, 1, args.textonly)

    # play UTLAs
    cases_by_area = corona_python_text_csv_api.cases_by_UTLA
    notes_UTLAs = play_audio(cases_by_area, "", 3, 5, 0.5,
                             args.short, 1, args.textonly)

    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(notes_nations)
            output_file.write(notes_regions)
            output_file.write(notes_UTLAs)
