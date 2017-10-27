.PHONY: all
all: build

.PHONY: test
test:
	python urukul_sim.py

.PHONY: build
build: build/urukul.vm6

build/urukul.vm6: urukul.py urukul_cpld.py
	python urukul_impl.py

REV:=$(shell git describe --always --abbrev=8 --dirty)

.PHONY: release
release: build/urukul.vm6
	cd build; tar czvf urukul_$(REV).tar.gz \
		urukul.v urukul.ucf urukul.xst \
		urukul.vm6 urukul.jed urukul.isc \
		urukul.tim urukul.rpt \
		urukul.pad urukul_pad.csv

