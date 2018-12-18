# -*- coding: utf-8 -*-
"""
Copyright 2008 Serge Matveenko

This file is part of PyStarDict.

PyStarDict is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyStarDict is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyStarDict.  If not, see <http://www.gnu.org/licenses/>.

@author: Serge Matveenko <s@matveenko.ru>
"""
import os
import re
import gzip
import hashlib
import string
import sqlite3
from struct import unpack


class _StarDictIfo(object):
    """
    The .ifo file has the following format:

    StarDict's dict ifo file
    version=2.4.2
    [options]

    Note that the current "version" string must be "2.4.2" or "3.0.0".  If it's not,
    then StarDict will refuse to read the file.
    If version is "3.0.0", StarDict will parse the "idxoffsetbits" option.

    [options]
    ---------
    In the example above, [options] expands to any of the following lines
    specifying information about the dictionary.  Each option is a keyword
    followed by an equal sign, then the value of that option, then a
    newline.  The options may be appear in any order.

    Note that the dictionary must have at least a bookname, a wordcount and a 
    idxfilesize, or the load will fail.  All other information is optional.  All 
    strings should be encoded in UTF-8.

    Available options:

    bookname=      // required
    wordcount=     // required
    synwordcount=  // required if ".syn" file exists.
    idxfilesize=   // required
    idxoffsetbits= // New in 3.0.0
    author=
    email=
    website=
    description=    // You can use <br> for new line.
    date=
    sametypesequence= // very important.
    """
    _prefix = None

    def __init__(self, dict_prefix, container):
        self._prefix = dict_prefix

        try:
            _file = open(self.source)
        except IOError:
            raise Exception('.ifo file does not exists')

        # skipping ifo header
        _file.readline()

        _line = _file.readline().split('=')
        if _line[0] == 'version':
            self.version = _line[1]
        else:
            raise Exception('ifo has invalid format')

        _config = {}
        for _line in _file:
            _line_splited = _line.split('=')
            _config[_line_splited[0]] = _line_splited[1]

        self.bookname = _config.get('bookname', None).strip()
        if self.bookname is None: raise Exception('ifo has no bookname')

        self.wordcount = _config.get('wordcount', None)
        if self.wordcount is None: raise Exception('ifo has no wordcount')
        self.wordcount = int(self.wordcount)

        if self.version == '3.0.0':
            try:
                _syn = open('%s.syn' % dict_prefix)
                self.synwordcount = _config.get('synwordcount', None)
                if self.synwordcount is None:
                    raise Exception('ifo has no synwordcount but .syn file exists')
                self.synwordcount = int(self.synwordcount)
            except IOError:
                pass

        self.idxfilesize = _config.get('idxfilesize', None)
        if self.idxfilesize is None: raise Exception('ifo has no idxfilesize')
        self.idxfilesize = int(self.idxfilesize)

        self.idxoffsetbits = _config.get('idxoffsetbits', 32)
        self.idxoffsetbits = int(self.idxoffsetbits)

        self.author = _config.get('author', '').strip()

        self.email = _config.get('email', '').strip()

        self.website = _config.get('website', '').strip()

        self.description = _config.get('description', '').strip()

        self.date = _config.get('date', '').strip()

        self.sametypesequence = _config.get('sametypesequence', '').strip()

    @property
    def source(self):
        return '%s.ifo' % self._prefix

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class _StarDictIdx(object):
    """
    The .idx file is just a word list.

    The word list is a sorted list of word entries.

    Each entry in the word list contains three fields, one after the other:
         word_str;  // a utf-8 string terminated by '\0'.
         word_data_offset;  // word data's offset in .dict file
         word_data_size;  // word data's total size in .dict file 
    """
    _container = None
    _prefix = None
    _tree = None
    _idx = None

    def __init__(self, dict_prefix, container):
        self._container = container
        self._prefix = dict_prefix

    def __init_dictionary__(self):
        idx_filename, idx_filename_gz = self.source

        try:
            file = open_file(idx_filename, idx_filename_gz)
        except:
            raise Exception('.idx file does not exists')

        """ check file size """
        self._file = file.read()
        if file.tell() != self._container.ifo.idxfilesize:
            raise Exception('size of the .idx file is incorrect')

        """ prepare main dict and parsing parameters """
        self._idx = {}
        idx_offset_bytes_size = int(self._container.ifo.idxoffsetbits / 8)
        idx_offset_format = {4: 'L', 8: 'Q', }[idx_offset_bytes_size]
        idx_cords_bytes_size = idx_offset_bytes_size + 4

        """ parse data via regex """
        record_pattern = r'([\d\D]+?\x00[\d\D]{%s})' % idx_cords_bytes_size
        matched_records = re.findall(record_pattern, self._file)

        """ check records count """
        if len(matched_records) != self._container.ifo.wordcount:
            raise Exception('words count is incorrect')

        """ unpack parsed records """
        for matched_record in matched_records:
            c = matched_record.find('\x00') + 1
            record_tuple = unpack('!%sc%sL' % (c, idx_offset_format), matched_record)
            word, cords = record_tuple[:c - 1], record_tuple[c:]
            self._idx[string.join(word, '')] = cords

    def __getitem__(self, word):
        """
        returns tuple (word_data_offset, word_data_size,) for word in .dict
        @note: here may be placed flexible search realization
        """
        if self._idx is None:
            self.__init_dictionary__()
        return self._idx[word]

    def __contains__(self, k):
        """
        returns True if index has a word k, else False
        """
        if self._idx is None:
            self.__init_dictionary__()
        return k in self._idx

    def __eq__(self, y):
        """
        returns True if hashlib.md5(x.idx) is equal to hashlib.md5(y.idx), else False
        """
        return hashlib.md5(self._file).hexdigest() == hashlib.md5(y._file).hexdigest()

    def __ne__(self, y):
        """
        returns True if hashlib.md5(x.idx) is not equal to hashlib.md5(y.idx), else False
        """
        return not self.__eq__(y)

    @property
    def source(self):
        source = '%s.idx' % self._prefix
        return (source, '%s.gz' % source)

    def words(self):
        if self._idx is None:
            self.__init_dictionary__()
        for word in self._idx.keys():
            index, length = self._idx[word]
            yield word, index, length

    def matches(self, match):
        if self._idx is None:
            self.__init_dictionary__()
        for word in self._idx.keys():
            if len(word) < len(match):
                continue
            if word.find(match) is 0:
                yield word
            if match[0:1].islower():
                if word.find(match.capitalize()) is 0:
                    yield word
                continue
            if word.find(match.lower()) is 0:
                yield word


