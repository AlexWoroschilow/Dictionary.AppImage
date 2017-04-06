all: prod


deb: clean
	sudo chown -R sensey:sensey build
	mkdir -p build/usr/bin
	mkdir -p build/usr/lib/dictionary
	mkdir -p build/usr/share/applications
	cp -r app build/usr/lib/dictionary
	cp -r config build/usr/lib/dictionary
	cp -r src build/usr/lib/dictionary
	cp -r img build/usr/lib/dictionary
	cp -r opt build/usr/lib/dictionary
	cp -r themes build/usr/lib/dictionary
	cp -r vendor build/usr/lib/dictionary
	cp indicator.py build/usr/lib/dictionary
	cp dictionary.py build/usr/lib/dictionary
	cp Dictionary.desktop build/usr/share/applications
	ln -rs build/usr/lib/dictionary/dictionary.py build/usr/bin/dictionary
	ln -rs build/usr/lib/dictionary/indicator.py build/usr/bin/dictionary-indicator
	find build -name "*.pyc" -exec rm -rf {} \;
	find build -type d -exec chmod 0755 {} \;
	find build -type f -exec chmod 0644 {} \;
	sudo chmod +x build/usr/lib/dictionary/indicator.py
	sudo chmod +x build/usr/lib/dictionary/dictionary.py
	sudo chown -R root:root build/usr/share/applications/Dictionary.desktop
	sudo chown -R root:root build/usr/lib/dictionary
	./dpkg-deb-nodot build dictionary

clean:
	rm -rf build/usr/bin
	rm -rf build/usr/lib