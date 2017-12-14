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


class ParserTreeField(object):
    def __init__(self, rule):
        self.start = rule._start
        self.stop = rule._stop
        self.content = None

        self._rule = rule

    def parse(self, text):
        cache = ""
        index = None
        for index, char in enumerate(text):
            if self.stop in cache:
                break
            cache += char
        self.content = cache.strip("%s%s" % (self.start, self.stop))
        return text[index:]

    def __str__(self):
        return self.content



class ParserRule(object):
    def __init__(self, start, stop):
        self._stop = stop
        self._start = start

    def has(self, string):
        return string == self._start

    def startHas(self, char, position):
        if len(self._start) > position:
            return char == self._start[position]
        return False

    def stopHas(self, char, position):
        if len(self._stop) > position:
            return char == self._stop[position]
        return False

    def __str__(self):
        print "%s...%s" % (self._start, self._stop)


class ParserRuleCollection(object):
    def __init__(self):
        self.collection = []

    def append(self, entity):
        self.collection.append(entity)

    def startHas(self, char, position):
        for entity in self.collection:
            if entity.startHas(char, position):
                return True
        return False

    def stopHas(self, char, position):
        for entity in self.collection:
            if entity.stopHas(char, position):
                return True
        return False

    def rule(self, start):
        for entity in self.collection:
            if entity.has(start):
                return entity
        return None


class ParserTree(object):
    def __init__(self):
        self.rules = ParserRuleCollection()
        self.children = []

    def append(self, entity):
        self.rules.append(entity)

    def __parse(self, text):

        cache_start = ""

        for index, char in enumerate(text):

            char = text[index]
            length_cache_start = len(cache_start)
            if not length_cache_start and self.rules.startHas(char, 0):
                cache_start = char
                index += 1
                continue

            if length_cache_start:
                if self.rules.startHas(char, length_cache_start):
                    cache_start += char
                    index += 1
                    continue

                rule = self.rules.rule(cache_start)
                if rule is None:
                    continue

                return rule, text[index:]


    def parse(self, text):

        while True:
            entity = self.__parse(text)
            if entity is None:
                break

            rule, text = entity
            field = ParserTreeField(rule)
            text = field.parse(text)
            print(len(text), field.__str__())

        for index, field in enumerate(self.children):
            print(index, field.__str__())


if __name__ == "__main__":
    text = """==German==
{{wikipedia|dab=Arbeit|lang=de}}

===Etymology===
From {{inh|de|gmh|arbeit}}, from {{inh|de|goh|arbeit}}, from {{inh|de|gem-pro|*arbaidiz}}. Cognate with {{cog|yi|אַרבעט}}, {{cog|ang|earfoþe}}.

===Pronunciation===
* {{IPA|/ˈaʁbaɪ̯t/|[ˈʔäʁbäɪ̯t]|lang=de}}
* {{audio|De-at-Arbeit.ogg|Audio (Austria)|lang=de}}
* {{audio|De-Arbeit.ogg|Audio|lang=de}}

===Noun===
{{de-noun|f||Arbeiten}}

# [[work]], [[labor]], [[toil]], [[job]]
#: {{ux|de|Seine '''Arbeit''' macht ihm Spaß.|t=He enjoys his '''work'''/'''job'''.}}
# [[job]], [[task]]
# [[performance]], [[workmanship]]
# [[employment]]
# [[effort]]

====Declension====
{{de-decl-noun-f|en}}

====Derived terms====
{{der3|lang=de|{{l|de|arbeiten|pos=v}}
|{{l|de|Arbeiter|g=m}}
|{{l|de|Arbeitgeber|g=m}}
|{{l|de|Arbeitnehmer|g=m}}
|{{l|de|arbeitsam}}
|{{l|de|Arbeitsamt|g=n}}
|{{l|de|Arbeitseifer|g=m}}
|{{l|de|Arbeitseinstellung|g=f}}
|{{l|de|Arbeitsfeld|g=n}}
|{{l|de|Arbeitsgang|g=m}}
|{{l|de|Arbeitsgruppe|g=f}}
|{{l|de|Arbeitshaus|g=n}}
|{{l|de|Arbeitskamerad|g=f}}
|{{l|de|Arbeitskraft|g=f}}, {{l|de|Arbeitskräfte}}
|{{l|de|Arbeitslager|g=n}}
|{{l|de|Arbeitsleistung|g=f}}
|{{l|de|Arbeitslohn|g=m}}
|{{l|de|arbeitslos}}
|{{l|de|Arbeitsmann|g=m}}
|{{l|de|Arbeitsmarkt|g=m}}
|{{l|de|Arbeitsmensch|g=m}}
|{{l|de|Arbeitsniederlegung|g=f}}
|{{l|de|Arbeitsplatz|g=m}}
|{{l|de|Arbeitsschule|g=f}}
|{{l|de|Arbeitstag|g=m}}
|{{l|de|Arbeitstisch|g=m}}
|{{l|de|arbeitsunfähig}}
|{{l|de|Arbeitsvermögen|g=n}}
|{{l|de|arbeitswillig}}
|{{l|de|Arbeitszeit|g=f}}
|{{l|de|Arbeitszeug|g=n}}
|{{l|de|Arbeitszeugnis|g=n}}
|{{l|de|Dreharbeit}}
|{{l|de|Leiharbeit}}
|{{l|de|Sisyphusarbeit}}
|{{l|de|Zwangsarbeit}}
|{{l|de|Arbeitszimmer|g=n}}
|{{l|de|Arbeitsschutz|g=m}}
}}

====Descendants====
* Japanese: {{l|ja|アルバイト|tr=arubaito}} and its clipping {{l|ja|バイト|tr=baito}}
* Korean: {{l|ko|아르바이트|tr=a-reu-ba-i-teu}}
* Icelandic, Faroese: arbeiða
* Swedish: arbete
* Danish: arbejde

===Further reading===
* {{R:Duden}}

"""

    tree = ParserTree()
    tree.append(ParserRule("==", "=="))
    tree.append(ParserRule("===", "==="))
    tree.append(ParserRule("====", "===="))
    tree.append(ParserRule("=====", "====="))
    tree.append(ParserRule("======", "======"))

    tree.append(ParserRule("{{", "}}"))
    tree.append(ParserRule("{{de-noun", "}}"))
    tree.append(ParserRule("{{der3", "\n}}"))

    tree.append(ParserRule("#", "\n"))
    tree.append(ParserRule("*", "\n"))

    print(tree.parse(text))
