#!/usr/bin/env python3

import itertools

number_of_pitches = 12
pitches_in_scale  = 5

full_scale   = list(range(0, number_of_pitches))

print(full_scale)
scales = itertools.combinations(full_scale,pitches_in_scale)

scales=list(scales)

for scale in scales:
    for interval in scale:
        if interval == 0:
            print(scale)
        
exit()
