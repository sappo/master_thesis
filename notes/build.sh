#!/bin/bash
pandoc --toc --toc-depth=1 --mathjax --css github-pandoc.css -s -o notes.html *.md
