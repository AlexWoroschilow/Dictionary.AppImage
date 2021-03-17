# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
PWD := $(shell pwd)
SHELL := /usr/bin/bash
ICONS := $(shell ls src/icons | grep svg)
.PHONY: all

all: clean

	mkdir -p $(PWD)/build/Boilerplate.AppDir/application
	mkdir -p $(PWD)/build/Boilerplate.AppDir/vendor

	apprepo --destination=$(PWD)/build appdir boilerplate python3.8 python3.8-dev python3.8-psutil \
										python3.8-setuptools python3-pip python3-dnf python3-apt \
										openssl libffi7 intltool libgudev-1.0-0 libffi libgudev \
										python3-pyqt5

	cp -r --force $(PWD)/src/default 	$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/icons 		$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/lib 		$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/modules 	$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/themes 	$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/main.py 	$(PWD)/build/Boilerplate.AppDir/application/

	echo 'case "$${1}" in' 																			>> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo "  '--python') exec \$${APPDIR}/bin/python3.8 \$${*:2} ;;" 								>> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo '  *)   $${APPDIR}/bin/python3.8 $${APPDIR}/application/main.py $${@} ;;' 					>> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo 'esac' 																					>> $(PWD)/build/Boilerplate.AppDir/AppRun

	sed -i 's/#APPDIR=`pwd`/APPDIR=`dirname \$${0}`/' $(PWD)/build/Boilerplate.AppDir/AppRun
	$(PWD)/build/Boilerplate.AppDir/AppRun --python -m pip install  -r $(PWD)/requirements.txt --target=$(PWD)/build/Boilerplate.AppDir/vendor --upgrade
	$(PWD)/build/Boilerplate.AppDir/AppRun --python -m pip uninstall typing -y
	sed -i 's/APPDIR=`dirname \$${0}`/#APPDIR=`dirname \$${0}`/' $(PWD)/build/Boilerplate.AppDir/AppRun

	rm -f $(PWD)/build/Boilerplate.AppDir/*.desktop 	| true
	rm -f $(PWD)/build/Boilerplate.AppDir/*.png 		| true
	rm -f $(PWD)/build/Boilerplate.AppDir/*.svg 		| true	

	cp --force $(PWD)/AppDir/*.svg 		$(PWD)/build/Boilerplate.AppDir 			| true	
	cp --force $(PWD)/AppDir/*.desktop 	$(PWD)/build/Boilerplate.AppDir 			| true	
	cp --force $(PWD)/AppDir/*.png 		$(PWD)/build/Boilerplate.AppDir 			| true	

	export ARCH=x86_64 && bin/appimagetool-x86_64.AppImage  $(PWD)/build/Boilerplate.AppDir $(PWD)/Dictionary.AppImage
	chmod +x $(PWD)/Dictionary.AppImage

icons: $(ICONS)
clean: $(shell rm -rf $(PWD)/build)

init:
	rm -rf $(PWD)/venv
	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && python3 -m pip install -r $(PWD)/requirements.txt


$(ICONS):
	rm -f src/icons/`echo $@ | sed -e 's/svg/png/'`
	inkscape src/icons/$@ --export-dpi=96 --export-filename=src/icons/`echo $@ | sed -e 's/svg/png/'`


