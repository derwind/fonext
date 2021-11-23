#MenuTitle: Set images as backgrounds
# -*- coding: utf-8 -*-

__doc__ = """
Set images as backgrounds
"""

from Foundation import *
import os
import glob

def main():
    folder_path = GetFolder('Select a folder in which glyph images are located')
    if folder_path is None:
        return

    font = GSFont()

    for file in glob.glob(os.path.join(folder_path, '*.*')):
        basename, ext = os.path.splitext(os.path.basename(file))
        if ext.lower() not in ['.png', '.jpg', '.bmp']:
            continue
        if not basename.startswith('uni'):
            continue
        uni = int(basename.replace('uni', ''), 16)
        glyph = GSGlyph(basename)
        glyph.unicode = '{0:04X}'.format(uni)
        font.glyphs.append(glyph)
        # manipulate layers after glyph is appended to the font
        glyph.layers[0].backgroundImage = GSBackgroundImage(file)
        #thisImage = GSBackgroundImage.alloc().initWithPath_(file)
        #glyph.layers[0].setBackgroundImage_(thisImage)

        for layer in glyph.layers:
            layer.width = 1000

    font.familyName = "New Fonts"
    Glyphs.fonts.append(font)

if __name__ == '__main__':
    main()
