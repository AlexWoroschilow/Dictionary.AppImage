PWD := $(shell pwd)
PYTHON := $(shell which python3)
SHELL := /usr/bin/bash
APPDIR := ./AppDir
APPDIR_APPLICATION := ${APPDIR}/opt/application
GLIBC_VERSION := $(shell getconf GNU_LIBC_VERSION | sed 's/ /-/g' )

all: init appimage clean

init:
	rm -rf ./venv
	rm -rf ./builds
	$(PYTHON) -m venv --copies venv
	source $(PWD)/venv/bin/activate && python3 -m pip install -r $(PWD)/requirements.txt
	cp /lib64/libpython3.6m.so.1.0 $(PWD)/venv/lib64

appimage: clean
	rm -rf ${APPDIR}/venv
	cp -r ./venv ${APPDIR}
	rm -rf $(APPDIR_APPLICATION)
	mkdir -p $(APPDIR_APPLICATION)
	cp -r ./src/icons $(APPDIR_APPLICATION)
	cp -r ./src/lib $(APPDIR_APPLICATION)
	cp -r ./src/modules $(APPDIR_APPLICATION)
	cp -r ./src/themes $(APPDIR_APPLICATION)
	cp -r ./src/default $(APPDIR_APPLICATION)
	cp ./src/main.py $(APPDIR_APPLICATION)
	bin/appimagetool-x86_64.AppImage  ./AppDir bin/AOD-Dictionary.AppImage
	@echo "done: bin/AOD-Dictionary.AppImage"

clean:
	rm -rf ${APPDIR}/venv
	rm -rf ${APPDIR}/opt
