import os, sys, glob
import argparse
from svg2glif import svg2glif

def get_args():
    def split(arg):
        return arg.replace(",", " ").split()

    def transform_list(arg):
        try:
            return [float(n) for n in split(arg)]
        except ValueError:
            msg = "Invalid transformation matrix: %r" % arg
            raise argparse.ArgumentTypeError(msg)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir", metavar="OUT_DIR", help="Output dir",
        default=None)
    parser.add_argument(
        "-w", "--width", help="The glyph advance width (default: 0)",
        type=int, default=1000)
    parser.add_argument(
        "-H", "--height", help="The glyph vertical advance (optional if "
        '"width" is defined)', type=int, default=0)
    parser.add_argument(
        "-t", "--transform", help="Transformation matrix as a list of six "
        'float values (e.g. -t "0.1 0 0 -0.1 -50 200")', type=transform_list,default="0.39,0,0,0.39,0,-120")
    parser.add_argument(
        "-f", "--format", help="UFO GLIF format version (default: 2)",
        type=int, choices=(1, 2), default=2)
    parser.add_argument("in_dir", metavar="DIR", type=str,
                        help="input directory in which .svg are located")

    args = parser.parse_args()

    return args

def main():
    options = get_args()

    if options.out_dir is None:
        options.out_dir = options.in_dir

    for svg_file in glob.glob(os.path.join(options.in_dir, '*.svg')):
        with open(svg_file, "r", encoding="utf-8") as f:
            svg = f.read()

        name = os.path.splitext(os.path.basename(svg_file))[0]
        outfile = os.path.join(options.out_dir, f'{name}.glif')

        glif = svg2glif(svg, name,
                        width=options.width,
                        height=options.height,
                        unicodes=[int(name.replace('uni', ''), 16)],
                        transform=options.transform,
                        version=options.format)

        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(glif)

if __name__ == '__main__':
    main()
