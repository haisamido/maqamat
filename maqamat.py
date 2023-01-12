#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np

def nth_root_of_2(n):
    return (2)**(1/n)

#
# Pitches
#
def frequency(f0,a,n):
    # https://pages.mtu.edu/~suits/NoteFreqCalcs.html
    # https://pages.mtu.edu/~suits/notefreqs.html
    # n = the number of half intervals away from the fixed note you are
    f = f0 * (a)**n
    return f

cents_in_octave   = 1200
TET_intervals     = np.array([12,24])
cents_in_interval = cents_in_octave/TET_intervals

print(nth_root_of_2(TET_intervals))
print(cents_in_interval)

tones = { 
    "cents":{ 
        200: { "interval":1,    "string":"1",   "tone_name":"tone" },
        100: { "interval":0.5,  "string":"1/2", "tone_name":"semi-tone" },
        50:  { "interval":0.25, "string":"1/4", "tone_name":"quarter-tone" }
    },
    "intervals":{
        1:    { "cents":200, "text":"1",     "tone_name":"tone" },
        1.5:  { "cents":300, "text":"1 1/2", "tone_name":"tone" },
        0.5:  { "cents":100, "text":"1/2",   "tone_name":"semi-ttone" },
        0.25: { "cents":50,  "text":"1/4",   "tone_name":"quarter-tone" },
        0.75: {},
        1.25: {}
    },
    "text_intervals" :{
        "1":1,
        "1/2":0.5,
        "1 1/4":1.25,
        "1 1/2":1.5,
        "3/4":0.75,
        "1/4":0.25
    }
}

print(tones)

jins = {
    "Ajam":{
        "cents": [200,200,100],
        "qarar": {},
        "hassas": {}
    },
    "Bayat":{
        "cents": [150,150,200],
        "qarar": {},
        "hassas": {}
    },
    "Hijaz":{},
    "Kurd":{},
    "Nawa-Athar":{},
    "Sikah":{},
    "Nahwand":{},
    "Rast":{},
    "Saba":{},
    "Zamzam":{},
    "Must'ar":{}
}

print(jins)

#print(jins'Ajam')