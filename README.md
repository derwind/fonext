# fonext
font manipulation tools

## Installation

```sh
python setup.py install
```

## Sample codes

```python
from fonext.utLib import UTFont
from ufoLib2 import Font

utFont = UTFont('foo.ttf')
font = Font('bar.ufo')

utFont.append_glyph(font['a-hira'])
utFont.remove_glyph('uni611B')
utFont.save('baz.ttf')
```