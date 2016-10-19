#!/bin/bash
pandoc --number-sections -V lang=de-DE --highlight-style=espresso \
       --filter=pandoc-crossref -M "crossrefYaml=pandoc-crossref-de.yaml" \
       --filter=pandoc-citeproc \
       --latex-engine=xelatex --template=thesis_template.tex \
       -o ./thesis.pdf ./thesis.md ./content/ch*.md
