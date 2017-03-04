#!/usr/bin/env python3

"""
Pandoc filter to process code blocks with class "tex" into
raw latex commands. This way it is possible to save the
highlighting of both markdown and latex.
"""

import sys
from pandocfilters import toJSONFilter, RawBlock, get_caption, stringify

def latex_block(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "tex" in classes:
            texblock = code.encode(sys.getfilesystemencoding())
            texblock = texblock.decode('utf-8')

            return RawBlock('latex', texblock)

        elif "texalgo" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            texblock = code.encode(sys.getfilesystemencoding())
            texblock = texblock.decode('utf-8')

            texblock = "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" % (
                r"\begin{algorithm}[p]",
                r"\tiny",
                r"\begin{algorithmic}[1]",
                "\caption{%s}" % stringify(caption),
                "\label{%s}" % ident,
                texblock,
                r"\end{algorithmic}",
                r"\end{algorithm}"
            )

            return RawBlock('latex', texblock)

if __name__ == "__main__":
    toJSONFilter(latex_block)
