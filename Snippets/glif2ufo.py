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
    parser.add_argument("--src_txt_file", dest="src_txt_file", metavar="FILE", type=str, default=None,
                        help="path to a text file in which unicode values are listed")
    parser.add_argument("in_dir", metavar="DIR", type=str,
                        help="input directory in which .glifs are located")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    glyphOrder = None
    if args.src_txt_file:
        with open(args.src_txt_file) as fin:
            glyphOrder = [f'uni{int(line.strip(), 16):04X}' for line in fin.readlines()]

    uni2glif = {}
    font = Font()
    for file in glob.glob(os.path.join(args.in_dir, '*.glif')):
        basename, _ = os.path.splitext(os.path.basename(file))
        if not basename.startswith('uni'):
            continue
        uni = int(basename.replace('uni', ''), 16)
        uni2glif[basename] = file
        font.newGlyph(basename)
    if glyphOrder is not None:
        font.glyphOrder = glyphOrder
    font.save(args.out_ufo)

    with open(os.path.join(args.out_ufo, 'glyphs', 'contents.plist'), 'rb') as fin:
        contents = plistlib.load(fin)
    for uni, file in uni2glif.items():
        output_path = os.path.join(args.out_ufo, 'glyphs', contents[uni])
        shutil.copyfile(file, output_path)

if __name__ == '__main__':
    main()
