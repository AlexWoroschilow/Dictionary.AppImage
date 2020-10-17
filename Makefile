PWD := $(shell pwd)
SHELL := /usr/bin/bash
APPDIR := ./AppDir
GLIBC_VERSION := $(shell getconf GNU_LIBC_VERSION | sed 's/ /-/g' )

all: init appimage clean

#tesseract-ocr
#tesseract-ocr-rus

init:
	rm -rf $(PWD)/venv
	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && python3 -m pip install -r $(PWD)/requirements.txt




clean:
	rm -rf ${APPDIR}/venv
	rm -rf ${APPDIR}/opt
