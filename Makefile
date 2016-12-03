all: prod


deb: clean
	sudo chown -R sensey:sensey build
	mkdir -p build/usr/bin
	mkdir -p build/usr/lib/dictionary-indicator
	cp -r themes build/usr/lib/dictionary-indicator
	cp -r vendor build/usr/lib/dictionary-indicator
	cp dictionary-indicator.py build/usr/lib/dictionary-indicator
	ln -rs build/usr/lib/dictionary-indicator/dictionary-indicator.py build/usr/bin/dictionary-indicator
	find build -name "__pycache__" -exec rm -rf {} \;
	find build -name "*.pyc" -exec rm -rf {} \;
	find build -type d -exec chmod 0755 {} \;
	find build -type f -exec chmod 0644 {} \;
	sudo chmod +x build/usr/lib/dictionary-indicator/dictionary-indicator.py
	./dpkg-deb-nodot build dictionary-indicator

clean:
	rm -rf build/usr/bin
	rm -rf build/usr/lib