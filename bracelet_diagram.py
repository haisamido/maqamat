#!/usr/bin/env python3

import math
import svgwrite
import numpy as np
    
# https://buildmedia.readthedocs.org/media/pdf/svgwrite/latest/svgwrite.pdf

cents_per_octave = 1200

output_file   ="bracelet.svg"
canvas_width  =600
canvas_height =600

r_note     =15  # note radius

r_bracelet =200 # radius of bracelet
cx = canvas_width/2
cy = canvas_height/2

cents = np.array([ 0.000, 111.731, 182.404, 315.641, 386.314, 498.045, 590.224, 609.776, 701.955, 813.686, 884.359, 1017.596, 1088.269])
#cents = np.array([0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0])
#cents = np.array([1, 16/15, 10/9, 6/5, 5/4, 4/3, 45/32, 64/45, 3/2, 8/5, 5/3, 9/5, 15/8, 2])

def create_canvas(output_file="bracelet.svg", canvas_width=600, canvas_height=600):
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
  
def main():

    dwg = create_canvas()
    
    add_bracelet_circle(dwg, stroke='red', fill=svgwrite.rgb(200, 200, 200), radius=250, stroke_width=.5 )
    add_bracelet_circle(dwg, stroke='black', stroke_width=.75)
    
    add_cent_tic_marks(dwg, stroke='blue',  radius=1.025*r_bracelet, interval=2)
    add_cent_tic_marks(dwg, stroke='red',   radius=1.05*r_bracelet,  interval=6)
    add_cent_tic_marks(dwg, stroke='green', stroke_width=.75, radius=1.075*r_bracelet,  interval=50)
        
    add_notes(dwg, stroke='red')
    
#    add_bracelet_circle(dwg, stroke='black', radius=250, stroke_width=.75)
        
    dwg.save()
    
if __name__ == "__main__":
    main()
