.PHONY: all
all: build

.PHONY: build
build: build/urukul.vm6

build/urukul.vm6: urukul.py urukul_cpld.py
	python urukul.py

REV:=$(shell git describe --always --abbrev=8 --dirty)

.PHONY: release
release: build/urukul.vm6
	cd build; tar czvf urukul_$(REV).tar.gz \
		urukul.v urukul.ucf urukul.xst \
		urukul.vm6 urukul.jed urukul.isc \
		urukul.tim urukul.rpt \
		urukul.pad urukul_pad.csv

