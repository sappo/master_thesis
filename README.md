# Cleanthesis with pandoc

This project is pandoc markdown environment to write a thesis. It is based of
the [Clean Thesis](http://cleanthesis.der-ric.de/) latex template by Ricardo
Langner. There have been a lot of improvements so that everything can be setup
from markdown and generated to pdf.

This is my acutal thesis but feel free to use it as an template to start your own :)

## Instalation

Haskell tools:

* pandoc                    # Document converter
* pandoc-citeproc           # bibliography/citations filter
* pandoc-citeproc-preamble  # bibliography header + settings
* pandoc-crossref           # images/tables/equations references

install with `cabal install <tool>`

Other tools

* python3 (required by filters)
* java1.7+ (required by plantuml filter)
* inkscape (required to convert svg/eps to pdf)

## Configuration

Do all the configuration in `thesis.md`.

## Citations

But citation key into brackets: [@citation_key]

## References

* Label: {#sec:yourlabel} {#fig:yourlabel} {#tbl:yourlabel} {#eq:yourlabel}
* Reference: @sec:yourlabel @fig:yourlabel @tbl:yourlabel @eq:yourlabel

## Code Block Filters

* Use plain tex markup which is pased to latex engine unmodified:

````
```tex
<your tex markup here>
```
````

* Convert plantuml codeblocks into images:

````
```plantuml
<your plantuml here>
```
````

* Convert asciitosvg codeblocks into images:

````
```a2s
<your asscitosvg here>
```
````

## Vim

If you're using vim and like a better pandoc markdown integration use my modified vim-markdown plugin https://github.com/sappo/vim-markdown.

## Licence

This project is GPL licensed as its based of the GPL licensed Clean Thesis
project.
