import os
from fontTools.ttLib import TTFont
from extractor import extractUFO

class UTFont:
    def __init__(self, font_path, use_defcon=False):
        self.font_path = font_path
        self.use_defcon = use_defcon

        self._ttFont = TTFont(self.font_path)
        self._extracted_path = None
        self._extracted_ufo = None

    def save(self, file):
        if self._extracted_path is None:
            self._ttFont.save(file)
            return

        #self._extracted_ufo.save(self._extracted_path)
        ttFont = self._compile_font()
        for table in ['GPOS', 'GSUB']:
            if table in self._ttFont:
                ttFont[table] = self._ttFont[table]
        self._ttFont.close()
        self._ttFont = ttFont
        self._ttFont.save(file)

        self._extracted_path = None
        self._extracted_ufo = None
        self._remove_garbages()

    def append_glyph(self, glyph):
        self._extract()

        self._extracted_ufo.addGlyph(glyph)

    def remove_glyph(self, glyph_name):
        self._extract()

        if glyph_name in self._extracted_ufo:
            del self._extracted_ufo[glyph_name]

    def _compile_font(self):
        if self._extracted_path is None:
            return None

        if 'CFF ' in self._ttFont:
            from ufo2ft import compileOTF
            return compileOTF(self._extracted_ufo)
        else:
            from ufo2ft import compileTTF
            return compileTTF(self._extracted_ufo)

    def _extract(self):
        if self._extracted_path is not None:
            return

        if self.use_defcon:
            from defcon import Font
        else:
            from ufoLib2 import Font

        dirname = os.path.dirname(self.font_path)
        basename, _ = os.path.splitext(os.path.basename(self.font_path))
        self._extracted_path = os.path.join(dirname, f'{basename}.ufo')

        self._extracted_ufo = Font()
        extractUFO(self.font_path, self._extracted_ufo)

    def _remove_garbages(self):
        if self._extracted_path is not None:
            return
