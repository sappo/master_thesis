#!/usr/bin/env python3

"""
Pandoc filter to process code blocks with class "plantuml" into
plant-generated images.

Needs `plantuml.jar` from http://plantuml.com/.
"""

import os
import sys
from subprocess import call

from pandocfilters import toJSONFilter, Para, Image, get_filename4code, get_caption, get_extension, stringify

def plantuml(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "plantuml" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("plantuml", code)
            filetype = get_extension(format, "png", html="svg", latex="eps")

            src = filename + '.uml'
            dest = filename + '.' + filetype

            skinparams = [
                "skinparam monochrome true",
                "skinparam shadowing false",
            ]
            metaMonoFont = meta.get('monofont', None)
            if metaMonoFont:
                fontName = stringify(metaMonoFont['c'])
                skinparams.append("skinparam defaultFontName %s" % fontName)

            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                txt = txt.decode('utf-8')
                if not txt.startswith("@start"):
                    params = ""
                    for skinparam in skinparams:
                        params += "%s\n" % skinparam

                    txt = "@startuml\n" + params + txt + "\n@enduml\n"
                with open(src, "w") as f:
                    f.write(txt)

                call(["plantuml.jar -t%s %s" % (filetype, src)], shell=True)
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter(plantuml)
