# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
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
from pyparsing import *


class WikiMarkupTable(object):
    def __init__(self):
        self.rows = []
        self.cols = []
        self.values = {}

    def add_row(self, row, col, value):
        """
        
        :param row: 
        :param col: 
        :param value: 
        :return: 
        """
        if row not in self.rows:
            self.rows.append(row)
        if col not in self.cols:
            self.cols.append(col)

        row_index = self.rows.index(row)
        if row_index not in self.values:
            self.values[row_index] = {}

        col_index = self.cols.index(col)
        if col_index not in self.values[row_index]:
            self.values[row_index][col_index] = {}

        self.values[row_index][col_index] = value
        return self

    def __str__(self):
        """
        
        :return: 
        """
        rows = "<th></th>"
        for name in self.cols:
            rows += "<th>%s</th>" % (name)
        rows = "<tr>%s</tr>" % (rows)
        for row_index in self.values:
            row = self.values[row_index]
            row_name = self.rows[row_index]
            columns = "<th>%s</th>" % (row_name)
            for column_index in row:
                column = row[column_index]
                columns += "<td>%s</td>" % (column)
            rows += "<tr>%s</tr>" % (columns)
        return '<table>%s</table>' % (rows)


class WikiMarkup(object):
    @property
    def converters(self):
        """
        
        :return: 
        """
        return [
            QuotedString(" ======", endQuoteChar="====== ").setParseAction(self._h6),
            QuotedString(" =====", endQuoteChar="===== ").setParseAction(self._h5),
            QuotedString(" ====", endQuoteChar="==== ").setParseAction(self._h4),
            QuotedString(" ===", endQuoteChar="=== ").setParseAction(self._h3),
            QuotedString(" ==", endQuoteChar="== ").setParseAction(self._h2),
            QuotedString("'''", endQuoteChar="'''").setParseAction(self._b),
            QuotedString("''", endQuoteChar="''").setParseAction(self._i),
            QuotedString("{{Deutsch Substantiv Übersicht", endQuoteChar="}}").setParseAction(self._t),

            QuotedString("[[", endQuoteChar="]]").setParseAction(self._a),
            QuotedString(":[", endQuoteChar="]").setParseAction(self._e),

            QuotedString("{{Wortbildung|", endQuoteChar="}}").setParseAction(self._wb),
            QuotedString("{{Ref-", endQuoteChar="}}").setParseAction(self._ref),
            QuotedString("{{Wikipedia|", endQuoteChar="}}").setParseAction(self._wiki),
            QuotedString("{{Lautschrift|", endQuoteChar="}}").setParseAction(self._ipa),
            QuotedString("{{Wortart|", endQuoteChar="}}").setParseAction(self._wa),
            QuotedString("{{Sprache|", endQuoteChar="}}").setParseAction(self._lang),
            QuotedString("{{K|", endQuoteChar="}}").setParseAction(self._type),

            QuotedString("{{my", endQuoteChar="}}").setParseAction(lambda l, t: self._text('My', l, t)),
            QuotedString("{{fr", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Fr', l, t)),
            QuotedString("{{cs", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Cs', l, t)),
            QuotedString("{{sv", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sv', l, t)),
            QuotedString("{{ja", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ja', l, t)),
            QuotedString("{{pl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Pl', l, t)),
            QuotedString("{{nl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Nl', l, t)),
            QuotedString("{{en", endQuoteChar="}}").setParseAction(lambda l, t: self._text('En', l, t)),
            QuotedString("{{da", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Da', l, t)),
            QuotedString("{{eo", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Eo', l, t)),
            QuotedString("{{it", endQuoteChar="}}").setParseAction(lambda l, t: self._text('It', l, t)),
            QuotedString("{{lt", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Lt', l, t)),
            QuotedString("{{ru", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ru', l, t)),
            QuotedString("{{uk", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Uk', l, t)),
            QuotedString("{{el", endQuoteChar="}}").setParseAction(lambda l, t: self._text('El', l, t)),
            QuotedString("{{pt", endQuoteChar="}}").setParseAction(lambda l, t: self._text('pt', l, t)),
            QuotedString("{{hsb", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Hsb', l, t)),
            QuotedString("{{es", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Es', l, t)),
            QuotedString("{{wen", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Wen', l, t)),
            QuotedString("{{sq", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sq', l, t)),
            QuotedString("{{cy", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Cy', l, t)),
            QuotedString("{{hu", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Hu', l, t)),
            QuotedString("{{sw", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sw', l, t)),
            QuotedString("{{tr", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Tr', l, t)),
            QuotedString("{{be", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Be', l, t)),
            QuotedString("{{sk", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sk', l, t)),
            QuotedString("{{dsb", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Dsb', l, t)),
            QuotedString("{{ro", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ro', l, t)),
            QuotedString("{{ko", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ko', l, t)),
            QuotedString("{{ar", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ar', l, t)),
            QuotedString("{{yi", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Yi', l, t)),
            QuotedString("{{ga", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ga', l, t)),
            QuotedString("{{io", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Io', l, t)),
            QuotedString("{{zh", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Zh', l, t)),
            QuotedString("{{u", endQuoteChar="}}").setParseAction(lambda l, t: self._text('U', l, t)),
            QuotedString("{{bs", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Bs', l, t)),
            QuotedString("{{az", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Az', l, t)),
            QuotedString("{{ast", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ast', l, t)),
            QuotedString("{{eu", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Eu', l, t)),
            QuotedString("{{bg", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Bg', l, t)),
            QuotedString("{{yue", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Yue', l, t)),
            QuotedString("{{gl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Gl', l, t)),
            QuotedString("{{he", endQuoteChar="}}").setParseAction(lambda l, t: self._text('He', l, t)),
            QuotedString("{{kl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Kl', l, t)),
            QuotedString("{{ka", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ka', l, t)),
            QuotedString("{{aeb", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Aeb', l, t)),
            QuotedString("{{ayl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ayl', l, t)),
            QuotedString("{{Arab", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ar', l, t)),
            QuotedString("{{zu", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Zu', l, t)),
            QuotedString("{{is", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Is', l, t)),
            QuotedString("{{ca", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ca', l, t)),
            QuotedString("{{hr", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Hr', l, t)),
            QuotedString("{{la", endQuoteChar="}}").setParseAction(lambda l, t: self._text('La', l, t)),
            QuotedString("{{oc", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Oc', l, t)),
            QuotedString("{{prs", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Prs', l, t)),
            QuotedString("{{tg", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Tg', l, t)),
            QuotedString("{{rm", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Rm', l, t)),
            QuotedString("{{sr", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sr', l, t)),
            QuotedString("{{am", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Am', l, t)),
            QuotedString("{{ay", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ay', l, t)),
            QuotedString("{{br", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Br', l, t)),
            QuotedString("{{ia", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ia', l, t)),
            QuotedString("{{vec", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Vec', l, t)),
            QuotedString("{{ku", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ku', l, t)),
            QuotedString("{{pap", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Pap', l, t)),
            QuotedString("{{qu", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Qu', l, t)),
            QuotedString("{{sm", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sm', l, t)),
            QuotedString("{{so", endQuoteChar="}}").setParseAction(lambda l, t: self._text('So', l, t)),
            QuotedString("{{th", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Th', l, t)),
            QuotedString("{{tpi", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Tpi', l, t)),
            QuotedString("{{vi", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Vi', l, t)),
            QuotedString("{{vo", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Vo', l, t)),
            QuotedString("{{pfi", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Pfi', l, t)),
            QuotedString("{{pfl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Pfl', l, t)),
            QuotedString("{{ang", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ang', l, t)),
            QuotedString("{{hy", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Hy', l, t)),
            QuotedString("{{bm", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Bm', l, t)),
            QuotedString("{{ceb", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ceb', l, t)),
            QuotedString("{{ch", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ch', l, t)),
            QuotedString("{{et", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Et', l, t)),
            QuotedString("{{gn", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Gn', l, t)),
            QuotedString("{{haw", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Haw', l, t)),
            QuotedString("{{id", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Id', l, t)),
            QuotedString("{{iu", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Iu', l, t)),
            QuotedString("{{jv", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Jv', l, t)),
            QuotedString("{{kg", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Kg', l, t)),
            QuotedString("{{rw", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Rw', l, t)),
            QuotedString("{{kw", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Kw', l, t)),
            QuotedString("{{co", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Co', l, t)),
            QuotedString("{{lo", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Lo', l, t)),
            QuotedString("{{lv", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Lv', l, t)),
            QuotedString("{{lb", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Lb', l, t)),
            QuotedString("{{gv", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Gv', l, t)),
            QuotedString("{{se", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Se', l, t)),
            QuotedString("{{gd", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Gd', l, t)),
            QuotedString("{{sn", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sn', l, t)),
            QuotedString("{{ss", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Ss', l, t)),
            QuotedString("{{scn", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Scn', l, t)),
            QuotedString("{{sl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Sl', l, t)),
            QuotedString("{{tl", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Tl', l, t)),
            QuotedString("{{khb", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Khb', l, t)),
            QuotedString("{{wa", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Wa', l, t)),
            QuotedString("{{vep", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Vep', l, t)),
            QuotedString("{{wo", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Wo', l, t)),
            QuotedString("{{yua", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Yua', l, t)),
            QuotedString("{{als", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Als', l, t)),
            QuotedString("{{bar", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Bar', l, t)),

            QuotedString("{{Ü|", endQuoteChar="}}").setParseAction(self._a),
            QuotedString("{{n", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Neutrum', l, t)),
            QuotedString("{{f", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Femininum', l, t)),
            QuotedString("{{m", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Maskulinum', l, t)),
            QuotedString("{{Pl.", endQuoteChar="}}").setParseAction(lambda l, t: self._text('Plural:', l, t)),
            QuotedString("{{kPl.", endQuoteChar="}}").setParseAction(lambda l, t: self._text('kein Plural', l, t)),
            QuotedString("{{Lit-Kluge:.", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)),

            QuotedString("{{Alternative Schreibweisen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Alternative Schreibweisen', l, t)),
            QuotedString("{{Redewendungen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Redewendungen', l, t)),
            QuotedString("{{Abkürzungen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Abkürzungen', l, t)),
            QuotedString("{{Sinnverwandte Wörter", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Sinnverwandte Wörter', l, t)),
            QuotedString("{{Worttrennung", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Worttrennung', l, t)),
            QuotedString("{{Wortbildungen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Wortbildungen', l, t)),
            QuotedString("{{Aussprache", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Aussprache', l, t)),
            QuotedString("{{IPA", endQuoteChar="}}").setParseAction(lambda l, t: self._text('IPA', l, t)),
            QuotedString("{{Bedeutungen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Bedeutungen', l, t)),
            QuotedString("{{Herkunft", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Herkunft', l, t)),
            QuotedString("{{Synonyme", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Synonyme', l, t)),
            QuotedString("{{Gegenwörter", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Gegenwörter', l, t)),
            QuotedString("{{Oberbegriffe", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Oberbegriffe', l, t)),
            QuotedString("{{Unterbegriffe", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Unterbegriffe', l, t)),
            QuotedString("{{Synonyme", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Synonyme', l, t)),
            QuotedString("{{Beispiele", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Beispiele', l, t)),
            QuotedString("{{Beispiele fehlen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Beispiele fehlen', l, t)),
            QuotedString("{{Referenzen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Referenzen', l, t)),
            QuotedString("{{Bekannte Namensträger", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Bekannte Namensträger', l, t)),
            QuotedString("{{Namensvarianten", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Namensvarianten', l, t)),
            QuotedString("{{Charakteristische Wortkombinationen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Wortkombinationen', l, t)),
            QuotedString("{{Quellen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Quellen', l, t)),
            QuotedString("{{Verkleinerungsformen", endQuoteChar="}}").setParseAction(lambda l, t: self._header('Verkleinerungsformen', l, t)),

            QuotedString("{{Siehe auch|", endQuoteChar="}}").setParseAction(self._s) | \
            QuotedString("{{QS Herkunft", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Ähnlichkeiten", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Ähnlichkeiten", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Deutsch Nachname Übersicht", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Navigationsleiste Anthroponyme", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Absatz", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Übersetzungen", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Üt", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Ü-Tabelle", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Per-", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{DiB-", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Lit-", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Literatur", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Reime", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Reim", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Audio", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Hörbeispiele", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{reg", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{va", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Üxx4", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Üxx5", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{MHA", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{abw", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Internetquelle", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{scherzh", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{abw", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{österr", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{geh", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{Wort der Woche", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{gmh", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)) | \
            QuotedString("{{schweiz", endQuoteChar="}}").setParseAction(lambda l, t: self._text('', l, t)),
        ]

    def _lang(self, l, t):
        """

        :param l: 
        :param t: 
        :return: 
        """
        return '<a href="/%s">%s</a>' % (t[0], t[0])

    def _type(self, l, t):
        """

        :param l: 
        :param t: 
        :return: 
        """
        return '<i>%s</i>' % (t[0])

    def _wb(self, l, t):
        """

        :param text: 
        :param l: 
        :param t: 
        :return: 
        """
        return '<h4>%s</h4>' % (t[0])

    def _wa(self, l, t):
        """

        :param text: 
        :param l: 
        :param t: 
        :return: 
        """
        name, help = t[0].split('|')
        return '<a href="/%s/%s">%s</a>' % (help, name, name)

    def _ipa(self, l, t):
        """

        :param text: 
        :param l: 
        :param t: 
        :return: 
        """
        return '[%s]' % (t[0])

    def _wiki(self, l, t):
        """

        :param text: 
        :param l: 
        :param t: 
        :return: 
        """
        return 'Wikipedia: %s' % (t[0])

    def _ref(self, l, t):
        """

        :param text: 
        :param l: 
        :param t: 
        :return: 
        """
        fields = t[0].split('|')
        if len(fields) == 1:
            return '%s' % fields[0]
        name = fields[0]
        link = fields[1]
        return '%s: %s' % (name, link)

    def _header(self, text, l, t):
        """
        
        :param text: 
        :param l: 
        :param t: 
        :return: 
        """
        return '<h4>%s</h4>' % (text)

    def _text(self, text, l, t):
        """
        
        :param text: 
        :param l: 
        :param t: 
        :return: 
        """
        return '%s' % (text)

    def _s(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return 'Siehe auch: %s ' % t[0]

    def _e(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<br/>[%s]: ' % t[0]

    def _h1(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<h1>%s</h1>' % (t[0])

    def _h2(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<h2>%s</h2>' % (t[0])

    def _h3(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<h3>%s</h3>' % (t[0])

    def _h4(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<h4>%s</h4>' % (t[0])

    def _h5(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<h4>%s</h4>' % (t[0])

    def _h6(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<h4>%s</h4>' % (t[0])

    def _b(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<b>%s</b>' % (t[0])

    def _i(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        return '<i>%s</i>' % (t[0])

    def _a(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        fields = t[0].split('|')
        if len(fields) > 2:
            return '%s: %s' % (
                self.parse(fields[0] if len(fields[0]) else fields[1]),
                self.parse(fields[2] if len(fields[2]) else fields[1]),
            )

        if len(fields) > 1:
            return '<a href="/%s">%s</a>' % (
                self.parse(fields[0] if len(fields[0]) else fields[1]),
                self.parse(fields[1] if len(fields[1]) else fields[0]),
            )

        return '<a href="/%s">%s</a>' % (
            self.parse(t[0]), self.parse(t[0]),
        ) if len(t[0]) else ''

    def _t(self, l, t):
        """
        
        :param l: 
        :param t: 
        :return: 
        """
        result = WikiMarkupTable()
        for field in t[0].split('|'):
            fields = field.split('=')
            if len(fields) > 1:
                table = fields[0]
                value = ' '.join(fields[1:])
                row = table.split(' ')
                if len(row) > 1:
                    result.add_row(row[0], ' '.join(row[1:]), value)
        return result.__str__()

    def parse(self, text):
        """
        
        :param text: 
        :return: 
        """
        result = text
        for convertor in self.converters:
            result = convertor.transformString(result)
        return result


if __name__ == "__main__":
    convertor = WikiMarkup()
    print(convertor.parse('= Heading 1 ='))
    print(convertor.parse('== Heading 2 =='))
    print(convertor.parse('=== Heading 3 ==='))
    print(convertor.parse('==== Heading 4 ===='))
    print(convertor.parse('===== Heading 5 ====='))
    print(convertor.parse('====== Heading 6 ======'))
    print(convertor.parse("''test''"))
    print(convertor.parse("'''test'''"))
    print(convertor.parse("[[link]]"))
    print(convertor.parse("[[link|link name]]"))
    print(convertor.parse("[[link|]]"))
    print(convertor.parse("{{Siehe auch|[[braun]]}}"))
    print(convertor.parse("{{Sprache|Deutsch}}"))
    print(convertor.parse("{{Üt|ja|茶色|}}"))

    print(convertor.parse("{{Deutsch Substantiv Übersicht |Genus=n |Nominativ Singular=Braun |Nominativ Plural=— "
                          "|Genitiv Singular=Brauns |Genitiv Plural=— |Dativ Singular=Braun |Dativ Plural=— "
                          "|Akkusativ Singular=Braun |Akkusativ Plural=— }}").replace("\n", ' '))
