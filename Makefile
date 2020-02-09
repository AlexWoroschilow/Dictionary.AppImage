PWD := $(shell pwd)
SHELL := /usr/bin/bash
APPDIR := ./AppDir
GLIBC_VERSION := $(shell getconf GNU_LIBC_VERSION | sed 's/ /-/g' )

all: init appimage clean

init:
	rm -rf $(PWD)/venv
	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && python3 -m pip install -r $(PWD)/requirements.txt


appimage: clean
	source $(PWD)/venv/bin/activate && python3 -O -m PyInstaller src/main.py --distpath $(APPDIR) --name application --noconfirm
	cp -r ./src/icons $(APPDIR)/application
	cp -r ./src/lib $(APPDIR)/application
	cp -r ./src/modules $(APPDIR)/application
	cp -r ./src/themes $(APPDIR)/application
	cp -r ./src/default $(APPDIR)/application
	bin/appimagetool-x86_64.AppImage  ./AppDir bin/AOD-Dictionary.AppImage
	chmod +x bin/AOD-Dictionary.AppImage
	@echo "done: bin/AOD-Dictionary.AppImage"

clean:
	rm -rf ${APPDIR}/venv
	rm -rf ${APPDIR}/opt
