#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# this uses the API for the data
# publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/index.html
# first run uk-covid19-API-download_all_utla.py
# and uk-covid19-API-download_all_nation.py
#
# using pygame
# this version graphs England, Scotland, Northern Ireland and Wales
# at the same time

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
font = pygame.font.SysFont('dejavusansmono', 48)
font2 = pygame.font.SysFont('dejavusans', 30)
font3 = pygame.font.SysFont('dejavusans', 12)
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
        



def generate_sine_wave_array4(freq_arr_all,
                             duration=0.5, wavefile = '', 
                             rest = 0.1, volume=0.5, sample_rate=44100,
                             quietmode=False):
    ''' Generate a tone at the given frequency.

        The sample rate should be at least double the frequency.
    '''
    # create one buffer for the whole array

    
    if not(quietmode):        
        for i, freq_arr in enumerate(freq_arr_all):
            allbuf = numpy.zeros((0,2), dtype=numpy.int16)
            for frequency in freq_arr:
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
            if i == 0:
                allbuf2 = allbuf
            else:
                allbuf2 = allbuf2 + allbuf
            sound = pygame.sndarray.make_sound(allbuf2)
    
    if not(quietmode):
        wfile = wave.open(wavefile, 'w')
        wfile.setframerate(sample_rate)
        wfile.setnchannels(2)
        wfile.setsampwidth(2)
        # write raw PyGame sound buffer to wave file
        wfile.writeframesraw(sound.get_raw())
        # play once      
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

def draw_graph_pygame(datelists, ncases_valslists, max_cases_all, area_l_all,
                      num_x, num_y):
    '''
    draw a line graph in a pygame window
    '''
    display_surf.fill(black)
    win_h = size[1]
    win_w = size[0]
    numareas = len(max_cases_all)
    k = 0
    
    win_h_i = win_h / num_x
    win_w_i = win_w / num_y
    
    while k < numareas:
        for i in range(num_x):
            for j in range(num_y):            
                img = font2.render(area_l_all[k], True, green, black)        
                display_surf.blit(img, (20+i*win_w_i, 20+j*win_h_i))    

                npoints = len(ncases_valslists[k])
                points = [[i*win_w_i,(j+1)*win_h_i]]
                #print(f"i,j = {i}, {j}. points = {points}")
                for r, (d, n) in enumerate(zip(datelists[k],
                                               ncases_valslists[k])):
                    x = int((r/npoints) * win_w_i)
                    y = int(win_h_i - (n/max_cases_all[k]) * win_h_i)
                    points.append([i*win_w_i + x, j*win_h_i + y])
                #print(f"i,j = {i}, {j}. points = {points}")
                pygame.draw.lines(display_surf, green, False, points, 3)
                k += 1
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
        
def overplot_fill_graph(datelists, ncases_valslists, caserate_lists,
                        max_cases_all, notetxt_arr_all, area_l_all, quietmode=False):
    '''
    overplot a fill for the line graph
    animated, delay to sync with sound
    and write text to annotate
    '''
    # note duration in seconds
    t = 0.5
    # height and width of window
    win_h = size[1]
    win_w = size[0]
    numareas = len(max_cases_all)
    k = 0
    pngfilecount = 0
    win_h_i = win_h / num_x
    win_w_i = win_w / num_y
    
    curtime = pygame.time.get_ticks()
    
    npoints = len(datelists[0])
    for q in range(npoints):
        for i in range(num_x):
            for j in range(num_y):
                k2 = 2*i + j
            
                print(area_l_all[k2], i, j)
                
                                                                                         
                # draw a vertical line
                x = int(i*win_w_i+((q/npoints) * win_w_i))
                y = int((j+1)*win_h_i - (ncases_valslists[k2][q]/max_cases_all[k2]) * win_h_i)
                # if its the first of the month
                if datelists[k2][q][-2:] == "01":
                    pygame.draw.line(display_surf, darkgreen, [x, (j+1)*win_h_i], [x, j*win_h_i], 1)
                    # write month
                    img = font3.render(datelists[k2][q][5:7], True, darkgreen, black)
                    display_surf.blit(img, (x+5, 5))
                print(f"area: {area_l_all[k2]}. date, cases: {datelists[k2][q]}, {ncases_valslists[k2][q]}")
                print(f"writing line from ({x}, {(j+1)*win_h_i}) to ({x}, {y})")
                pygame.draw.line(display_surf, choose_colour(caserate_lists[k2][q]), [x, (j+1)*win_h_i], [x, y], 4)
                # write date in pygame window
                img = font2.render(datelists[k2][q], True, green, black)        
                display_surf.blit(img, (i*win_w_i + 20, j*win_h_i + 70))
                    
                # write the musical note text
                musicnote = notetxt_arr_all[k2][q]
                try:
                    img = font.render(musicnote, True, green, black)
                except UnicodeError:
                    # the semiquaver in Unicode is U+1D161
                    # pygame doesn't seem to work with characters above FFFF
                    # replace with beamed semiquavers character
                    musicnote = musicnote.replace("𝅘𝅥𝅯", "♬")
                    img = font.render(musicnote, True, green, black)
                display_surf.blit(img, (i*win_w_i + 20,j*win_h_i + 120))

                # write number of cases on day
                if ncases_valslists[k2][q] == 1:
                    img = font2.render(f"{ncases_valslists[k2][q]:5} case  ", True, green, black)        
                else:
                    img = font2.render(f"{ncases_valslists[k2][q]:5} cases  ", True, green, black)        
                display_surf.blit(img, (i*win_w_i+200,j*win_h_i + 70))
    
                # write rate per 100k
                img = font2.render(f"{caserate_lists[k2][q]} /100k last 7 days  ", True, green, black)        
                display_surf.blit(img, (i*win_w_i+450,j*win_h_i+ 70))

                
        
                pygame.display.flip()
                # save png file
                # these can be converted to video using ffmpeg
                # hamelot.io/
                # visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video
                # print(t/min_duration)                        
                pngfile = os.path.join("graphfiles",
                           f"four_nations_{pngfilecount:05}.png")

                pygame.image.save(display_surf, pngfile)                 
        if k2+1 == numareas:               
            pngfilecount += 1
 
        curtime2 = pygame.time.get_ticks()
        # wait for the note duration, minus the time taken to execute the code
        if not(quietmode):
            pygame.time.wait(int(t*1000) - (curtime2-curtime))

