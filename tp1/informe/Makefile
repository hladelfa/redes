CC = pdflatex
SRC = InformeTP1
DEP = $(SRC:=.tex)
PDF = $(SRC:=.pdf)
TOC = $(SRC:=.toc)

.phony: all clean

all: $(PDF)

FORCE:

$(PDF): $(DEP) $(TOC)
	$(CC) $<

%.toc: $(DEP) FORCE
	$(CC) $<

clean:
	rm -f *.aux *.toc *.out