class _StarDictIdxSQLite(_StarDictIdx):
    _connection = None

    def __init_dictionary__(self):
        idx_filename, idx_filename_gz = self.source

        try:
            file = open_file(idx_filename, idx_filename_gz)
        except:
            raise Exception('.idx file does not exists')

        """ check file size """
        self._file = file.read()
        if file.tell() != self._container.ifo.idxfilesize:
            raise Exception('size of the .idx file is incorrect')

        database = "%s.db" % self._prefix
        if os.path.isfile(database):
            self._connection = sqlite3.connect(database, check_same_thread=False)
            self._connection.text_factory = str
            return

        """ prepare main dict and parsing parameters """
        idx_offset_bytes_size = int(self._container.ifo.idxoffsetbits / 8)
        idx_offset_format = {4: 'L', 8: 'Q', }[idx_offset_bytes_size]
        idx_cords_bytes_size = idx_offset_bytes_size + 4

        """ parse data via regex """
        record_pattern = r'([\d\D]+?\x00[\d\D]{%s})' % idx_cords_bytes_size
        matched_records = re.findall(record_pattern, self._file)

        """ check records count """
        if len(matched_records) != self._container.ifo.wordcount:
            raise Exception('words count is incorrect')

        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.text_factory = str
        self._connection.execute("CREATE TABLE words (word text, start integer, length integer)")
        self._connection.execute("CREATE INDEX IDX_WORD ON words(word)")

        """ unpack parsed records """
        for index, matched_record in enumerate(matched_records):
            c = matched_record.find('\x00') + 1
            record_tuple = unpack('!%sc%sL' % (c, idx_offset_format), matched_record)
            word, cords = record_tuple[:c - 1], record_tuple[c:]
            if not len(word):
                continue

            word = (string.join(word, '')).strip(" \n\t-_;:,.'\"")
            if not len(word):
                continue

            start, length = cords
            self._connection.execute("INSERT INTO words VALUES (?, ?, ?)", (word, start, length))
        self._connection.commit()

    def __getitem__(self, word):
        if self._connection is None:
            self.__init_dictionary__()
        query = "SELECT * FROM words WHERE word = ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word]):
            word, start, length = row
            return [start, length]
        return None

    def __contains__(self, word):
        if self._connection is None:
            self.__init_dictionary__()
        query = "SELECT COUNT(*) FROM words WHERE word = ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word]):
            count, = row
            return count > 0
        return False

    def words(self):
        if self._connection is None:
            self.__init_dictionary__()
        query = "SELECT * FROM words"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, []):
            yield row

    def matches(self, word, limit=30):
        if self._connection is None:
            self.__init_dictionary__()
        query = "SELECT * FROM words WHERE word LIKE ? limit ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word + "%", limit]):
            yield row

