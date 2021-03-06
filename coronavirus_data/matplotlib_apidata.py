#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# this file will do similar graphs to pygame_apidata.py
# but use matplotlib. without sound for the time being

import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from operator import itemgetter
# from itertools import *
# import time
import datetime
import argparse
# import os
import re
import corona_python_text_csv_api 

# for labelling of y-axis
dailycasenums = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000,
                 20000, 50000, 100000]
rates7day = [50.0, 100.0, 200.0, 400.0, 800.0, 1600.0]                

# define colours to be used - based on Public Health England map
green = (  0, 255,  0)
darkgreen = (  0, 127,  0)
black = (  0,   0,  0)
darkgrey = (76, 76, 76)

yellow_0_10 = (  224, 229,  67)
green_10_50 = (  116, 187, 104)
green_50_100 = (  57, 147, 132)
blue_100_200 = (  32, 103, 171)
blue_200_400 = (  18,  64, 127)
purple_400_800 = (83,   8,  74)
purple_800_inf = (43,   2,  38)

notes = ["C ", "C♯", "D ", "E♭", "E ", "F ",
         "F♯", "G ", "A♭", "A ", "B♭", "B "]
         
def choose_colour(rate100k):
    if rate100k < 10.0:
        colour = yellow_0_10
    elif rate100k < 50.0:
        colour = green_10_50
    elif rate100k < 100.0:
        colour = green_50_100
    elif rate100k < 200.0:
        colour = blue_100_200
    elif rate100k < 400.0:
        colour = blue_200_400
    elif rate100k < 800.0:
        colour = purple_400_800
    else:
        colour = purple_800_inf
    return colour
    
    
def draw_graph(datelist, ncases_valslist, caserate_list, max_cases,
                        duration_arr, notetxt_arr, area, population, caption):
    '''
    draw a filled histogram
    '''
    fig, ax = plt.subplots()
    ax.plot(datelist, ncases_valslist)
    # Major ticks every 3 months.
    fmt_3month = mdates.MonthLocator(bymonthday=1, interval=3)
    ax.xaxis.set_major_locator(fmt_3month)
    # Minor ticks every month.
    fmt_month = mdates.MonthLocator(bymonthday=1)
    ax.xaxis.set_minor_locator(fmt_month)
    ax.set_title(caption)    
    
