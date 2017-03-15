# Cleanthesis with pandoc

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

```tex
<your tex markup here>
```

* Convert plantuml codeblocks into images:

```plantuml
<your plantuml here>
```

* Convert asciitosvg codeblocks into images:

```a2s
<your asscitosvg here>
```
