#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
import re
import hashlib

import wave
import time
import sys

import pyaudio

from fractions import Fraction
from hashlib import sha256

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('-f0','--f0', type=float, default=440, help='foo help')
parser.add_argument('-f1','--f1', type=float, default=440, help='foo help')
parser.add_argument('-c','--cents-per-octave',  type=float, default=1200, help='cents per octave')
parser.add_argument('-o','--number-of-octaves', type=float, default=1, help='number of octaves')

parser.add_argument('-E','--by-et',     action='store_true', default=True, help='by equal temparement')
parser.add_argument('-i','--intervals', type=float, default=12,  help='Number of equally tempered intervals')

parser.add_argument('-R','--by-ratios', action='store_true', default=False, help='providing scale by ratios')
parser.add_argument('-r','--ratios',    type=str,  default='[1/1, 253/243, 16/15, 10/9 , 9/8, 32/27, 6/5, 5/4, 81/64, 4/3, 27/20, 45/32, 729/512, 3/2, 128/81, 8/5, 5/3, 27/16, 16/9, 9/5, 15/8, 243/128, 2/1]', help='Scale by ratios')

parser.add_argument('-A','--generate-audio', action='store_true', default=False, help='Generate audio per interval')
parser.add_argument('-v','--volume',        type=float, default=1.75,  help='Audio volume')
parser.add_argument('-s','--sampling-rate', type=int,   default=44100, help='Audio sampling rate, Hz, must be integer')
parser.add_argument('-d','--duration',      type=float, default=1.0,   help='Audio duration')

args = vars(parser.parse_args())
                    
f0                = args['f0']
f1                = args['f1']
cents_per_octave  = args['cents_per_octave']
number_of_octaves = args['number_of_octaves']

# Audio section
generate_audio  = args['generate_audio']
volume          = args['volume']
sampling_rate   = args['sampling_rate']
duration        = args['duration']

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

# {0,1,3,5,6,7,9,11}

# (101011101011)₂ = (1 × 2¹¹) + (0 × 2¹⁰) + (1 × 2⁹) + (0 × 2⁸) + (1 × 2⁷) + (1 × 2⁶) + (1 × 2⁵) + (0 × 2⁴) + (1 × 2³) + (0 × 2²) + (1 × 2¹) + (1 × 2⁰) = (2795)₁₀

radians_per_cent   = (2*math.pi)/cents_per_octave
degrees_per_radian = 360.0/(2*math.pi)

def get_arcs_per_cents(scale_by_cents,cents_per_octave):
    
    arcs_per_cents =np.array([])
    
    for i, cent in enumerate(scale_by_cents):
        radian_at_cent = radians_per_cent * scale_by_cents[i]
        arcs_per_cents = np.append(arcs_per_cents, radian_at_cent)

    return arcs_per_cents
    
def generate_frequency(f):
    p = pyaudio.PyAudio()
    
    # generate samples, note conversion to float32 array
    
    p1 = np.sin(2 * np.pi * np.arange(sampling_rate * duration) * f / sampling_rate)
    ph = p1
    
    samples = ( ph ).astype(np.float32)

    # per @yahweh comment explicitly convert to bytes sequence
    output_bytes = (volume * samples).tobytes()

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(
        format   = pyaudio.paFloat32,
        channels = 1,
        rate     = sampling_rate,
        output   = True
    )

    # play. May repeat with different volume values (if done interactively)
    start_time = time.time()
    stream.write(output_bytes)
   # print("Played sound for {:.2f} seconds".format(time.time() - start_time))

    stream.stop_stream()
    stream.close()
    p.terminate()

# By Equal Tempermant
if args['by_et'] is True:
    number_of_intervals  = args['intervals']
    cents_per_interval   = cents_per_octave/number_of_intervals
    
    scale_by_cents       = np.arange(0, cents_per_octave+cents_per_interval, cents_per_interval)
    scale_in_frequencies = frequency_from_cents(f1, scale_by_cents, cents_per_octave)
    number_of_intervals  = scale_by_cents.size
    limit_denominator    = number_of_intervals-1
    description          = f"Type=equal temperament intervals, Number of intervals={number_of_intervals-1}, keywords=TET,ET,EDO"

