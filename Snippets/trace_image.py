import os
import glob
import argparse

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir", metavar="OUT_DIR", help="Output dir",
        default=None)
    parser.add_argument("in_dir", metavar="DIR", type=str,
                        help="input directory in which .svg are located")

    args = parser.parse_args()

    return args

def main():
    options = get_args()

    if options.out_dir is None:
        options.out_dir = options.in_dir

    for bmp_file in glob.glob(os.path.join(options.in_dir, '*.bmp')):

        name = os.path.splitext(os.path.basename(bmp_file))[0]
        outfile = os.path.join(options.out_dir, f'{name}.svg')

        command = f'potrace -b svg -t 20 -O 0.2 -k 0.78 -o {outfile} {bmp_file}'
        os.system(command)

if __name__ == '__main__':
    main()
