#!/bin/bash
#pandoc -s -V geometry="paperwidth=18cm, paperheight=34cm, margin=0.3cm" \
       #-V lang=de-DE --highlight-style=espresso --filter=pandoc-citeproc \
       #--biblio=paper.bib --csl=ieee.csl \
       #-o paper.pdf paper.md
pandoc --number-sections -V lang=de-DE --highlight-style=espresso \
       --filter=pandoc-citeproc \
       --latex-engine=xelatex --template=template_expose.tex \
       --biblio=expose_thesis.bib --csl=din-1505-2-numeric.csl \
       -o ./expose_thesis.pdf ./expose_thesis.md
