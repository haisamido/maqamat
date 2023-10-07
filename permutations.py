#!/usr/bin/env python3

import itertools

number_of_pitches = 12
pitches_in_scale  = 3

chromatic_scale   = list(range(0, number_of_pitches))

print(chromatic_scale)
print(number_of_pitches,pitches_in_scale)

pitch_classes = itertools.combinations(chromatic_scale,pitches_in_scale)
# Convert to list
pitch_classes = list(pitch_classes)

print()
for pitch_class in pitch_classes:
    for interval in pitch_class:
        if interval == 0:
            print(pitch_class)
        
exit()
