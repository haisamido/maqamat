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
import svgwrite

import yaml

from fractions import Fraction
from hashlib import sha256

maqamat_temp = yaml.safe_load(open('maqamat.yml'))
maqamat = yaml.safe_load(open('maqamat.yml'))['maqamat']

#intervals=maqamat['urmawi']['intervals']

# print(intervals)


parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('-f0','--f0', type=float, default=440, help='foo help')
parser.add_argument('-f1','--f1', type=float, default=440, help='foo help')
parser.add_argument('-c','--cents-per-octave', type=float, default=1200, help='cents per octave')
parser.add_argument('-o','--output-file', type=str, default='bracelet.svg', help='output name for svg file')

parser.add_argument('-E','--by-et',     action='store_true', default=True, help='by equal temperament')
parser.add_argument('-i','--intervals', type=float, default=12,  help='Number of equally tempered intervals')

parser.add_argument('-R','--by-ratios', action='store_true', default=False, help='providing scale by ratios')
parser.add_argument('-r','--ratios',    type=str,  default='[1/1, 253/243, 16/15, 10/9 , 9/8, 32/27, 6/5, 5/4, 81/64, 4/3, 27/20, 45/32, 729/512, 3/2, 128/81, 8/5, 5/3, 27/16, 16/9, 9/5, 15/8, 243/128, 2/1]', help='Scale by ratios')

parser.add_argument('-A','--generate-audio', action='store_true', default=False, help='Generate audio per interval')
parser.add_argument('-v','--volume',        type=float, default=1.75,  help='Audio volume')
parser.add_argument('-s','--sampling-rate', type=int,   default=44100, help='Audio sampling rate, Hz, must be integer')
parser.add_argument('-d','--duration',      type=float, default=.1,   help='Audio duration')

# SVG Canvas arguments for the bracelet diagram
parser.add_argument('-w','--canvas_width',  type=float, default=600,   help='Canvas Width')
parser.add_argument('-H','--canvas_height', type=float, default=600,   help='Canvas Height')

args = vars(parser.parse_args())

# Provided                    
f0                = args['f0']
f1                = args['f1']
cents_per_octave  = args['cents_per_octave']
#number_of_octaves = args['number_of_octaves']

canvas_width      = args['canvas_width']
canvas_height     = args['canvas_height']
output_file       = args['output_file']

r_note            =15  # note radius
r_bracelet        =200 # radius of bracelet

# Derived
radians_per_cent   = (2*math.pi)/cents_per_octave
degrees_per_radian = 360.0/(2*math.pi)

# Canvas
cx    = canvas_width/2
cy    = canvas_height/2
cents = np.array([])

# Audio section
generate_audio  = args['generate_audio']
volume          = args['volume']
sampling_rate   = args['sampling_rate']
duration        = args['duration']

# Canvas functions
#cents_per_octave = 1200

#output_file   ="bracelet.svg"
canvas_width  =600
canvas_height =600

r_note     =15  # note radius

r_bracelet =200 # radius of bracelet
cx = canvas_width/2
cy = canvas_height/2
stroke='red'
stroke_width=0.75

cents = np.array([])

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

def create_canvas(output_file=output_file, canvas_width=600, canvas_height=600):
    return svgwrite.Drawing(output_file, size=(canvas_width, canvas_height))
    
def add_bracelet_circle(obj='dwg', radius=r_bracelet, cx=canvas_width/2, cy=canvas_height/2, fill=svgwrite.rgb(140, 171, 255), stroke='white', stroke_width=.5):
    
    obj.add(
        obj.circle( 
            center=(cx,cy), 
            r=radius, 
            fill=fill,
            stroke=stroke, 
            stroke_width=stroke_width,
            id='bracelet'
        )
    )

