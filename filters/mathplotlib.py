#!/usr/bin/env python3

"""
Pandoc filter.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension, stringify

def plantuml(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "plot" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("plot", code)
            filetype = get_extension(format, "png", html="svg", latex="eps")

            dest = filename + '.' + filetype

            if not os.path.isfile(dest):
                src = code.encode(sys.getfilesystemencoding())
                src = src.decode('utf-8')

                df = pd.read_csv(src,
                                 skipinitialspace=True,
                                 iterator=False)

                # df.plot()
                plt.figure(dpi=None, facecolor="white")

            # return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(plantuml)