def play_audio(cases_by_area, selected_areas, num_x, num_y, bass_octave = 3,
               range_octaves=4, scaling=1, shorttext=False, duration=1,
               quietmode=False):
    textout = ""   
    bass_note = 261.63 / (5-bass_octave)
    # one octave below middle C if bass-octave is its default
    textout += "bass note = {h} Hz\n".format(h=bass_note)
    textout += "scaling={s}. freq prop. to (cases/max cases)^scaling\n".format(
                s=scaling)
    startDate = datetime.datetime.fromisoformat("2020-02-01")
    datelists = []
    ncases_valslists = []
    caserate_lists = []
    max_cases_all = []
    area_l_all = []
    freq_arr_all = []
    notetxt_arr_all = []
    pygame.display.set_caption(
            f"SARS-CoV2 cases by specimen date in selected areas")    
    for area in sorted(selected_areas):
        textout_a = ""
        area_cases = sorted(cases_by_area[area], key=itemgetter(0))
        print(area, area_cases)        
        startDate_area = area_cases[0][0]
        endDate = area_cases[-1][0]
        startDate_area = datetime.datetime.fromisoformat(startDate_area)
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

        
        # find occurance of 1st case in the area
        #ncases_numpy = numpy.array(ncases_valslist, dtype=int)
        #firstnonzero = numpy.nonzero(ncases_numpy)[0][0]
        # remove part of array before 1st case in the area
        #datelist = datelist[firstnonzero:]
        #ncases_valslist = ncases_valslist[firstnonzero:]
        #caserate_list = caserate_list[firstnonzero:]
        
        # generate the frequencies and musical note texts
        freq_arr = []
        notetxt_arr = []
        for i, n in enumerate(zip(datelist, ncases_valslist, caserate_list)):
            # range of 4 octaves by default
            octaves = range_octaves*((n[1]/max_cases)**scaling)
            # quantise to the nearest semitone
            octaves = math.floor(octaves*12.0)/12.0
            # calculate frequency
            freq = bass_note*(2**octaves)        
            
            note = "♩ "
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
   
        textout_a += "\n\n"
        textout += textout_a
        print(textout_a)
        freq_arr_all.append(freq_arr)
        datelists.append(datelist)
        ncases_valslists.append(ncases_valslist)
        caserate_lists.append(caserate_list)
        max_cases_all.append(max_cases)
        area_l_all.append(area_l)
        notetxt_arr_all.append(notetxt_arr)
        
    # except if text only output, play sound and save it to a wavefile
    # if text only, just save it to file but don't play it
    # done by passing the value of quietmode to 
    # generate_sine_wave_array and overplot_fill_graph
    wavefile = "four_nations.wav"
    wavefile = os.path.join("audiofiles", wavefile)
    soundlength = generate_sine_wave_array4(freq_arr_all, 0.5,
                                           wavefile, quietmode=False)
    # draw the line graph for the areas
    draw_graph_pygame(datelists, ncases_valslists, max_cases_all, area_l_all,
                      num_x, num_y)                                                
    overplot_fill_graph(datelists, ncases_valslists,  caserate_lists,
                            max_cases_all, notetxt_arr_all, area_l_all,
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
                                                
    args = parser.parse_args()    
    
    # play the UK and nations cases, with square root scaling            
    cases_by_area = corona_python_text_csv_api.cases_by_country
    # print(cases_by_area)
    nations = ["Northern_Ireland", "Scotland", "Wales", "England"]
    num_x = 2
    num_y = 2
    notes_nations = play_audio(cases_by_area, nations, num_x, num_y, 2, 6, 0.5,
                               args.short, 0.5, args.quietmode)

    # play regions of England
    #cases_by_area = corona_python_text_csv_api.cases_by_region
    #notes_regions = play_audio(cases_by_area, "", 2, 6, 0.5,
    #                           args.short, 0.5, args.quietmode)
    # example selecting a region
    #notes_regions = play_audio(cases_by_area, "North_West", 2, 6, 0.5,
    #                           args.short, 0.5, args.quietmode)

    # play UTLAs
    #cases_by_area = corona_python_text_csv_api.cases_by_UTLA
    #notes_UTLAs = play_audio(cases_by_area, "", 3, 5, 0.5,
    #                         args.short, 0.5, args.quietmode)
    
    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(notes_nations)
            #output_file.write(notes_regions)
            #output_file.write(notes_UTLAs)

pygame.quit()