def allgraphs(cases_by_area, selected_areas=[], bass_octave = 3,
               range_octaves=4, scaling=1, shorttext=False, duration=1):
    textout = ""   
    bass_note = 261.63 * 2**(bass_octave-4)
    # one octave below middle C if bass-octave is its default
    textout += "bass note = {h} Hz\n".format(h=bass_note)
    textout += "scaling={s}. freq prop. to (cases/max cases)^scaling\n".format(
                s=scaling)
    
    for area in sorted(cases_by_area):
        textout_a = ""
        if len(selected_areas) > 0 and area not in selected_areas:
            continue
        area_cases = sorted(cases_by_area[area], key=itemgetter(0))        
        
        startDate = area_cases[0][0]
        endDate = area_cases[-1][0]
        startDate = datetime.datetime.fromisoformat(startDate)
        endDate = datetime.datetime.fromisoformat(endDate)
         
        datelist = [datetime.datetime.fromisoformat(i[0]) for i in area_cases]
        ncases_valslist = [i[1] if i[1] else 0 for i in area_cases]
        caserate_list = [i[2] for i in area_cases]

        textout_a += area + "\n"
        max_cases = max(ncases_valslist)
        # print(max(ncases_valslist))
        textout_a += f"max cases = {max_cases}\n"
        if max_cases == 0:
            print(f"no cases in {area}, skipping")
            continue
            
        total_cases = sum(ncases_valslist)        
        textout_a += f"total cases = {total_cases}\n"
                
        # discard last 7 days for calulating total rate and population
        total_rate = sum(caserate_list[:-7])/7        
        total_cases2 = sum(ncases_valslist[:-7])        
        textout_a += f"total rate/100k pop. = {total_rate:.2f}\n"
        
        total_pop = round((100000/total_rate)*total_cases2)
        textout_a += f"total pop. = {total_pop}\n"
        
        # turn underscores back to spaces for captions
        area_l = area.replace("_", " ")
        caption = f"SARS-CoV2 cases by specimen date in {area_l}"
        print(caption)
        
        # find occurance of 1st case in the area
        ncases_numpy = numpy.array(ncases_valslist, dtype=int)
        firstnonzero = numpy.nonzero(ncases_numpy)[0][0]
        # 
        # COMMENTED OUT remove part of array before 1st case in the area
        # 
        # datelist = datelist[firstnonzero:]
        # ncases_valslist = ncases_valslist[firstnonzero:]
        # caserate_list = caserate_list[firstnonzero:]
        
        
        # generate the frequencies, durations, and musical note texts
        freq_arr = []
        duration_arr = []
        notetxt_arr = []
        volume_arr = []
        volume = 1
        for i, n in enumerate(zip(datelist, ncases_valslist, caserate_list)):
            # range of 4 octaves by default
            octaves = range_octaves*((n[1]/max_cases)**scaling)
            # quantise to the nearest semitone
            octaves = math.floor(octaves*12.0)/12.0
            # calculate frequency
            freq = bass_note*(2**octaves)
            
            # check change in cases since previous day            
            if i > 0 and ncases_valslist[i-1]>0:
                # if the same number, a semiquaver 
                if ncases_valslist[i] == ncases_valslist[i-1]:
                    duration_2 = duration / 4
                # if a small change, a quaver
                elif abs(
        (ncases_valslist[i]-ncases_valslist[i-1])/ncases_valslist[i-1]) < 0.2:            
                    duration_2 = duration / 2
                # if a large change, a crochet
                else:
                    duration_2 = duration
            # also a crochet for the first element, or if previous was a zero
            else:
                duration_2 = duration
            # create text for musical note
            if duration_2 == duration:
                note = "♩ "
            elif duration_2 == duration/2:
                note = "♪ "
            elif duration_2 == duration/4:
                note = "𝅘𝅥𝅯 "
            else:
                note = "♫ "
                
            if i > 2 and n[1]==0 and ncases_valslist[i-1]==0 and ncases_valslist[i-2]==0:
                volume = 0.0
                note = "𝄽 "
            else:
                volume = 1.0                
            # write text to terminal in either short or long form
            if note == "𝄽 ":
                notetxt = f"   {note}"
            else:
                notetxt = "{a}{b}{s}".format(
                    a=notes[int((octaves*12) % 12)],
                    b=int(bass_octave+math.floor(octaves)), s=note)
            if shorttext:                    
                textout_a += notetxt
                if ((i+1) % 14 == 0 and i > 0):
                    textout_a += "\n"
            else:
                notetxt2 = ("{d} {c} cases, {f:.3f} Hz, "
                            "{n:.3f} octaves, {a}{b}{s}{r}/100k last 7 days\n").format(
                            d=n[0], c=n[1], f=freq, n=octaves,
                            a=notes[int((octaves*12) % 12)],
                            b=int(bass_octave+math.floor(octaves)),s=note,
                            r=n[2])
                textout_a += notetxt2

            # add the note to the arrays
            notetxt_arr.append(notetxt)
            freq_arr.append(float(freq))
            duration_arr.append(duration_2)
            volume_arr.append(volume)                    
            
        textout_a += "\n\n"
        textout += textout_a
        print(textout_a)

        draw_graph(datelist, ncases_valslist,  caserate_list,
                   max_cases, duration_arr, notetxt_arr, area,
                   total_pop, caption)
        plt.show()
    return textout
    
