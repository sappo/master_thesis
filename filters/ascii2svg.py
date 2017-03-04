#!/usr/bin/env python3

"""
Pandoc filter to process code blocks with class "a2s" into
ascii2svg-generated images.

Needs `a2s` shell script from https://github.com/dhobsd/asciitosvg
"""

import os
import sys
from subprocess import call

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension

def ascii2svg(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "a2s" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("a2s", code)
            filetype = get_extension(format, "svg")

            src = filename + '.a2s'
            dest = filename + '.' + filetype

            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                txt = txt.decode('utf-8')
                with open(src, "w") as f:
                    f.write(txt)

                call(["a2s -i%s -o%s" % (src, dest)], shell=True)
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(ascii2svg)

