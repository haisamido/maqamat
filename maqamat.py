#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np
import argparse

import wave
import time
import sys

import pyaudio

from fractions import Fraction

parser = argparse.ArgumentParser()
parser.add_argument('-f0','--f0', type=float, default=440, help='foo help')
parser.add_argument('-f1','--f1', type=float, default=220, help='foo help')
parser.add_argument('-c','--cents-per-octave',  type=float, default=1200, help='cents per octave')
parser.add_argument('-o','--number-of-octaves', type=float, default=1, help='number of octaves')

parser.add_argument('-e','--by-et',        type=bool, default=True,  help='by equal temparement')
parser.add_argument('-i','--et-intervals', type=float, default=12,  help='Number of equally tempered intervals')

parser.add_argument('-R','--by-ratios', type=bool, default=False, help='providing scale by ratios')
parser.add_argument('-r','--ratios',    type=str,  default=[1/1, 253/243, 16/15, 10/9 , 9/8, 32/27, 6/5, 5/4, 81/64, 4/3, 27/20, 45/32, 729/512, 3/2, 128/81, 8/5, 5/3, 27/16, 16/9, 9/5, 15/8, 243/128, 2/1], help='Scale by ratios')

parser.add_argument('-l','--limit-denominator-factor', type=int, default=5, help='Limit denominator to calculate ratios')

args = vars(parser.parse_args())

f0                = args['f0']
f1                = args['f1']
cents_per_octave  = args['cents_per_octave']
number_of_octaves = args['number_of_octaves']

limit_denominator_factor = args['limit_denominator_factor']

by_et              = args['by_et']
et_intervals       = args['et_intervals']
cents_per_interval = cents_per_octave/et_intervals

by_ratios       = args['by_ratios']
scale_by_ratios = np.array(args['ratios'])

def nth_root_of_2(n):
    return (2)**(1/n)

def determine_frequency(f0, a, n):
    # https://pages.mtu.edu/~suits/NoteFreqCalcs.html
    # https://pages.mtu.edu/~suits/notefreqs.html
    # n = the number of half intervals away from the fixed note you are
    f = f0 * (a)**n
    return f

def cents_from_frequency(f1,f2,cents_per_octave):
    return cents_per_octave*np.log2(f2 / f1)

def frequency_from_cents(f1,cents,cents_per_octave):
    return f1*2**(cents/cents_per_octave)

def frequency_from_ratio(f1,f_ratio):
    return f1*f_ratio

def cents_from_ratio(f_ratio,cents_per_octave):
    return cents_per_octave*np.log2(f_ratio)

def generate_scale_by_et():
    return 0

def derive_scale_by_ratios():
    return 0    
        
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

    
if by_et is True:
    scale_by_cents       = np.arange(0, cents_per_octave+cents_per_interval, cents_per_interval)
    scale_in_frequencies = frequency_from_cents(f1, scale_by_cents, cents_per_octave)
    intervals            = scale_by_cents.size
    limit_denominator    = intervals-1

if by_ratios is True:
    scale_by_cents       = cents_from_ratio(scale_by_ratios,cents_per_octave)
    scale_in_frequencies = frequency_from_ratio(f1,scale_by_ratios)
    intervals            = scale_by_cents.size
    limit_denominator    = intervals*intervals

print(by_et)
print(by_ratios)

frequency_ratios = scale_in_frequencies/f1
delta_cents      = np.diff(scale_by_cents)

print("%s  %9s  %10s  %8s  %7s  %9s  %11s  %11s" %("#", "cents", "f (Hz)", "f/f1", "ratio","fl(ratio)","abs err","rel err (%)"))
print("--------------------------------------------------------------------------------")

for i, cent in enumerate(scale_by_cents):
    f       = scale_in_frequencies[i]
    f_ratio = frequency_ratios[i]

    fraction       = Fraction(f_ratio).limit_denominator(limit_denominator)
    fraction_float = float(fraction)
    
    aerror         = f_ratio - float(fraction)
    rerror         = 100*(aerror)/f_ratio
    
    print("%2s  %8.3f  %10.6f  %8f  %7s  %9f  %11.8f  %11.8f" %(i,cent,f,f_ratio,fraction,fraction_float,aerror,rerror))
#    generate_frequency(f)
