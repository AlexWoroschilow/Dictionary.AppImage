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

init:
	rm -rf $(PWD)/venv
	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && $(PWD)/venv/bin/python3 -m pip install -r $(PWD)/requirements.txt

	wget https://apprepo.de/appimage/download/apprepo --output-document=$(PWD)/bin/Apprepo.AppImage
	wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage --output-document=$(PWD)/bin/appimagetool.AppImage

	chmod +x $(PWD)/bin/appimagetool.AppImage
	chmod +x $(PWD)/bin/Apprepo.AppImage

	
all: init

	mkdir -p $(PWD)/build/Boilerplate.AppDir/application
	mkdir -p $(PWD)/build/Boilerplate.AppDir/vendor

	$(PWD)/bin/Apprepo.AppImage --destination=$(PWD)/build appdir boilerplate python3.8 python3.8-dev python3.8-psutil python3-xlib libxcb1 \
										python3.8-setuptools python3-pip python3-dnf python3-apt python3-xdg libicu66 \
										python3-distutils python3-distutils-extra python3-gi python3-dbus python3-cairo \
										python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtx11extras python3-pyqt5.qtquick python3-pyqt5.sip \
										openssl libffi7 intltool libgudev-1.0-0 libffi libgudev gir1.2-gudev-1.0 \
										zlib1g libleptonica-dev libjpeg-turbo8 libwebp6 libpcre2-16-0 \
										tesseract-ocr tesseract-ocr-bel tesseract-ocr-rus tesseract-ocr-ukr  tesseract-ocr-eng \
										tesseract-ocr-deu tesseract-ocr-spa tesseract-ocr-fra tesseract-ocr-ita tesseract-ocr-fin \
										tesseract-ocr-dan tesseract-ocr-ell tesseract-ocr-est tesseract-ocr-heb tesseract-ocr-hin \
										tesseract-ocr-hrv tesseract-ocr-hun tesseract-ocr-isl tesseract-ocr-lav tesseract-ocr-lit \
										tesseract-ocr-nld tesseract-ocr-nor tesseract-ocr-pol tesseract-ocr-por tesseract-ocr-slk \
										tesseract-ocr-slv tesseract-ocr-sqi tesseract-ocr-srp tesseract-ocr-swe tesseract-ocr-chi-sim \
										tesseract-ocr-chi-tra tesseract-ocr-jpn tesseract-ocr-ara

	cp -r --force $(PWD)/src/default 	$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/icons 		$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/lib 		$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/modules 	$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/themes 	$(PWD)/build/Boilerplate.AppDir/application/
	cp -r --force $(PWD)/src/main.py 	$(PWD)/build/Boilerplate.AppDir/application/

	echo 'TESSDATA_PREFIX=$${APPDIR}/share/tesseract-ocr/4.00/tessdata'                     >> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo 'export TESSDATA_PREFIX=$${TESSDATA_PREFIX}'                                       >> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo ''                                                                                 >> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo ''                                                                                 >> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo 'case "$${1}" in'                                                                  >> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo "  '--python') exec \$${APPDIR}/bin/python3.8 \$${*:2} ;;"                         >> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo '  *)   $${APPDIR}/bin/python3.8 $${APPDIR}/application/main.py $${@} ;;'          >> $(PWD)/build/Boilerplate.AppDir/AppRun
	echo 'esac'                                                                             >> $(PWD)/build/Boilerplate.AppDir/AppRun

	python3 -m venv --copies $(PWD)/venv
	source $(PWD)/venv/bin/activate && $(PWD)/venv/bin/python3 -m pip install -r $(PWD)/requirements.txt --target=$(PWD)/build/Boilerplate.AppDir/vendor --upgrade
	source $(PWD)/venv/bin/activate && $(PWD)/venv/bin/python3 -m pip uninstall typing -y 	|| true
	rm -rf $(PWD)/build/Boilerplate.AppDir/vendor/typing.py 								|| true

	rm -f $(PWD)/build/Boilerplate.AppDir/*.desktop 	|| true
	rm -f $(PWD)/build/Boilerplate.AppDir/*.svg 		|| true	

	cp --force $(PWD)/AppDir/*.svg 		$(PWD)/build/Boilerplate.AppDir 			|| true	
	cp --force $(PWD)/AppDir/*.desktop 	$(PWD)/build/Boilerplate.AppDir 			|| true	

	export ARCH=x86_64 && $(PWD)/bin/appimagetool.AppImage  $(PWD)/build/Boilerplate.AppDir $(PWD)/Dictionary.AppImage
	chmod +x $(PWD)/Dictionary.AppImage

icons: $(ICONS)
clean: $(shell rm -rf $(PWD)/build)


$(ICONS):
	rm -f src/icons/`echo $@ | sed -e 's/svg/png/'`
	inkscape src/icons/$@ --export-dpi=96 --export-filename=src/icons/`echo $@ | sed -e 's/svg/png/'`


