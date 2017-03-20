#!/usr/bin/env python3

"""
Pandoc filter to process code blocks with class "tex" into
raw latex commands. This way it is possible to save the
highlighting of both markdown and latex.
"""

import sys
import re
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

            labels = []
            captions = []
            blocks = []
            subalgopattern = r"^#([^\s]*)\s*(.*)$"
            match = re.search(subalgopattern, texblock, re.MULTILINE)
            if match:
                label1 = match.group(1)
                caption1 = match.group(2)
                blockstart1 = match.end() + 1 # skip \n
                match = re.search(subalgopattern, texblock[1:], re.MULTILINE)
                blockend1 = match.start()
                label2 = match.group(1)
                caption2 = match.group(2)
                blockstart2 = match.end() + 2 # skip \n

                texalgorithm = r"""
                \begin{figure}
                \centering
                \begin{minipage}[t]{0.45\textwidth}
                    \vspace{0pt}
                    \centering
                    \begin{algorithm}[H]
                        \caption{%s}
                        \label{%s}
                        \tiny
                        \begin{algorithmic}[1]
                            %s
                         \end{algorithmic}
                    \end{algorithm}
                \end{minipage}
                \hfill
                \begin{minipage}[t]{0.45\textwidth}
                    \vspace{0pt}
                    \centering
                    \begin{algorithm}[H]
                        \caption{%s}
                        \label{%s}
                        \tiny
                        \begin{algorithmic}[1]
                            %s
                         \end{algorithmic}
                    \end{algorithm}
                \end{minipage}
                \end{figure}
                """ % (caption1, label1, texblock[blockstart1:blockend1],
                       caption2, label2, texblock[blockstart2:])
            else:
                texalgorithm = r"""
                \begin{figure}
                \centering
                \begin{minipage}[t]{0.45\textwidth}
                    \vspace{0pt}
                    \centering
                    \begin{algorithm}[H]
                        \caption{%s}
                        \label{%s}
                        \tiny
                        \begin{algorithmic}[1]
                            %s
                         \end{algorithmic}
                    \end{algorithm}
                \end{minipage}
                \end{figure}
                """ % (stringify(caption), ident, texblock)

            return RawBlock('latex', texalgorithm)

if __name__ == "__main__":
    toJSONFilter(latex_block)
