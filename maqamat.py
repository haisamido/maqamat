#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np

import wave
import time
import sys

import pyaudio

from fractions import Fraction

def nth_root_of_2(n):
    return (2)**(1/n)

def determine_frequency(f0, a, n):
    # https://pages.mtu.edu/~suits/NoteFreqCalcs.html
    # https://pages.mtu.edu/~suits/notefreqs.html
    # n = the number of half intervals away from the fixed note you are
    f = f0 * (a)**n
    return f

def cents_from_frequency(f1,f2,cents_per_octave):
    return cents_per_octave*math.log2(f2 / f1)

def frequency_from_cents(f1,cents,cents_per_octave):
    return f1*2**(cents/cents_per_octave)

def generate_frequency(f):
    p = pyaudio.PyAudio()

    volume   = 1.75  # range [0.0, 1.0]
    fs       = 44100  # sampling rate, Hz, must be integer
    duration = 0.2  # in seconds, may be float

    # generate samples, note conversion to float32 array
    
    p1 = np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)
    ph = p1
    
    samples = ( ph ).astype(np.float32)

    # per @yahweh comment explicitly convert to bytes sequence
    output_bytes = (volume * samples).tobytes()

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(
        format   = pyaudio.paFloat32,
        channels = 1,
        rate     = fs,
        output   = True
    )

    # play. May repeat with different volume values (if done interactively)
    start_time = time.time()
    stream.write(output_bytes)
   # print("Played sound for {:.2f} seconds".format(time.time() - start_time))

    stream.stop_stream()
    stream.close()
    p.terminate()

cents_per_octave   = 1200
TET_intervals      = 53
cents_per_interval = cents_per_octave/TET_intervals
f1                 = 220

scale_in_cents       = np.arange(0, cents_per_octave+cents_per_interval, cents_per_interval)
delta_cents          = np.diff(scale_in_cents)

scale_in_frequencies = frequency_from_cents(f1, scale_in_cents, cents_per_octave)
frequency_ratios     = scale_in_frequencies/f1

print("%s  %9s  %10s  %8s  %7s  %9s  %11s  %11s" %("#", "cents", "f (Hz)", "f/f1", "ratio","fl(ratio)","abs err","rel err (%)"))
print("--------------------------------------------------------------------------------")

for i, cent in enumerate(scale_in_cents):
    f       = scale_in_frequencies[i]
    f_ratio = frequency_ratios[i]
    
#    delta_cent = delta_cents[i]
    
    fraction       = Fraction(f_ratio).limit_denominator(4*TET_intervals)
    fraction_float = float(fraction)
    
    aerror         = f_ratio - float(fraction)
    rerror         = 100*(aerror)/f_ratio
    
    print("%2s  %8.3f  %10.6f  %8f  %7s  %9f  %11.8f  %11.8f" %(i,cent,f,f_ratio,fraction,fraction_float,aerror,rerror))
    generate_frequency(f)
