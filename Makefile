project = AOD-Dictionary
GLIBC_VERSION_RAW=$(shell getconf GNU_LIBC_VERSION)
GLIBC_VERSION=$(shell sed -e 's/ /./g' <<< '${GLIBC_VERSION_RAW}')


all: appimage clean
	echo "done"

clean:
	@echo	"[clean] Cleanup the AppDir" && 		rm	-rf		$(project).AppDir
	@echo	"[clean] Cleanup the PyInstaller" && 	rm 	-rf		target/PyInstaller
	@echo	"[clean] Cleanup the Build" && 			rm  -rf		target/$(project)
	echo $(GLIBC_VERSION1)


appimage:
	python3         -m     fbs freeze
	cp              -r     src/main/python/modules target/$(project)
	cp              -r     src/main/python/icons target/$(project)
	cp              -r     src/main/python/css target/$(project)
	cp              -r     src/main/python/lib target/$(project)
	cp              -r     src/main/python/themes target/$(project)
	cp              -r     src/main/python/application.py target/$(project)

	rm              -rf    $(project).AppDir
	mkdir           -p     $(project).AppDir/opt/$(project)
	cp              -r     target/$(project) $(project).AppDir/opt
	cp              -r     src/main/icons/Icon.svg $(project).AppDir/icon.svg
	echo			"[Desktop Entry]" >> $(project).AppDir/$(project).desktop
	echo			"Name=$(project)" >> $(project).AppDir/$(project).desktop
	echo			"Exec=AppRun" >> $(project).AppDir/$(project).desktop
	echo			"Icon=icon" >> $(project).AppDir/$(project).desktop
	echo			"Type=Application" >> $(project).AppDir/$(project).desktop
	echo			"Categories=Office;Education;" >> $(project).AppDir/$(project).desktop

	echo			"#! /bin/bash" >> $(project).AppDir/AppRun
	echo			"set -e" >> $(project).AppDir/AppRun
	echo			"cd \$${HOME}" >> $(project).AppDir/AppRun
	echo			"exec \$${APPDIR}/opt/$(project)/$(project)" >> $(project).AppDir/AppRun
	chmod 			+x $(project).AppDir/AppRun
	find 			$(project).AppDir -name '__pycache__' -exec rm -rf {} +
	find 			$(project).AppDir -name '.pyc*' -exec rm -rf {} +
	export 			ARCH=x86_64
	exec 			bin/appimagetool $(project).AppDir bin/$(project).AppImage

