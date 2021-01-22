#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# this uses the API for the data
# publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/index.html
# first run uk-covid19-API-download_all_utla.py
# and uk-covid19-API-download_all_nation.py
#
# using pygame

import math
import numpy
from operator import itemgetter
import pygame
import wave
from pygame.locals import *
from itertools import *
import time
import datetime
import argparse
import os
import re
import corona_python_text_csv_api 

# code partly copied from answers at
# stackoverflow.com/questions/974071/
# python-library-for-playing-fixed-frequency-sound
# saving to file: https://github.com/esdalmaijer/Save_PyGame_Sound

size = (1920, 1080)
# bits in the sound samples to be generated
bits = 16
green = (  0, 255,  0)
darkgreen = (  0, 127,  0)
black = (  0,   0,  0)

yellow_0_10 = (  224, 229,  67)
green_10_50 = (  116, 187, 104)
green_50_100 = (  57, 147, 132)
blue_100_200 = (  32, 103, 171)
blue_200_400 = (  18,  64, 127)
purple_400_800 = (83,   8,  74)
purple_800_inf = (43,   2,  38)

pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
display_surf = pygame.display.set_mode(size,
                                       pygame.HWSURFACE | pygame.DOUBLEBUF)
font = pygame.font.SysFont('dejavusansmono', 96)
font2 = pygame.font.SysFont('dejavusans', 60)
font3 = pygame.font.SysFont('dejavusans', 24)
#time.sleep(10)

     
def generate_sine_wave(frequency, duration, volume=0.5, sample_rate=44100):
    ''' Generate a tone at the given frequency.

        The sample rate should be at least double the frequency.
    '''
    if sample_rate < (frequency * 2):
        print('Warning: sample_rate must be at least double the frequency '
              f'to accurately represent it:\n    sample_rate {sample_rate}'
              f' ≯ {frequency*2} (frequency {frequency}*2)')
    num_samples = int(sample_rate * duration)
    rest_frames = num_samples % sample_rate

    # make samples
    buf = numpy.zeros((num_samples + rest_frames, 2),
                      dtype=numpy.int16)
    max_sample = 2**(bits-1) - 1    
    s = lambda i: volume * max_sample * math.sin(
                                    2 * math.pi * frequency * i / sample_rate)
    for k in range(num_samples):
        buf[k][0] = s(k)*((num_samples-k)/num_samples)
        buf[k][1] = s(k)*((num_samples-k)/num_samples)
    sound = pygame.sndarray.make_sound(buf)
    #play once
    sound.play()
    time.sleep(duration)
        



def generate_sine_wave_array(freq_arr, duration_arr, wavefile = '',
                             rest = 0.1, volume=0.5, sample_rate=44100,
                             quietmode=False):
    ''' Generate a tone at the given frequency.

        The sample rate should be at least double the frequency.
    '''
    # create one buffer for the whole array
    allbuf = numpy.zeros((0,2), dtype=numpy.int16)
    if not(quietmode):
        for frequency, duration in zip(freq_arr, duration_arr):
            if sample_rate < (frequency * 2):
                print(
                'Warning: sample_rate must be at least double the frequency '
                f'to accurately represent it:\n    sample_rate {sample_rate}'
                f' ≯ {frequency*2} (frequency {frequency}*2)')
            # calculate the number of samples, use variable 'rest' to leave a gap
            # between one note and the next
            num_samples = int(sample_rate * duration*(1-rest))
            rest_frames = int(duration*rest*sample_rate)
            # + ((sample_rate - num_samples) % sample_rate)
            
            # make samples
            # a numpy array of zeros, 2 channels for stereo
            buf = numpy.zeros((num_samples + rest_frames, 2),
                              dtype=numpy.int16)
            max_sample = 2**(bits-1) - 1
            # generate sine wave at a particular frequency 
            s = lambda i: volume * max_sample * math.sin(
                                    2 * math.pi * frequency * i / sample_rate)
            # make the volume decay linearly with time
            for k in range(num_samples):
                buf[k][0] = s(k)*((num_samples-k)/num_samples)
                buf[k][1] = s(k)*((num_samples-k)/num_samples)
            # add this note to the buffer
            allbuf = numpy.vstack((allbuf, buf))    
        sound = pygame.sndarray.make_sound(allbuf)
    
    if not(quietmode):
        wfile = wave.open(wavefile, 'w')
        wfile.setframerate(sample_rate)
        wfile.setnchannels(2)
        wfile.setsampwidth(2)
        # write raw PyGame sound buffer to wave file
        wfile.writeframesraw(sound.get_raw())
        # play once      
        if not(quietmode):
            sound.play()
    # the delay is now introduced in the code for drawing the animated graph
    # time.sleep(sound.get_length())
    return sound.get_length()
        


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


