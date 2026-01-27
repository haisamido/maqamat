#!/usr/bin/env python3

import os
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
import re
import hashlib

import subprocess
import shutil
import wave
import time
import sys

import pyaudio
import svgwrite

import yaml

from fractions import Fraction
from hashlib import sha256

np.set_printoptions(precision=3, suppress=True, linewidth=np.inf)

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('-m','--maqamat-file', type=str, default='maqamat.yml', help='YAML file defining maqamat scales')
parser.add_argument('-M','--maqam',        type=str, default=None, help='Generate a specific maqam by name (default: all)')
parser.add_argument('-f0','--f0', type=float, default=440, help='foo help')
parser.add_argument('-f1','--f1', type=float, default=440, help='foo help')
parser.add_argument('-c','--cents-per-octave', type=float, default=1200, help='cents per octave')
parser.add_argument('-o','--output-file', type=str, default='bracelet.svg', help='output name for svg file')

parser.add_argument('-E','--by-et',     action='store_true', default=True, help='by equal temperament')
parser.add_argument('-i','--intervals', type=float, default=12,  help='Number of equally tempered intervals')

parser.add_argument('-R','--by-ratios', action='store_true', default=False, help='providing scale by ratios')
parser.add_argument('-r','--ratios',    type=str,  default='[1/1, 253/243, 16/15, 10/9 , 9/8, 32/27, 6/5, 5/4, 81/64, 4/3, 27/20, 45/32, 729/512, 3/2, 128/81, 8/5, 5/3, 27/16, 16/9, 9/5, 15/8, 243/128, 2/1]', help='Scale by ratios')

parser.add_argument('-S','--generate-scl',   action='store_true', default=False, help='Generate Scala .scl tuning files')
parser.add_argument('-V','--verbose',        action='store_true', default=False, help='Verbose output to console')
parser.add_argument('-A','--generate-audio', action='store_true', default=False, help='Generate audio per interval')
parser.add_argument('-v','--volume',        type=float, default=1.75,  help='Audio volume')
parser.add_argument('-s','--sampling-rate', type=int,   default=44100, help='Audio sampling rate, Hz, must be integer')
parser.add_argument('-d','--duration',      type=float, default=.1,   help='Audio duration')

# SVG Canvas arguments for the bracelet diagram
parser.add_argument('-w','--canvas_width',  type=float, default=600,   help='Canvas Width')
parser.add_argument('-H','--canvas_height', type=float, default=600,   help='Canvas Height')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

args = vars(parser.parse_args())

maqamat = yaml.safe_load(open(args['maqamat_file']))

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

# Scala section
generate_scl    = args['generate_scl']

# Verbosity
verbose         = args['verbose']

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

def tee(line, lines_list):
    if verbose:
        print(line)
    lines_list.append(line)

def create_scala_file(scale_by_cents, description, filename):
    """Create a Scala .scl file from a scale defined in cents.

    The SCL format omits the implicit 1/1 unison (0 cents), so pitch values
    are written starting from the second degree through the octave.

    See: https://www.huygens-fokker.org/scala/scl_format.html
    """
    number_of_notes = len(scale_by_cents) - 1  # exclude the implicit 1/1

    lines = []
    lines.append(f"! {filename}")
    lines.append("!")
    lines.append(description)
    lines.append(f" {number_of_notes}")
    lines.append("!")
    for cent in scale_by_cents[1:]:
        lines.append(f" {cent:.6f}")

    with open(filename, 'w') as f:
        f.write('\n'.join(lines))
        f.write('\n')

