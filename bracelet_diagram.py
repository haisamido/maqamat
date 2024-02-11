#!/usr/bin/env python3

import math
import svgwrite
import numpy as np
    
# https://buildmedia.readthedocs.org/media/pdf/svgwrite/latest/svgwrite.pdf
def main():
    
    canvas_width  =600
    canvas_height =600
    
    dwg = svgwrite.Drawing('bracelet.svg', size=(canvas_width, canvas_height))
    
    #
    pitches_per_octave   = 24
    cents_per_octave     = 1200
    intervals_per_octave = pitches_per_octave -1
    
    cents_per_interval = cents_per_octave/(pitches_per_octave)
    stepSize           = (360/(pitches_per_octave))*(math.pi/180)
    
    i          =0
    r_note     =15  # note radius 
    r_bracelet =200 # radius of bracelet

    cx = canvas_width/2
    cy = canvas_height/2
      
    dwg.add(
        dwg.circle( 
            center=(cx,cy), 
            r=r_bracelet, 
            fill=svgwrite.rgb(140, 171, 255), 
            id='bracelet'
        )
    )

    t = 0 #radians
    
    note={}
    cents = np.array([ 0.000, 111.731, 182.404, 315.641, 386.314, 498.045, 590.224, 609.776, 701.955, 813.686, 884.359, 1017.596, 1088.269])
#    cents = np.array([ 0.000, 300.0, 450, 600.0, 900.0])

    i=0
    theta=-1*math.pi/2
    
    for cent in cents:
        step=(2*math.pi)*(cent/1200)
        
        x = r_bracelet* math.cos(step) + cx
        y = r_bracelet* math.sin(step) + cy
        
        # https://math.stackexchange.com/a/814981
        𝑥rot=(math.cos(theta)*(x-cx) - math.sin(theta)*(y-cy) + cx)
        yrot=(math.sin(theta)*(x-cx) - math.cos(theta)*(y-cy) + cy)
        
        print(i,cent,' x,y ---> ',x,y,' xrot, yrot ---> ',xrot,yrot)
        
        x=xrot
        y=yrot
        
        # x_text = 1.2*r_bracelet* math.cos(step) + cx
        # y_text = 1.2*r_bracelet* math.sin(step) + cy
        
        dwg.add(
            dwg.circle(
                center=(x,y),
                r=r_note,
                fill=svgwrite.rgb(0, 255, 0), 
                stroke='green', 
                stroke_width='2',
                id=cent
            )
        )

        dwg.add(
            dwg.line(
                (cx, cy), 
                (x, y), 
                stroke=svgwrite.rgb(10, 10, 16, '%'), 
                stroke_width='.2'
            )
        )
        
        # dwg.add(
        #     dwg.circle(
        #         center=(x_text, y_text),
        #         r=r_note,
        #         fill=svgwrite.rgb(255, 0, 255, '%'),
        #         stroke='black',
        #         stroke_width='2'
        #     )
        # )
        
        i = i + 1

    i=0
    dwg.save()
    
if __name__ == "__main__":
    main()