def add_notes(obj='dwg', cents=cents, radius=r_bracelet, stroke='red', stroke_width=.75, cx=canvas_width/2, cy=canvas_height/2):
    
    theta =-1*math.pi/2
    i=0
    for cent in cents:
        step=(2*math.pi)*(cent/cents_per_octave)
        
        x = radius * math.cos(step) + cx
        y = radius * math.sin(step) + cy
        
        # https://math.stackexchange.com/a/814981
        𝑥rot=(math.cos(theta)*(x-cx) - math.sin(theta)*(y-cy) + cx)
        yrot=(math.sin(theta)*(x-cx) - math.cos(theta)*(y-cy) + cy)
        
        #print(i,cent,' x,y ---> ',x,y,' xrot, yrot ---> ',xrot,yrot)
        
        x=xrot
        y=yrot
        
        obj.add(
            obj.circle(
                center=(x,y),
                r=r_note,
                fill=svgwrite.rgb(0, 255, 0, '%'), 
                stroke=stroke, 
                stroke_width=stroke_width,
                id=cent
            )
        )

        obj.add(
            obj.line(
                (cx, cy), 
                (x, y), 
                stroke=svgwrite.rgb(10, 10, 16, '%'), 
                stroke_width='.2'
            )
        )
    
        i = i + 1
    
def add_cent_tic_marks(obj='dwg', radius=1.025*r_bracelet, interval=2, stroke='red', stroke_width=0.2):
    
    theta =-1*math.pi/2
    
    cents = []
    for i in range(0,cents_per_octave,interval):
        cents = np.append(cents, i)
    
    for cent in cents:
        step=(2*math.pi)*(cent/cents_per_octave)
        
        x = radius * math.cos(step) + cx
        y = radius * math.sin(step) + cy
        
        # dx0 = radius/0.975 * math.cos(step) + cx
        # dy0 = radius/0.975 * math.sin(step) + cy
        
        # dxf=x-dx0
        # dyf=y-dy0
        
        # https://math.stackexchange.com/a/814981
        𝑥rot=(math.cos(theta)*(x-cx) - math.sin(theta)*(y-cy) + cx)
        yrot=(math.sin(theta)*(x-cx) - math.cos(theta)*(y-cy) + cy)
        
        x=xrot
        y=yrot
        
        obj.add(
            obj.line(
                (cx, cy), 
                (x, y), 
                stroke=stroke, 
                stroke_width=stroke_width,
                id='tic_marks'
            )
        )
    
        i = i + 1

for maqam in sorted(maqamat):
    
    intervals = maqamat[maqam]['intervals']
    by        = maqamat[maqam]['metadata']['by']
    
    intervals_str = ','.join(map(str,intervals))
    intervals_str = f"[{intervals_str}]"
    
#    ratios               = re.sub(r"\s*,\s*", ",", intervals)
    scale_by_ratios  = np.array(eval(intervals_str))
#    print(scale_by_ratios)
#    scale_by_ratios = np.array((intervals))
#    print(scale_by_ratios)
    
    scale_by_cents       = cents_from_ratio(scale_by_ratios,cents_per_octave)
    scale_in_frequencies = frequency_from_ratio(f1,scale_by_ratios)
    number_of_intervals  = scale_by_cents.size
    limit_denominator    = (number_of_intervals-5)**5
    description          = f"maqam ={maqam}, type={by}"