def create_readme_file(maqam, metadata, intervals, number_of_intervals, by, derived_ratios_str, scale_by_cents_str, scale_hash_value, output_dir, generate_scl, maqamat_data, maqamat_file, tsv_lines):
    """Create a README.md in the maqam output directory."""
    source  = metadata.get('source', '')
    page    = metadata.get('page', '')
    comment = metadata.get('comment', '')
    maqamat_file_rel = os.path.relpath(maqamat_file, output_dir)

    lines = []
    lines.append(f"# {maqam}")
    lines.append("")
    if comment:
        lines.append(comment)
        lines.append("")

    lines.append(f"Data source: [{os.path.basename(maqamat_file)}]({maqamat_file_rel})")
    lines.append("")

    # Scale properties
    lines.append("## Scale properties")
    lines.append("")
    lines.append(f"- **Type**: {by}")
    lines.append(f"- **Number of intervals**: {number_of_intervals}")
    if by in ('et', 'tet', 'edo'):
        lines.append(f"- **Equal divisions of the octave**: {number_of_intervals}")
    else:
        intervals_str = ', '.join(map(str, intervals))
        lines.append(f"- **Intervals**: [{intervals_str}]")
    lines.append("")

    # Source
    if source:
        lines.append("## Source")
        lines.append("")
        lines.append(f"- **Reference**: {source}")
        if page:
            lines.append(f"- **Page**: {page}")
        lines.append("")

        # Bibliography lookup
        bib = maqamat_data.get('bibliography', {})
        if source in bib:
            entry = bib[source]
            author    = entry.get('author', '')
            title     = entry.get('title', '')
            publisher = entry.get('publisher', '')
            year      = entry.get('year', '')
            lines.append("### Bibliography")
            lines.append("")
            lines.append(f"> {author}. *{title}*. {publisher}, {year}.")
            lines.append("")

    # Derived data
    lines.append("## Derived data")
    lines.append("")
    lines.append("```yaml")
    lines.append(f"derived_ratios: [{derived_ratios_str}]")
    lines.append(f"cents: [{scale_by_cents_str}]")
    lines.append(f"sha256: {scale_hash_value}")
    lines.append("```")
    lines.append("")

    # Generated files
    lines.append("## Generated files")
    lines.append("")
    lines.append(f"- [{maqam}.tsv]({maqam}.tsv)")
    lines.append(f"- [{maqam}.svg]({maqam}.svg)")
    if generate_scl:
        lines.append(f"- [{maqam}.scl]({maqam}.scl)")
    lines.append(f"- [{maqam}.ly]({maqam}.ly)")
    ly_png = os.path.join(output_dir, f"{maqam}.cropped.png")
    if os.path.exists(ly_png):
        lines.append(f"- [{maqam}.cropped.png]({maqam}.cropped.png)")
    lines.append("")

    # Interval table
    lines.append(f"## Interval table")
    lines.append("")
    lines.append("```")
    for tsv_line in tsv_lines:
        lines.append(tsv_line)
    lines.append("```")
    lines.append("")

    # Scala tuning file
    if generate_scl:
        scl_path = os.path.join(output_dir, f"{maqam}.scl")
        if os.path.exists(scl_path):
            lines.append(f"## Scala tuning file")
            lines.append("")
            lines.append("```")
            with open(scl_path, 'r') as sf:
                lines.append(sf.read().rstrip())
            lines.append("```")
            lines.append("")

    # LilyPond file
    ly_path = os.path.join(output_dir, f"{maqam}.ly")
    if os.path.exists(ly_path):
        lines.append(f"## LilyPond file")
        lines.append("")
        ly_png_path = os.path.join(output_dir, f"{maqam}.cropped.png")
        if os.path.exists(ly_png_path):
            lines.append(f"![{maqam} scale]({maqam}.cropped.png)")
            lines.append("")
        lines.append("```lilypond")
        with open(ly_path, 'r') as lf:
            lines.append(lf.read().rstrip())
        lines.append("```")
        lines.append("")

    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, 'w') as f:
        f.write('\n'.join(lines))

