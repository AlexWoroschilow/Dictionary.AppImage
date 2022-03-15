
# Dictionary (Prototype)

This is a free open source dictionary program for linux. 

The first version used the stardict dictionary format but then i decided to switch to the simple sqlite db for the dictionaries. 

There are a converter to actually convert the stardict format to sqlite - db (currently broken)


### Features
- translate words using the text field
- translate words by double click at any words in any text (as a popup)
- show similar words and sentences
- export history into csv format
- export history into anki format
- statistic as a calendar 
- simple dictionary format - sqlite db
- convertor from the stardict to sqlite db (currently broken)
- dictionary management
- themes

### Planned features
- dictionary manager to download / enable / disable dictionaries
- grab wiktionary and use these dictionaries by default
- ocr and text recognition + translation


### How to run
To be able to run the programm you will need the python3 and python3-virtualenv installed

Install required modules: `make init`

Activate python virtual environment: `source venv/bin/activate`

Run the programm: `python3 src/main.py`

### How to build an AppImage
To be able to run the programm you will need the python3 and python3-virtualenv installed.

Leave virtual environment: `deactivate`

Build appimage: `make`

Run the program: `bin/Dictionary.AppImage`




### Screenshots

![Dashboard](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/translations.png)
![History](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/history.png)
![Statistic](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/statistic.png)
![Popup](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/popup.framed.png)
![Frameless popup](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/popup.frameless.png)
![Menu](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/menu.dictionaries.png)
![Themes](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/menu.themes.png)
![Popup](https://github.com/AlexWoroschilow/AOD-Dictionary/raw/master/screenshot/popup.gif)