notes = ["C ", "C♯", "D ", "E♭", "E ", "F ",
         "F♯", "G ", "A♭", "A ", "B♭", "B "]

def draw_graph_pygame(datelist, ncases_valslist, max_cases, area):
    '''
    draw a line graph in a pygame window
    '''
    display_surf.fill(black)
    img = font2.render(area, True, green, black)        
    display_surf.blit(img, (20, 20))    
    win_h = size[1]
    win_w = size[0]
    npoints = len(ncases_valslist)
    points = [[0, win_h]]
    for i, (d, n) in enumerate(zip(datelist, ncases_valslist)):
        x = int((i/npoints) * win_w)
        y = int(win_h - (n/max_cases) * win_h)
        points.append([x, y])
    pygame.draw.lines(display_surf, green, False, points, 3)
    pygame.display.flip()

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
        
def overplot_fill_graph(datelist, ncases_valslist, caserate_list, max_cases,
                        duration_arr, notetxt_arr, area, quietmode=False):
    '''
    overplot a fill for the line graph
    animated, delay to sync with sound
    and write text to annotate
    '''
    # height and width of window
    win_h = size[1]
    win_w = size[0]
    npoints = len(ncases_valslist)
    # duration will be 1/4, 1/2 and 1 * the maximum duration
    # by default set to 0.5 seconds in call to function play_audio()
    min_duration = max(duration_arr)/4
    pngfilecount = 0
    for i, (d, n, r, t, m) in enumerate(zip(datelist, ncases_valslist,
                                            caserate_list,
                                            duration_arr, notetxt_arr)):
        curtime = pygame.time.get_ticks()
        # draw a vertical line
        x = int((i/npoints) * win_w)    
        y = int(win_h - (n/max_cases) * win_h)
        # if its the first of the month
        if d[-2:] == "01":
            pygame.draw.line(display_surf, darkgreen, [x, win_h], [x, 0], 1)
            # write month
            img = font3.render(d[5:7], True, darkgreen, black)
            display_surf.blit(img, (x+5, 5))
            
        pygame.draw.line(display_surf, choose_colour(r), [x, win_h], [x, y], 8)
        # write date in pygame window
        img = font2.render(d, True, green, black)        
        display_surf.blit(img, (20, 120))
        
        # write the musical note text
        musicnote = m
        try:
            img = font.render(musicnote, True, green, black)
        except UnicodeError:
            # the semiquaver in Unicode is U+1D161
            # pygame doesn't seem to work with characters above FFFF
            # replace with beamed semiquavers character
            musicnote = musicnote.replace("𝅘𝅥𝅯", "♬")
            img = font.render(musicnote, True, green, black)
        display_surf.blit(img, (20, 220))

        # write number of cases on day
        if n == 1:
            img = font2.render(f"{n:5} case  ", True, green, black)        
        else:
            img = font2.render(f"{n:5} cases  ", True, green, black)        
        display_surf.blit(img, (400, 120))
        
        # write rate per 100k
        img = font2.render(f"{r} /100k last 7 days  ", True, green, black)        
        display_surf.blit(img, (900, 120))
        
        pygame.display.flip()
        # save png file
        # these can be converted to video using ffmpeg
        # hamelot.io/
        # visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video
        # print(t/min_duration)        
        if t == min_duration:
            # i.e. if its a semiquaver
            # this is if its the same number of cases as the previous day
            pngfile = os.path.join("graphfiles",
                                   f"{area}_{pngfilecount:05}.png")
            pngfilecount += 1
            pygame.image.save(display_surf, pngfile)
        else:
            # this program uses a quaver where there is a small change in
            # case numbers, and a crochet if a large one or a zero
            # if so, write out several png files as needed            
            dur = int(t / min_duration)            
            for r in range(dur):
                pngfile = os.path.join("graphfiles",
                                       f"{area}_{pngfilecount:05}.png")
                pngfilecount += 1
                pygame.image.save(display_surf, pngfile)
                
        curtime2 = pygame.time.get_ticks()
        # wait for the note duration, minus the time taken to execute the code
        if not(quietmode):
            pygame.time.wait(int(t*1000) - (curtime2-curtime))

