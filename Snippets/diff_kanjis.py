import sys
import argparse
from fontTools.ttLib import TTFont

def is_kanji(uni):
    return 0x2E80 <= uni <= 0x2EFF or \
    0x2F00 <= uni <= 0x2FDF or \
    0x3400 <= uni <= 0x4DBF or \
    0x4E00 <= uni <= 0x9FFF or \
    0xF900 <= uni <= 0xFAFF or \
    0x20000 <= uni <= 0x2A6DF or \
    0x2A700 <= uni <= 0x2B73F or \
    0x2B740 <= uni <= 0x2B81F or \
    0x2B820 <= uni <= 0x2CEAF or \
    0x2CEB0 <= uni <= 0x2EBEF or \
    0x2F800 <= uni <= 0x2FA1F

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--output', dest='out_log', metavar='OUTPUT_LOG', type=str, default=None,
                        help='output log_file')
    parser.add_argument('--src-font', metavar='FONT', type=str, required=True, help='src font')
    parser.add_argument('--dst-font', metavar='FONT', type=str, required=True, help='dst font')
    parser.add_argument('--max-num', metavar='NUM', type=int, default=None, help='max number')

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    src_ttFont = TTFont(args.src_font)
    dst_ttFont = TTFont(args.dst_font)
    cmap = src_ttFont.getBestCmap()
    rcmap = dst_ttFont['cmap'].buildReversed()

    fout = sys.stdout
    if args.out_log:
        fout = open(args.out_log, 'w')
    cnt = 0
    for gname in dst_ttFont.getGlyphOrder():
        if gname not in rcmap:
            continue
        uni = sorted(rcmap[gname])[0]
        if is_kanji(uni) and uni not in cmap:
            print(f'{uni:04X}', file=fout)
            cnt += 1
            if args.max_num and cnt >= args.max_num:
                break

    if fout != sys.stdout:
        fout.close()

if __name__ == '__main__':
    main()