def create_lilypond_file(maqam, scale_by_cents, description, output_dir):
    """Create a LilyPond .ly file rendering the scale as whole notes starting at C2."""
    pitch_names = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']

    def cents_to_lilypond_pitch(cent):
        nearest_semitone = round(cent / 100)
        pitch_index = nearest_semitone % 12
        octave_offset = nearest_semitone // 12
        name = pitch_names[pitch_index]
        # Base octave is C2 = "c," in LilyPond absolute mode
        # octave_offset 0 → suffix ","  (C2 octave)
        # octave_offset 1 → suffix ""   (C3 octave)
        # octave_offset 2 → suffix "'"  (C4 octave)
        if octave_offset == 0:
            suffix = ","
        elif octave_offset == 1:
            suffix = ""
        else:
            suffix = "'" * (octave_offset - 1)
        return f"{name}{suffix}"

    note_lines = []
    for cent in scale_by_cents:
        pitch = cents_to_lilypond_pitch(cent)
        note_lines.append(f'      {pitch}1^\\markup {{ "{cent:.1f}¢" }}')

    lines = []
    lines.append('\\version "2.24.0"')
    lines.append("")
    lines.append("\\header {")
    lines.append(f'  title = "{maqam}"')
    lines.append(f'  subtitle = "{description}"')
    lines.append("  tagline = ##f")
    lines.append("}")
    lines.append("")
    lines.append("\\score {")
    lines.append("  \\new Staff {")
    lines.append('    \\clef "bass"')
    lines.append("    \\cadenzaOn")
    lines.append("    \\absolute {")
    for note_line in note_lines:
        lines.append(note_line)
    lines.append("    }")
    lines.append("  }")
    lines.append("  \\layout { }")
    lines.append("}")
    lines.append("")

    ly_filename = os.path.join(output_dir, f"{maqam}.ly")
    with open(ly_filename, 'w') as f:
        f.write('\n'.join(lines))

    # Render to PNG if lilypond is available
    if shutil.which('lilypond'):
        output_prefix = os.path.join(output_dir, maqam)
        result = subprocess.run(
            ['lilypond', '--png', '-dcrop', '-dresolution=150', '-o', output_prefix, ly_filename],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  Warning: lilypond rendering failed for {maqam}: {result.stderr.strip()}")

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

frequencies_to_output = np.array(maqamat['metadata']['frequencies_to_output'])

for maqam in (maqamat['maqamat']):

    if args['maqam'] is not None and maqam != args['maqam']:
        continue

    metadata  = maqamat['maqamat'][maqam]['metadata']
    by        = metadata['by']
    source    = metadata.get('source', '')
    page      = metadata.get('page', '')
    comment   = metadata.get('comment', '')
    intervals = maqamat['maqamat'][maqam]['intervals']

    output_dir = os.path.join('results', by, maqam)
    os.makedirs(output_dir, exist_ok=True)

    print(f"  maqam={maqam}  by={by}  source={source}  page={page}  comment={comment}  output={output_dir}")

    # By Equal Temperament
    if by == 'et' or by == 'tet' or by == 'edo':
        number_of_intervals  = maqamat['maqamat'][maqam]['number_of_intervals']
        cents_per_interval   = cents_per_octave/number_of_intervals
        
        
        scale_by_cents       = np.arange(0, cents_per_octave+cents_per_interval, cents_per_interval)
        scale_in_frequencies = frequency_from_cents(f1, scale_by_cents, cents_per_octave)

    else:
        intervals = maqamat['maqamat'][maqam]['intervals']
        intervals_str = ','.join(map(str,intervals))
        intervals_str = f"[{intervals_str}]"
        
        scale_by_ratios = np.array(eval(intervals_str))
        
        scale_by_cents  = cents_from_ratio(scale_by_ratios,cents_per_octave)
        scale_in_frequencies = frequency_from_ratio(f1,scale_by_ratios)

    number_of_intervals  = scale_by_cents.size-1

    if by == 'et' or by == 'tet' or by == 'edo':
        limit_denominator = number_of_intervals-1
    else:
        limit_denominator = (number_of_intervals+10)**4
        
    description = f"scale type ={maqam}, provided type=by {by}, intervals={number_of_intervals}, f0={f0}Hz"

# TODO: amazing https://ryanhpratt.github.io/maya/

    scale_hash_value=(sha256(bytes(scale_by_cents)).hexdigest())

    arcs_per_cents = get_arcs_per_cents(scale_by_cents,cents_per_octave)

    frequency_ratios = scale_in_frequencies/f1

    delta_cents  = np.diff(scale_by_cents)
    delta_cents  = np.append(0, delta_cents)

    tsv_lines = []

    tee("", tsv_lines)
    tee("#-------------------------------------------------------------------------------------------------", tsv_lines)
    tee(f"# {description}", tsv_lines)
    tee("#-------------------------------------------------------------------------------------------------", tsv_lines)
    tee("%-4s %11s %11s  %-8s  %-16s %8s  %11s  %11s %12s" %("#", "cents", "Δ cents","f ratio", "ratio (derived)","fl ratio","abs error","rel error","f (Hz)"), tsv_lines)
    tee("#-------------------------------------------------------------------------------------------------", tsv_lines)

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

        freqs=(2**(cent/cents_per_octave))*frequencies_to_output


        z = np.array2string(freqs, separator=' | ', formatter={'float': lambda x: f"{x:-8.3f}"})[1:-1]

        tee("%-4s %11.6f %11.6f  %8.6f  %-16s %8f  %11.8f  %11.8f | %s" %(i,cent,delta_cents[i],f_ratio,fraction,fraction_float,aerror,rerror,z), tsv_lines)

        if generate_audio is True:
            generate_frequency(f)

    tee("#-------------------------------------------------------------------------------------------------", tsv_lines)

    # Create SCL (Scala file) output
    if generate_scl is True:
        scl_filename = os.path.join(output_dir, f"{maqam}.scl")
        create_scala_file(scale_by_cents, description, scl_filename)
        tee(f"# Scala file written: {scl_filename}", tsv_lines)

        # m = hashlib.sha256(given_ratios_str.encode('UTF-8'))
        # print(m.hexdigest())

    derived_ratios_str = (', '.join(map(str, derived_ratios)))
    #print(sha256(derived_ratios_str).hexdigest())

    # m = hashlib.sha256(derived_ratios_str.encode('UTF-8'))
    # print(m.hexdigest())

    tee(f"# derived ratios: [{derived_ratios_str}]", tsv_lines)

    np.set_printoptions(precision=3,floatmode='fixed')
    #print(np.array(scale_by_cents))

    scale_by_cents_str = (', '.join(map(str, scale_by_cents)))

    tee(f"# derived  cents: [{scale_by_cents_str}]", tsv_lines)

    tee(f"# derived  cents: sha256:{scale_hash_value}", tsv_lines)
    tee("#-------------------------------------------------------------------------------------------------", tsv_lines)

    # Write TSV file
    tsv_filename = os.path.join(output_dir, f"{maqam}.tsv")
    with open(tsv_filename, 'w') as f:
        f.write('\n'.join(tsv_lines))
        f.write('\n')

    # Write LilyPond file (before README so it can embed the content)
    create_lilypond_file(maqam, scale_by_cents, description, output_dir)

    # Write README
    create_readme_file(maqam, metadata, intervals, number_of_intervals, by, derived_ratios_str, scale_by_cents_str, scale_hash_value, output_dir, generate_scl, maqamat, args['maqamat_file'], tsv_lines)

    # Canvas section
    svg_filename = os.path.join(output_dir, f"{maqam}.svg")
    dwg=create_canvas(output_file=svg_filename, canvas_width=canvas_width, canvas_height=canvas_height)

    add_bracelet_circle(dwg, stroke='red', fill=svgwrite.rgb(200, 200, 200), radius=250, stroke_width=.5 )
    add_bracelet_circle(dwg, stroke='black', stroke_width=.75)

    add_cent_tic_marks(dwg, stroke='blue',  radius=1.025*r_bracelet, interval=2)
    add_cent_tic_marks(dwg, stroke='red',   radius=1.05*r_bracelet,  interval=6)
    add_cent_tic_marks(dwg, stroke='green', stroke_width=.75, radius=1.075*r_bracelet,  interval=50)

    add_notes(dwg, cents=scale_by_cents, radius=r_bracelet, stroke='red', stroke_width=.75, cx=cx, cy=cy)

    dwg.save()
