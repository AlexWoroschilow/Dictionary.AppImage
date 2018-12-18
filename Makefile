project = dictionary
project_version = 0.1
source_rpm = ~/rpmbuild/SOURCES
source_project = $(source_rpm)/$(project)-$(project_version)


all: appimage
	rm 			-rf		$(source_project)
	mkdir 		-p 		$(source_project)
	cp 			-R 		bin/$(project) $(source_project)
	cp 			-R 		Dictionary.desktop $(source_project)
	tar 		-czf 	$(source_project).tar.gz -C $(source_rpm) $(project)-$(project_version)
	rm 			-rf 	$(source_project)
	rpmbuild 	-bb project.spec

appimage:
	rm 		-rf build/opt/application
	mkdir 	-p 	build/opt/application
	cp 		-r 	css build/opt/application
	cp 		-r 	lib build/opt/application
	cp 		-r 	modules build/opt/application
	cp 		-r 	icons build/opt/application
	cp 		-r 	main.py build/opt/application
	find build/opt/application -name '__pycache__' -exec rm -rf {} +
	find build/opt/application -name '.pyc*' -exec rm -rf {} +
	export ARCH=x86_64
	exec bin/appimagetool build bin/Dictionary

