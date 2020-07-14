#!/usr/bin/python
# -*- coding: utf-8 -*-
# this version only works on Windows as it uses the winsound library
import corona_python_text
import corona_python_text_csv
import math
import numpy
from operator import itemgetter
import winsound
import time
import datetime
import argparse

# code partly copied from answers at https://stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound

     
def generate_sine_wave(frequency, duration):
    ''' Generate a tone at the given frequency.

        Limited to unsigned 8-bit samples at a given sample_rate.
        The sample rate should be at least double the frequency.
    '''
    winsound.Beep(int(frequency), int(duration*1000))

def generate_sine_wave_array(freq_arr, duration_arr):
    ''' Generate a tone at the given frequency.

        Limited to unsigned 8-bit samples at a given sample_rate.
        The sample rate should be at least double the frequency.
    '''

    for frequency, duration in zip(freq_arr, duration_arr):
        winsound.Beep(int(frequency), int(duration*1000))

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


def play_audio(cases_by_area, selected_area="", bass_octave = 3, range_octaves=4, scaling=1, shorttext=False, duration=1):    
    bass_note = 261.63 / (5-bass_octave) # one octave below middle C if bass-octave is its default
    print("bass note = {h} Hz".format(h=bass_note))
    print("scaling = {s}. freq prop. to (cases/max cases)**scaling".format(s=scaling))
    
    for area in sorted(cases_by_area):
        if selected_area != "" and area != selected_area:
            continue
        area_cases = sorted(cases_by_area[area], key=itemgetter(0))        
        startDate = area_cases[0][0]
        endDate = area_cases[-1][0]
        startDate = corona_python_text.datestr_to_date(startDate)
        endDate = corona_python_text.datestr_to_date(endDate)

        cases_by_date = corona_python_text.get_cases_by_date(area_cases , startDate, endDate)
        ncases_list = list(cases_by_date.items())        
        ncases_list = sorted(ncases_list, key=itemgetter(0))            
        datelist = [i[0] for i in ncases_list]
        ncases_valslist = [i[1] if i[1] else 0 for i in ncases_list]

        print(area)
        max_cases = max(ncases_valslist)
        #print(max(ncases_valslist))
        print("max cases = ",max_cases)
        
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
                elif abs((ncases_valslist[i]-ncases_valslist[i-1])/ncases_valslist[i-1]) < 0.2:
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
                print("{a}{b}{s}".format(a=notes[int((octaves*12) % 12)], b=int(bass_octave+math.floor(octaves)), s=note), end=" ")
            else:
                print("{d} {c} cases, {f:.3f} Hz, {n:.3f} octaves, {a}{b}{s}".format(d=n[0], c=n[1], f=freq, n=octaves, a=notes[int((octaves*12) % 12)], b=int(bass_octave+math.floor(octaves)),s=note))
            freq_arr.append(float(freq))
            duration_arr.append(duration_2)        
            # generate_sine_wave(
            # # see http://www.phy.mtu.edu/~suits/notefreqs.html
                # frequency=float(freq),   # Hz, waves per second C6
                # duration=duration_2,       # seconds to play sound
                # volume=0.25,        # 0..1 how loud it is
                # sample_rate=44100,  # number of samples per second: 11025, 22050, 44100
            # )
            
        print("\n")
        generate_sine_wave_array(freq_arr, duration_arr)
        time.sleep(3)
        


if __name__ == '__main__':
    """
    If invoked at the command-line
    """
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("--short",action="store_true",
                        help="shorter form text output with just the note not date, cases, freq etc.")
    args = parser.parse_args()
    
    # play the England cases, with square root scaling            
    cases_by_area = corona_python_text.cases_by_country
    #play_audio(cases_by_area, "", 2, 5, 0.5, args.short, 0.5)	
    # play regions, with square root scaling
    cases_by_area = corona_python_text.cases_by_region
    #play_audio(cases_by_area, "", 2, 5, 0.5, args.short, 0.5)
    
    # import from csv file (to get Scottish and Welsh local data)
    countries_datearrays = corona_python_text_csv.countries_datearrays
    countries_dailyarrays = corona_python_text_csv.countries_dailyarrays
    areas_datearrays = corona_python_text_csv.areas_datearrays
    areas_dailyarrays = corona_python_text_csv.areas_dailyarrays
    
    
    # play Scotland, Wales and Northern Ireland
    # Northern Ireland has a few days with a negative number of daily cases!
    # this occurs to a larger extent in NI local data
    # also for "Unknown" area in Wales
    # and for a few Scottish areas to a minor extent
    
    # set any negative values to zero
    # and truncate the array before the first case
    cases_by_area = {}
    for c in ["Scotland", "Wales", "Northern Ireland"]:
        cases_by_area_c = [(datetime.date.isoformat(d), max(int(n),0)) for (d,n) in zip(countries_datearrays[c], countries_dailyarrays[c])]        
        cases_by_area_c2 = []
        totalcases = 0        
        for i, n in enumerate(cases_by_area_c):
            totalcases = totalcases + n[1]
            #print(n, totalcases)
            if totalcases > 0:
                cases_by_area_c2.append(n)

        #print(cases_by_area_c)    
        cases_by_area[c] = cases_by_area_c2
    #print(cases_by_area)
    play_audio(cases_by_area, "", 2, 5, 0.5, args.short, 0.5)

    # play Scottish and Welsh areas
    cases_by_area = {}
    for c in ["Scotland", "Wales"]:
        for a in sorted(corona_python_text_csv.countries_areaarr[c]):
            cases_by_area_a = [(datetime.date.isoformat(d), max(int(n),0)) for (d,n) in zip(areas_datearrays[a], areas_dailyarrays[a])]
            cases_by_area_a2 = []
            totalcases = 0
            for i, n in enumerate(cases_by_area_a):
                totalcases = totalcases + n[1]
                if totalcases > 0:
                    cases_by_area_a2.append(n)
        
            cases_by_area[a] = cases_by_area_a2
        play_audio(cases_by_area, "", 3, 4, 0.5, args.short, 0.5)
    	
    # play upper-tier local authorities
    cases_by_area = corona_python_text.cases_by_utla

    # select only Cornwall
    # selectedarea = 'Cornwall and Isles of Scilly'
    # play without scaling
    # play_audio(cases_by_area, selectedarea)

    # play with square-root scaling
    # play_audio(cases_by_area, selectedarea, scaling=0.5)

    # play all UTLAs with square-root scaling
    play_audio(cases_by_area, "", 3, 4, 0.5, args.short, 0.5)
