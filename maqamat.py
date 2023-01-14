#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np


def nth_root_of_2(n):
    return (2)**(1/n)

#
# Pitches
#


def frequency(f0, a, n):
    # https://pages.mtu.edu/~suits/NoteFreqCalcs.html
    # https://pages.mtu.edu/~suits/notefreqs.html
    # n = the number of half intervals away from the fixed note you are
    f = f0 * (a)**n
    return f


cents_in_octave = 1200
# Equally Tempered Intervals
TET_intervals = np.array([12, 24])
cents_in_interval = cents_in_octave/TET_intervals

# print(nth_root_of_2(TET_intervals))
# print(cents_in_interval)

tones = {
    "cents": {
        200: {"interval": 1,    "string": "1",   "tone_name": "tone"},
        100: {"interval": 0.5,  "string": "1/2", "tone_name": "semi-tone"},
        50:  {"interval": 0.25, "string": "1/4", "tone_name": "quarter-tone"}
    },
    "intervals": {
        1:    {"cents": 200, "text": "1",     "tone_name": "tone"},
        1.5:  {"cents": 300, "text": "1 1/2", "tone_name": "tone"},
        0.5:  {"cents": 100, "text": "1/2",   "tone_name": "semi-ttone"},
        0.25: {"cents": 50,  "text": "1/4",   "tone_name": "quarter-tone"},
        0.75: {},
        1.25: {}
    },
    "text_intervals": {
        "1": 1,
        "1/2": 0.5,
        "1 1/4": 1.25,
        "1 1/2": 1.5,
        "3/4": 0.75,
        "1/4": 0.25
    }
}

# print(tones)

frequencies = {
    "D4": 293.665
}

jins = {
    "Ajam": {
        "cents": [200, 200, 100],
        "qarar": {},
        "hassas": {}
    },
    "Bayat": {
        "cents": [150, 150, 200],
        "qarar": {},
        "tonics": ["D4", "G4", "A4", "E4", "C4"],
        "modulation_from_ghammaz": ["Nahwand", "Rast", "Hijaz"],
        "hassas": {}
    },
    "Hijaz": {},
    "Kurd": {},
    "Nawa-Athar": {},
    "Sikah": {},
    "Nahwand": {
        "cents": [200, 100, 200],
        "qarar": {},
        "hassas": {}},
    "Rast": {},
    "Saba": {},
    "Zamzam": {},
    "Must'ar": {}
}

maqam_def = {
    "Bayat": {"tonic": "D4", "ajnas": ["Bayat", "Nahwand"]} 
}

#print(maqam['Bayat']['ajnas'])

i=0
maqam_argv='Bayat'

for key in maqam_def[maqam_argv]['ajnas']:
    l=len(jins[key]['cents'])
    if i == 0:
        maqam = np.array(jins[key]['cents'])
    else:
        maqam = np.append(maqam,jins[key]['cents'][1:l])
    i=i+1

def cents_from_frequency(f1,f2,cents_in_octave):
    return cents_in_octave*math.log2(f2 / f1)

def frequency_from_cents(f1,cents,cents_in_octave):
    return f1*math.exp(cents/cents_in_octave)

#f2=frequency_from_cents(110,0,1200)

#print(frequency_from_cents(293.665,200,1200))
print(cents_from_frequency(293.665,329.628 ,1200))

c=0
cu=np.array([c])

for key in maqam:
    c=c+key
    cu=np.append(cu,c)

maqam_def[maqam_argv].update({ "cents":cu })

# print(cu)

#print(maqam_def[maqam_argv]['cents'])

f1=293.665
# E4 = 329.628 
for cent in maqam_def[maqam_argv]['cents']:
  print(cent,frequency_from_cents(f1,cent,cents_in_octave))