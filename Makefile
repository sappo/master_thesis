all: pdf

MD_FILES = \
	thesis.md \
	content/ch*.md

FILTERS = \
	--filter=pandoc-crossref -M "crossrefYaml=pandoc-crossref-de.yaml" \
	--filter=pandoc-citeproc \
	--filter=pandoc-citeproc-preamble -M "citeproc-preamble=citeproc-preamble.tex" \
	--filter=filters/plantuml.py \
	--filter=filters/ascii2svg.py \
	--filter=filters/latex_blocks.py \
	--filter=filters/svg2pdf.py \

EXPORTS = PATH=$(PATH):$(PWD)/tools/:$(PWD)/tools/asciitosvg/

LANGUAGE=de-DE

pdf:
	@$(EXPORTS) pandoc \
	   --number-sections -V lang=$(LANGUAGE) --highlight-style=espresso \
	   $(FILTERS) \
       --latex-engine=xelatex --template=thesis_template.tex \
	   -o thesis.pdf $(MD_FILES)

tex:
	@$(EXPORTS) pandoc \
	   --number-sections -V lang=$(LANGUAGE) --highlight-style=espresso \
	   $(FILTERS) \
       --latex-engine=xelatex --template=thesis_template.tex \
	   -o thesis.tex $(MD_FILES)

clean:
	@rm -f thesis.tex \
 	  	   thesis.aux \
		   thesis.lof \
		   thesis.log \
		   thesis.lop \
		   thesis.lot \
		   thesis.out \
		   thesis.synctex.gz \
		   thesis.toc

dist-clean: clean
	@rm -rf *-images
