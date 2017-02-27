#!/bin/bash
export PATH=$PATH:$PWD/tools/

if [ "$1" == '--tex' ]; then
    pandoc --number-sections -V lang=de-DE --highlight-style=espresso \
           --filter=pandoc-crossref -M "crossrefYaml=pandoc-crossref-de.yaml" \
           --filter=pandoc-citeproc \
           --filter=./filters/plantuml.py \
           --latex-engine=xelatex --template=thesis_template.tex \
           -o ./thesis.tex ./thesis.md ./content/ch*.md
else
    pandoc --number-sections -V lang=de-DE --highlight-style=espresso \
           --filter=pandoc-crossref -M "crossrefYaml=pandoc-crossref-de.yaml" \
           --filter=pandoc-citeproc \
           --filter=./filters/plantuml.py \
           --latex-engine=xelatex --template=thesis_template.tex \
           -o ./thesis.pdf ./thesis.md ./content/ch*.md
fi