class _StarDictDict(object):
    """
    The .dict file is a pure data sequence, as the offset and size of each
    word is recorded in the corresponding .idx file.

    If the "sametypesequence" option is not used in the .ifo file, then
    the .dict file has fields in the following order:
    ==============
    word_1_data_1_type; // a single char identifying the data type
    word_1_data_1_data; // the data
    word_1_data_2_type;
    word_1_data_2_data;
    ...... // the number of data entries for each word is determined by
           // word_data_size in .idx file
    word_2_data_1_type;
    word_2_data_1_data;
    ......
    ==============
    It's important to note that each field in each word indicates its
    own length, as described below.  The number of possible fields per
    word is also not fixed, and is determined by simply reading data until
    you've read word_data_size bytes for that word.

    Suppose the "sametypesequence" option is used in the .idx file, and
    the option is set like this:
    sametypesequence=tm
    Then the .dict file will look like this:
    ==============
    word_1_data_1_data
    word_1_data_2_data
    word_2_data_1_data
    word_2_data_2_data
    ......
    ==============
    The first data entry for each word will have a terminating '\0', but
    the second entry will not have a terminating '\0'.  The omissions of
    the type chars and of the last field's size information are the
    optimizations required by the "sametypesequence" option described
    above.

    If "idxoffsetbits=64", the file size of the .dict file will be bigger 
    than 4G. Because we often need to mmap this large file, and there is 
    a 4G maximum virtual memory space limit in a process on the 32 bits 
    computer, which will make we can get error, so "idxoffsetbits=64" 
    dictionary can't be loaded in 32 bits machine in fact, StarDict will 
    simply print a warning in this case when loading. 64-bits computers 
    should haven't this limit.

    Type identifiers
    ----------------
    Here are the single-character type identifiers that may be used with
    the "sametypesequence" option in the .idx file, or may appear in the
    dict file itself if the "sametypesequence" option is not used.

    Lower-case characters signify that a field's size is determined by a
    terminating '\0', while upper-case characters indicate that the data
    begins with a network byte-ordered guint32 that gives the length of 
    the following data's size(NOT the whole size which is 4 bytes bigger).

    'm'
    Word's pure text meaning.
    The data should be a utf-8 string ending with '\0'.

    'l'
    Word's pure text meaning.
    The data is NOT a utf-8 string, but is instead a string in locale
    encoding, ending with '\0'.  Sometimes using this type will save disk
    space, but its use is discouraged.

    'g'
    A utf-8 string which is marked up with the Pango text markup language.
    For more information about this markup language, See the "Pango
    Reference Manual."
    You might have it installed locally at:
    file:///usr/share/gtk-doc/html/pango/PangoMarkupFormat.html

    't'
    English phonetic string.
    The data should be a utf-8 string ending with '\0'.

    Here are some utf-8 phonetic characters:
    θʃŋʧðʒæıʌʊɒɛəɑɜɔˌˈːˑṃṇḷ
    æɑɒʌәєŋvθðʃʒɚːɡˏˊˋ

    'x'
    A utf-8 string which is marked up with the xdxf language.
    See http://xdxf.sourceforge.net
    StarDict have these extention:
    <rref> can have "type" attribute, it can be "image", "sound", "video" 
    and "attach".
    <kref> can have "k" attribute.

    'y'
    Chinese YinBiao or Japanese KANA.
    The data should be a utf-8 string ending with '\0'.

    'k'
    KingSoft PowerWord's data. The data is a utf-8 string ending with '\0'.
    It is in XML format.

    'w'
    MediaWiki markup language.
    See http://meta.wikimedia.org/wiki/Help:Editing#The_wiki_markup

    'h'
    Html codes.

    'r'
    Resource file list.
    The content can be:
    img:pic/example.jpg     // Image file
    snd:apple.wav           // Sound file
    vdo:film.avi            // Video file
    att:file.bin            // Attachment file
    More than one line is supported as a list of available files.
    StarDict will find the files in the Resource Storage.
    The image will be shown, the sound file will have a play button.
    You can "save as" the attachment file and so on.

    'W'
    wav file.
    The data begins with a network byte-ordered guint32 to identify the wav
    file's size, immediately followed by the file's content.

    'P'
    Picture file.
    The data begins with a network byte-ordered guint32 to identify the picture
    file's size, immediately followed by the file's content.

    'X'
    this type identifier is reserved for experimental extensions.
    """
    _prefix = None

    def __init__(self, dict_prefix, container):
        self._prefix = dict_prefix
        self._container = container

        dict_filename, dict_filename_dz = self.source

        try:
            self._file = open_file(dict_filename, dict_filename_dz)
        except:
            raise Exception('.dict file does not exists')

    def __getitem__(self, word):
        coordinates = self._container.idx[word]
        if coordinates is None:
            return None
        return self.word(coordinates)

    @property
    def source(self):
        source = '%s.dict' % self._prefix
        return (source, '%s.dz' % source)

    def word(self, coordinates):
        self._file.seek(coordinates[0])
        return self._file.read(coordinates[1])