def play_audio(cases_by_area, selected_areas=[], bass_octave = 3,
               range_octaves=4, scaling=1, shorttext=False, duration=1,
               quietmode=False):
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
         
        datelist = [i[0] for i in area_cases]
        ncases_valslist = [i[1] if i[1] else 0 for i in area_cases]
        caserate_list = [i[2] for i in area_cases]

        textout_a += area + "\n"
        max_cases = max(ncases_valslist)
        # print(max(ncases_valslist))
        textout_a += f"max cases = {max_cases}\n"
        if max_cases == 0:
            print(f"no cases in {area}, skipping")
            continue
        # turn underscores back to spaces for captions
        area_l = area.replace("_", " ")
        pygame.display.set_caption(
            f"SARS-CoV2 cases by specimen date in {area_l}")
        
        # find occurance of 1st case in the area
        ncases_numpy = numpy.array(ncases_valslist, dtype=int)
        firstnonzero = numpy.nonzero(ncases_numpy)[0][0]
        # remove part of array before 1st case in the area
        datelist = datelist[firstnonzero:]
        ncases_valslist = ncases_valslist[firstnonzero:]
        caserate_list = caserate_list[firstnonzero:]
        
        # draw the line graph for the area
        draw_graph_pygame(datelist, ncases_valslist, max_cases, area_l)
        
        # generate the frequencies, durations, and musical note texts
        freq_arr = []
        duration_arr = []
        notetxt_arr = []
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
            # write text to terminal in either short or long form

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
            
        textout_a += "\n\n"
        textout += textout_a
        print(textout_a)
        # except if text only output, play sound and save it to a wavefile
        # if text only, just save it to file but don't play it
        # done by passing the value of quietmode to 
        # generate_sine_wave_array and overplot_fill_graph
        wavefile = area.lower() + ".wav"
        wavefile = os.path.join("audiofiles", wavefile)
        soundlength = generate_sine_wave_array(freq_arr, duration_arr,
                                               wavefile, quietmode)
        overplot_fill_graph(datelist, ncases_valslist,  caserate_list,
                            max_cases, duration_arr, notetxt_arr, area,
                            quietmode)
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
    parser.add_argument("--quietmode",action="store_true",
                        help="quiet mode(don't play audio)")
    parser.add_argument("-o", "--output", help=("Directs the text output to a "
                                                "filename of your choice"))
    parser.add_argument("-a", "--areaselect", help=("Select areas containing"
                                                    "text matching regex"))
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
    if args.areaselect:
        # if selecting areas using a substring, ignore case
        q = re.compile(args.areaselect.strip(), re.IGNORECASE)
    
    # play the UK and nations cases, with square root scaling            
    cases_by_area = corona_python_text_csv_api.cases_by_country
    # print(cases_by_area)

    if args.areaselect:                
        cases_by_area = {k:v for k, v in cases_by_area.items() if q.search(k.lower())}
    notes_nations = play_audio(cases_by_area, "", 2, 6, 0.5,
                               args.short, 0.5, args.quietmode)

    # play regions of England
    cases_by_area = corona_python_text_csv_api.cases_by_region
    if args.areaselect:
        cases_by_area = {k:v for k, v in cases_by_area.items() if q.search(k.lower())}   
    notes_regions = play_audio(cases_by_area, "", 2, 6, 0.5,
                               args.short, 0.5, args.quietmode)
    # example selecting a region
    #notes_regions = play_audio(cases_by_area, ["North_West"], 2, 6, 0.5,
    #                           args.short, 0.5, args.quietmode)

    # play UTLAs
    cases_by_areaUTLA = corona_python_text_csv_api.cases_by_UTLA
    if args.areaselect:
        cases_by_area = {k:v for k, v in cases_by_areaUTLA.items() if q.search(k.lower())}   
    notes_UTLAs = play_audio(cases_by_areaUTLA, "", 3, 5, 0.5,
                             args.short, 0.5, args.quietmode)

    # play LTLAs only if the command-line argument is set
    if args.ltla:
        cases_by_areaLTLA = corona_python_text_csv_api.cases_by_LTLA
        # remove any LTLA which is also a UTLA
        cases_by_areaLTLA = {k:v for k, v in cases_by_areaLTLA.items() if k not in cases_by_areaUTLA.keys()}
        if args.areaselect:
            cases_by_areaLTLA = {k:v for k, v in cases_by_areaLTLA.items() if q.search(k.lower())}   
        notes_LTLAs = play_audio(cases_by_areaLTLA, "", 3, 5, 0.5,
                                 args.short, 0.5, args.quietmode)                             

    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(notes_nations)
            output_file.write(notes_regions)
            output_file.write(notes_UTLAs)
            if args.ltla:
                output_file.write(notes_LTLAs)

pygame.quit()