# By Ratios
if args['by_ratios'] is True:
    ratios               = re.sub("\s*,\s*", ",", args['ratios'])
    scale_by_ratios      = np.array(eval(ratios))
    
    scale_by_cents       = cents_from_ratio(scale_by_ratios,cents_per_octave)
    scale_in_frequencies = frequency_from_ratio(f1,scale_by_ratios)
    number_of_intervals  = scale_by_cents.size
    limit_denominator    = number_of_intervals**5
    description          = f"Type=intervals by ratios, Number of intervals={number_of_intervals-1}, keywords=ratios,just,pythogrean"

scale_hash_value=(sha256(bytes(scale_by_cents)).hexdigest())

arcs_per_cents = get_arcs_per_cents(scale_by_cents,cents_per_octave)

frequency_ratios = scale_in_frequencies/f1

delta_cents  = np.diff(scale_by_cents)
delta_cents  = np.append(0, delta_cents)

#print(f"## {description}\n")
#print('```bash')
print()
print("#-------------------------------------------------------------------------------------------------")
print(f"# {description}")
print("#-------------------------------------------------------------------------------------------------")
print("%-4s %8s %8s  %-8s  %-16s %8s  %11s  %11s %12s" %("#", "cents", "Δ cents","f ratio", "ratio (derived)","fl ratio","aerror","rerror","f (Hz)"))
print("#-------------------------------------------------------------------------------------------------")

derived_ratios =np.array([])

for i, cent in enumerate(scale_by_cents):
    f       = scale_in_frequencies[i]
    f_ratio = frequency_ratios[i]

    fraction       = Fraction(f_ratio).limit_denominator(limit_denominator)
    derived_ratios = np.append(derived_ratios, f"{fraction}")
    
    fraction_float = float(fraction)
    fraction_delta_cents = Fraction(delta_cents[i]).limit_denominator(number_of_intervals)
    
    arc_per_delta_cent = delta_cents[i] * radians_per_cent

    # absolute error
    aerror    = f_ratio - float(fraction)
    # relative error
    rerror    = 100*(aerror)/f_ratio

    print("%-4s %8.3f %8.3f  %8.6f  %-16s %8f  %11.8f  %11.8f  %11.6f" %(i,cent,delta_cents[i],f_ratio,fraction,fraction_float,aerror,rerror,f))
#          ,arcs_per_cents[i],arcs_per_cents[i]*degrees_per_radian,arc_per_delta_cent,arc_per_delta_cent*degrees_per_radian))
    
    if generate_audio is True:
        generate_frequency(f)

print("#-------------------------------------------------------------------------------------------------")

if args['by_ratios'] is True:
    given_ratios_str   = re.sub(",", ", ", ratios)
    given_ratios_str   = re.sub("\[|\]", "", given_ratios_str)
    print(f"# given   ratios: [{given_ratios_str}]")

    # m = hashlib.sha256(given_ratios_str.encode('UTF-8'))
    # print(m.hexdigest())

derived_ratios_str = (', '.join(map(str, derived_ratios)))
#print(sha256(derived_ratios_str).hexdigest())

# m = hashlib.sha256(derived_ratios_str.encode('UTF-8'))
# print(m.hexdigest())

print(f"# derived ratios: [{derived_ratios_str}]")


np.set_printoptions(precision=3,floatmode='fixed')
print(np.array(scale_by_cents))

scale_by_cents_str = (', '.join(map(str, scale_by_cents)))

print(f"# derived  cents: [{scale_by_cents_str}]")

print(f"# derived  cents: sha256:{scale_hash_value}")
print("#-------------------------------------------------------------------------------------------------")

#print('```')