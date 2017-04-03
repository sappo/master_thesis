#!/usr/bin/env python3

"""
Pandoc filter to process code blocks with class "a2s" into
ascii2svg-generated images.

Needs `a2s` shell script from https://github.com/dhobsd/asciitosvg
"""

import os
import sys
from subprocess import call

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension, stringify

def ascii2svg(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "a2s" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("a2s", code)
            typepandoc = get_extension(format, "pdf")
            typea2s = "svg"

            src = filename + '.a2s'
            desta2s = filename + '.' + typea2s

            fontName = ""
            metaMonoFont = meta.get('monofont', None)
            if metaMonoFont:
                fontName = stringify(metaMonoFont['c'])

            if not os.path.isfile(desta2s):
                txt = code.encode(sys.getfilesystemencoding())
                txt = txt.decode('utf-8')
                with open(src, "w") as f:
                    f.write(txt)

                call(['a2s "-f%s" -i%s -o%s' % (fontName, src, desta2s)], shell=True)
                sys.stderr.write('Created image ' + desta2s + '\n')

            return Para([Image([ident, [], keyvals], caption, [desta2s, typef])])

if __name__ == "__main__":
    toJSONFilter(ascii2svg)