if __name__ == '__main__':
    '''
    If invoked at the command-line
    '''
    # Create the command line options parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("--short",action="store_true",
                        help=("shorter form text output with just "
                              "the note not date, cases, freq etc."))    
    parser.add_argument("-o", "--output", help=("Directs the text output to a "
                                                "filename of your choice"))
    parser.add_argument("-y", "--ysize", help=("sets y size"
                                                "default 1280x720"))                                                
    parser.add_argument("-a", "--areaselect", help=("Select areas containing"
                                                    "text matching regex"))
    parser.add_argument("--utla",action="store_true",
                        help=("include upper-tier LAs"
                        "by default don't"))                                                     
    parser.add_argument("--ltla",action="store_true",
                        help=("include lower-tier LAs (England only)"
                        "by default don't")) 
                                                        
    # example run this command to select LAs containing Isle/Island 
    # python pygame_apidata.py --quietmode --areaselect Isl[ae] --short
    
    # example selects Devon (county council area), and the lower-tier areas
    # East Devon, Mid Devon, North Devon, South Devon
    # note - Devon county has some lower-tier areas
    # that don't contain the word Devon
    # and 2 unitary LAs (Plymouth + Torbay) separate from Devon county
    # python pygame_apidata.py --quietmode --areaselect devon --short --ltla
    
                              
    args = parser.parse_args()
    if args.ysize:
        try:
            ysize = int(args.ysize)
        except:
            # if args.ysize doesn't convert to an integer, set it to the default
            ysize = 720
        if ysize < 216 or ysize > 2180:
            print("ysize out of bounds 216-2180, setting to default 720")
            ysize = 720
    else:
        # if no args.ysize, set it to the default
        ysize = 720
    size = (int((16/9)*ysize), ysize)

    if args.areaselect:
        # if selecting areas using a substring, ignore case
        q = re.compile(args.areaselect.strip(), re.IGNORECASE)
    
    # the UK and nations cases
    cases_by_area = corona_python_text_csv_api.cases_by_country
    # print(cases_by_area)
    # Code to create the graphs
    
    
    if args.areaselect:                
        cases_by_area = {k:v for k, v in cases_by_area.items() if q.search(k.lower())}

    graphs_nations = allgraphs(cases_by_area, "", 2, 6, 0.5,
                               args.short, 0.5)
    # regions of England
    cases_by_area = corona_python_text_csv_api.cases_by_region
    if args.areaselect:
        cases_by_area = {k:v for k, v in cases_by_area.items() if q.search(k.lower())}   
    # Code to create the graphs 
    graphs_regions = allgraphs(cases_by_area, "", 2, 6, 0.5,
                               args.short, 0.5)
    # play UTLAs only if the command-line argument is set
    if args.utla:
        cases_by_areaUTLA = corona_python_text_csv_api.cases_by_UTLA
        if args.areaselect:
            cases_by_areaUTLA = {k:v for k, v in cases_by_areaUTLA.items() if q.search(k.lower())}   
        # Code to create the graphs 
        graphs_UTLAs = allgraphs(cases_by_areaUTLA, "", 3, 5, 0.5,
                               args.short, 0.5)    
    # play LTLAs only if the command-line argument is set
    if args.ltla:
        cases_by_areaLTLA = corona_python_text_csv_api.cases_by_LTLA
        # remove any LTLA which is also a UTLA
        cases_by_areaLTLA = {k:v for k, v in cases_by_areaLTLA.items() if k not in cases_by_areaUTLA.keys()}
        if args.areaselect:
            cases_by_areaLTLA = {k:v for k, v in cases_by_areaLTLA.items() if q.search(k.lower())}
        # Code to create the graphs                
        graphs_LTLAs = allgraphs(cases_by_areaLTLA, "", 3, 5, 0.5,
                               args.short, 0.5)

    # not sure what text to output for this file
    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(graphs_nations)
            output_file.write(graphs_regions)
            if args.utla:
                output_file.write(graphs_UTLAs)
            if args.ltla:
                output_file.write(graphs_LTLAs)
