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
import corona_python_text_csv_api 

# code partly copied from answers at
# stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound
# saving to file: https://github.com/esdalmaijer/Save_PyGame_Sound

size = (1920, 1080)
bits = 16
green = (  0, 255,  0)
black = (  0,   0,  0)
pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
font = pygame.font.SysFont('dejavusansmono', 96)
font2 = pygame.font.SysFont('dejavusans', 60)
     
def generate_sine_wave(frequency, duration, volume=0.5, sample_rate=44100):
    ''' Generate a tone at the given frequency.

        Limited to unsigned 8-bit samples at a given sample_rate.
        The sample rate should be at least double the frequency.
    '''
    if sample_rate < (frequency * 2):
        print('Warning: sample_rate must be at least double the frequency '
              f'to accurately represent it:\n    sample_rate {sample_rate}'
              f' ≯ {frequency*2} (frequency {frequency}*2)')
    num_samples = int(sample_rate * duration)
    rest_frames = num_samples % sample_rate

    # make samples
    buf = numpy.zeros((num_samples + rest_frames, 2), dtype=numpy.int16)
    max_sample = 2**(bits-1) - 1    
    s = lambda i: volume * max_sample * math.sin(2 * math.pi * frequency * i / sample_rate)
    for k in range(num_samples):
        buf[k][0] = s(k)*((num_samples-k)/num_samples)
        buf[k][1] = s(k)*((num_samples-k)/num_samples)
    sound = pygame.sndarray.make_sound(buf)
    #play once
    sound.play()
    time.sleep(duration)
        



def generate_sine_wave_array(freq_arr, duration_arr, wavefile = '', rest = 0.1, volume=0.5, sample_rate=44100):
    ''' Generate a tone at the given frequency.

        Limited to unsigned 8-bit samples at a given sample_rate.
        The sample rate should be at least double the frequency.
    '''
    allbuf = numpy.zeros((0,2), dtype=numpy.int16)    
    for frequency, duration in zip(freq_arr, duration_arr):
        if sample_rate < (frequency * 2):
            print('Warning: sample_rate must be at least double the frequency '
                  f'to accurately represent it:\n    sample_rate {sample_rate}'
                  f' ≯ {frequency*2} (frequency {frequency}*2)')
        num_samples = int(sample_rate * duration*(1-rest))      
        rest_frames = int(duration*rest*sample_rate)# + ((sample_rate - num_samples) % sample_rate)
        
        # make samples
        buf = numpy.zeros((num_samples + rest_frames, 2), dtype=numpy.int16)
        max_sample = 2**(bits-1) - 1 
        s = lambda i: volume * max_sample * math.sin(2 * math.pi * frequency * i / sample_rate)
        for k in range(num_samples):
            buf[k][0] = s(k)*((num_samples-k)/num_samples)
            buf[k][1] = s(k)*((num_samples-k)/num_samples)
        allbuf = numpy.vstack((allbuf, buf))
    sound = pygame.sndarray.make_sound(allbuf)
    
    if wavefile != '':
        wfile = wave.open(wavefile, 'w')
        wfile.setframerate(sample_rate)
        wfile.setnchannels(2)
        wfile.setsampwidth(2)
        # write raw PyGame sound buffer to wave file
        wfile.writeframesraw(sound.get_raw())
    #play once        
    sound.play()        
    #time.sleep(sound.get_length())
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


notes = ["C ", "C♯", "D ", "E♭", "E ", "F ", "F♯", "G ", "A♭", "A ", "B♭", "B "]

def draw_graph_pygame(datelist, ncases_valslist, max_cases, area):
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
        
def overplot_fill_graph(datelist, ncases_valslist, max_cases, duration_arr, notetxt_arr):
    win_h = size[1]
    win_w = size[0]
    npoints = len(ncases_valslist)
    for i, (d, n, t, m) in enumerate(zip(datelist, ncases_valslist, duration_arr, notetxt_arr)):
        curtime = pygame.time.get_ticks()
        x = int((i/npoints) * win_w)    
        y = int(win_h - (n/max_cases) * win_h)
        pygame.draw.line(display_surf, green, [x, win_h], [x, y], 8)
        img = font2.render(d, True, green, black)        
        display_surf.blit(img, (20, 120))
        
        musicnote = m
        try:
            img = font.render(musicnote, True, green, black)
        except UnicodeError:
            img = font.render(musicnote[0:3], True, green, black)
        display_surf.blit(img, (20, 220))
        #print(d)
        img = font2.render(f"{n:5} cases  ", True, green, black)        
        display_surf.blit(img, (500, 120))
        pygame.display.flip()
        curtime2 = pygame.time.get_ticks()
        pygame.time.wait(int(t*1000) - (curtime2-curtime))

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
        area_l = area.replace("_", " ")
        pygame.display.set_caption(f"SARS-CoV2 cases by specimen date in {area_l}")

        
        draw_graph_pygame(datelist, ncases_valslist, max_cases, area_l)
        
        freq_arr = []
        duration_arr = []
        notetxt_arr = []
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
                note = "♩ "
            elif duration_2 == duration/2:
                note = "♪ "
            elif duration_2 == duration/4:
                note = "𝅘𝅥𝅯 "
            else:
                note = "♫ "
            if shorttext:
                notetxt = "{a}{b}{s}".format(
                    a=notes[int((octaves*12) % 12)],
                    b=int(bass_octave+math.floor(octaves)), s=note)
                textout_a += notetxt
                if ((i+1) % 14 == 0 and i > 0):
                    textout_a += "\n"
            else:
                notetxt = ("{d} {c} cases, {f:.3f} Hz, "
                              "{n:.3f} octaves, {a}{b}{s}\n").format(
                              d=n[0], c=n[1], f=freq, n=octaves,
                              a=notes[int((octaves*12) % 12)],
                              b=int(bass_octave+math.floor(octaves)),s=note)
                textout_a += notetxt
            notetxt_arr.append(notetxt)
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
            wavefile = area.lower().replace(",","") + ".wav"
            wavefile = os.path.join("audiofiles", wavefile)
            soundlength = generate_sine_wave_array(freq_arr, duration_arr, wavefile)
            #soundlength = generate_sine_wave_array(freq_arr, duration_arr, wavefile='')
            overplot_fill_graph(datelist, ncases_valslist, max_cases, duration_arr, notetxt_arr)
            #time.sleep(3)        
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
                               args.short, 0.5, args.textonly)

    # play regions of England	
    cases_by_area = corona_python_text_csv_api.cases_by_region
    notes_regions = play_audio(cases_by_area, "", 3, 5, 0.5,
                               args.short, 0.5, args.textonly)

    # play UTLAs
    cases_by_area = corona_python_text_csv_api.cases_by_UTLA
    notes_UTLAs = play_audio(cases_by_area, "", 3, 5, 0.5,
                             args.short, 0.5, args.textonly)

    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(notes_nations)
            output_file.write(notes_regions)
            output_file.write(notes_UTLAs)

pygame.quit()
