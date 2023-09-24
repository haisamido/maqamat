#!/usr/bin/env python3

import itertools

intervals    = 12
scale_length = 6

chromatic_scale = list(range(0, intervals+1))

print(chromatic_scale)
scales = itertools.combinations(chromatic_scale,scale_length)

scales=list(scales)

for scale in scales:
    for interval in scale:
        if interval == 0:
            print(scale)
        
exit()
