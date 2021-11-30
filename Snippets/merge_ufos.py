import os
import glob
import plistlib
import shutil
import argparse
from ufoLib2 import Font

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", dest="out_ufo", metavar="UFO", type=str, required=True,
                        help="output ufo")
    parser.add_argument("--src_txt_file", dest="src_txt_file", metavar="FILE", type=str, required=True,
                        help="path to a text file in which unicode values are listed")
    parser.add_argument("in_ufos", metavar="UFO", nargs="+", type=str,
                        help="input UFOs")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    glyphOrder = None
    if args.src_txt_file:
        with open(args.src_txt_file) as fin:
            glyphOrder = [f'uni{int(line.strip(), 16):04X}' for line in fin.readlines()]

    in_fonts = [Font(path) for path in args.in_ufos]

    font = Font()
    for gname in glyphOrder:
        for f in in_fonts:
            if gname in f.glyphOrder:
                g = f[gname]
                break
        font.addGlyph(g)
    font.glyphOrder = glyphOrder
    font.save(args.out_ufo)

if __name__ == '__main__':
    main()
