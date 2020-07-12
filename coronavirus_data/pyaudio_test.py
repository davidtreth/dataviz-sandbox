#!/usr/bin/python
# -*- coding: utf-8 -*-

import corona_python_text
import math
import numpy
import time
from operator import itemgetter
from pyaudio import PyAudio, paUInt8

# code partly copied from answers at https://stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound
 
def generate_sine_wave(frequency, duration, volume=0.2, sample_rate=22050):
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

    pa = PyAudio()
    stream = pa.open(
        format=paUInt8,
        channels=1,  # mono
        rate=sample_rate,
        output=True,
    )

    # make samples
    s = lambda i: volume * math.sin(2 * math.pi * frequency * i / sample_rate)
    samples = (int(s(i) * 0x7F + 0x80) for i in range(num_samples))

    # write several samples at a time
    for buf in zip( *([samples] * sample_rate) ):
        stream.write(bytes(buf))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * rest_frames)

    stream.stop_stream()
    stream.close()
    pa.terminate()

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

bass_note = 261.63 / 2 # one octave below middle C
notes = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
print("bass note = {h} Hz".format(h=bass_note))

#area = 'Cornwall and Isles of Scilly'
for area in sorted(corona_python_text.cases_by_utla):
    area_cases = sorted(corona_python_text.cases_by_utla[area], key=itemgetter(0))
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
    
    for n in zip(datelist, ncases_valslist):
        print("{d} {c} cases".format(d=n[0], c=n[1]))
        # range of 4 octaves
        octaves = n[1]*4/max_cases
        # quantise to the nearest semitone
        octaves = math.floor(octaves*12.0)/12.0
        # calculate frequency
        freq = bass_note*(2**octaves)
        print("{f:.3f} Hz, {n:.3f} octaves, {a}\n".format(f=freq, n=octaves, a=notes[int((octaves*12) % 12)]))
        generate_sine_wave(
        # see http://www.phy.mtu.edu/~suits/notefreqs.html
            frequency=float(freq),   # Hz, waves per second C6
            duration=1.0,       # seconds to play sound
            volume=0.25,        # 0..1 how loud it is
            sample_rate=22050,  # number of samples per second: 11025, 22050, 44100
        )
        