# exit(0)

    # By Equal Temperament
    # if args['by_et'] is True:
    #     number_of_intervals  = args['intervals']
    #     cents_per_interval   = cents_per_octave/number_of_intervals
        
    #     scale_by_cents       = np.arange(0, cents_per_octave+cents_per_interval, cents_per_interval)
    #     scale_in_frequencies = frequency_from_cents(f1, scale_by_cents, cents_per_octave)
    #     number_of_intervals  = scale_by_cents.size
    #     limit_denominator    = number_of_intervals-1
    #     description          = f"Type=equal temperament intervals, Number of intervals={number_of_intervals-1}, keywords=TET,ET,EDO"

    # # By Ratios
    # if args['by_ratios'] is True:
    #     ratios               = re.sub(r"\s*,\s*", ",", args['ratios'])
    #     scale_by_ratios      = np.array(eval(ratios))
        
    #     # intervals=ratios
    #     # intervals_str =','.join(map(str,intervals))
    #     # intervals2    = f"[{intervals_str}]"
        
    #     # scale_by_ratios  = np.array(eval(intervals2))
    # #    print('scale by rations:  ', scale_by_ratios)
        
    #     scale_by_cents       = cents_from_ratio(scale_by_ratios,cents_per_octave)
    #     scale_in_frequencies = frequency_from_ratio(f1,scale_by_ratios)
    #     number_of_intervals  = scale_by_cents.size
    #     limit_denominator    = number_of_intervals**5
    #     description          = f"Type=intervals by ratios, Number of intervals={number_of_intervals-1}, keywords=ratios,just,pythogrean"

    scale_hash_value=(sha256(bytes(scale_by_cents)).hexdigest())

    arcs_per_cents = get_arcs_per_cents(scale_by_cents,cents_per_octave)

    frequency_ratios = scale_in_frequencies/f1

    delta_cents  = np.diff(scale_by_cents)
    delta_cents  = np.append(0, delta_cents)

    print()
    print("#-------------------------------------------------------------------------------------------------")
    print(f"# {description}")
    print("#-------------------------------------------------------------------------------------------------")
    print("%-4s %11s %11s  %-8s  %-16s %8s  %11s  %11s %12s" %("#", "cents", "Δ cents","f ratio", "ratio (derived)","fl ratio","abs error","rel error","f (Hz)"))
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

        print("%-4s %11.6f %11.6f  %8.6f  %-16s %8f  %11.8f  %11.8f  %11.6f" %(i,cent,delta_cents[i],f_ratio,fraction,fraction_float,aerror,rerror,f))
    #          ,arcs_per_cents[i],arcs_per_cents[i]*degrees_per_radian,arc_per_delta_cent,arc_per_delta_cent*degrees_per_radian))
        
        if generate_audio is True:
            generate_frequency(f)

    output_frequencies = [ 61.74, 82.41, 110.00, 146.83, 196.00, 261.63, 329.63, 392.00, 523.25 ]

    print("#-------------------------------------------------------------------------------------------------")

    # TODO: create SCL (scala file) output
    # for i, cent in enumerate(scale_by_cents):
    #     f       = scale_in_frequencies[i]
    #     f_ratio = frequency_ratios[i]

    #     fraction       = Fraction(f_ratio).limit_denominator(limit_denominator)
    #     derived_ratios = np.append(derived_ratios, f"{fraction}")
        
    #     fraction_float = float(fraction)
    #     fraction_delta_cents = Fraction(delta_cents[i]).limit_denominator(number_of_intervals)
        
    #     arc_per_delta_cent = delta_cents[i] * radians_per_cent

    #     # absolute error
    #     aerror    = f_ratio - float(fraction)
    #     # relative error
    #     rerror    = 100*(aerror)/f_ratio

    #    print("%8.6f" %(cent,))
    #          ,arcs_per_cents[i],arcs_per_cents[i]*degrees_per_radian,arc_per_delta_cent,arc_per_delta_cent*degrees_per_radian))
        
    #     if generate_audio is True:
    #         generate_frequency(f)
            
    # if args['by_ratios'] is True:
    #     given_ratios_str   = re.sub(",", ", ", ratios)
    # #    given_ratios_str = intervals_str
    #     given_ratios_str   = re.sub(r"\[|\]", "", given_ratios_str)
    #     print(f"# given   ratios: [{given_ratios_str}]")

        # m = hashlib.sha256(given_ratios_str.encode('UTF-8'))
        # print(m.hexdigest())

    derived_ratios_str = (', '.join(map(str, derived_ratios)))
    #print(sha256(derived_ratios_str).hexdigest())

    # m = hashlib.sha256(derived_ratios_str.encode('UTF-8'))
    # print(m.hexdigest())

    print(f"# derived ratios: [{derived_ratios_str}]")

    np.set_printoptions(precision=3,floatmode='fixed')
    #print(np.array(scale_by_cents))

    scale_by_cents_str = (', '.join(map(str, scale_by_cents)))

    print(f"# derived  cents: [{scale_by_cents_str}]")

    print(f"# derived  cents: sha256:{scale_hash_value}")
    print("#-------------------------------------------------------------------------------------------------")

    # Canvas section
    dwg=create_canvas(output_file=output_file, canvas_width=canvas_width, canvas_height=canvas_height)

    add_bracelet_circle(dwg, stroke='red', fill=svgwrite.rgb(200, 200, 200), radius=250, stroke_width=.5 )
    add_bracelet_circle(dwg, stroke='black', stroke_width=.75)

    add_cent_tic_marks(dwg, stroke='blue',  radius=1.025*r_bracelet, interval=2)
    add_cent_tic_marks(dwg, stroke='red',   radius=1.05*r_bracelet,  interval=6)
    add_cent_tic_marks(dwg, stroke='green', stroke_width=.75, radius=1.075*r_bracelet,  interval=50)

    add_notes(dwg, cents=scale_by_cents, radius=r_bracelet, stroke='red', stroke_width=.75, cx=cx, cy=cy)

    dwg.save()