class _StarDictSyn(object):
    _prefix = None

    def __init__(self, dict_prefix, container):
        self._prefix = dict_prefix

        try:
            self._file = open(self.source)
        except IOError:
            pass

    @property
    def source(self):
        return '%s.syn' % self._prefix


class Dictionary(dict):
    """
    Dictionary-like class for lazy manipulating stardict dictionaries

    All items of this dictionary are writable and dict is expandable itself,
    but changes are not stored anywhere and available in runtime only.

    We assume in this documentation that "x" or "y" is instances of the
    StarDictDict class and "x.{ifo,idx{,.gz},dict{,.dz),syn}" or
    "y.{ifo,idx{,.gz},dict{,.dz),syn}" is files of the corresponding stardict
    dictionaries.

    Following documentation is from the "dict" class an is subject to rewrite
    in further impleneted methods:
    """

    def __init__(self, filename_prefix):
        self._dict_cache = {}
        self._match_cache = {}

        self.ifo = _StarDictIfo(dict_prefix=filename_prefix, container=self)
        self.idx = _StarDictIdx(dict_prefix=filename_prefix, container=self)
        self.dict = _StarDictDict(dict_prefix=filename_prefix, container=self)
        self.syn = _StarDictSyn(dict_prefix=filename_prefix, container=self)

    @property
    def source(self):
        collection = []
        for sources in [self.ifo.source, self.idx.source, self.dict.source, self.syn.source]:
            if type(sources) in [list, tuple]:
                for source in sources:
                    collection.append(source)
                continue
            collection.append(sources)
        return collection

    def matches(self, k):
        return self.idx.matches(k)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __contains__(self, k):
        return k in self.idx

    def __delitem__(self, k):
        del self._dict_cache[k]

    def __eq__(self, y):
        return self.idx.__eq__(y.idx)

    def __getitem__(self, k):
        if k in self._dict_cache:
            return self._dict_cache[k]
        value = self.dict[k]
        self._dict_cache[k] = value
        return value

    def __len__(self):
        return self.ifo.wordcount

    def __ne__(self, y):
        return not self.__eq__(y)

    def __repr__(self):
        return u'%s %s' % (self.__class__, self.ifo.bookname)

    def clear(self):
        self._dict_cache = {}
        self._match_cache = {}

    def get(self, k, d=''):
        return self[k] or d

    def has_key(self, k):
        return k in self

    def words(self):
        for word in self.idx.words():
            word, position, length = word
            translation = self.dict.word((position, length))
            yield (word, translation)

    @property
    def name(self):
        return self.ifo.bookname

    @property
    def word_count(self):
        return self.ifo.wordcount


def open_file(regular, gz):
    try:
        return open(regular, 'rb')
    except IOError:
        try:
            return gzip.open(gz, 'rb')
        except IOError:
            raise ValueError('Neither regular nor gz file exists')
