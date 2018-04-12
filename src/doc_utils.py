#!/usr/bin/env python3


class Document(object):
    def __init__(self, base_paths, _id):
        self.base_paths = base_paths
        self._id = _id
        self.is_aquaint2 = "_" in _id
        self.is_aquaint = not self.is_aquaint2

        if self.is_aquaint2:
            self.src, self.lang, rest = _id.split("_")
            self.yyyy = rest[0:4]
            self.mm = rest[4:6]
            self.dd = rest[6:8]
        else:
            self.src = _id[0:3]
            self.yyyy = _id[3:7]
            self.mm = _id[7:9]
            self.dd = _id[9:11]

    def id(self):
        return self._id

    def get_path(self):
        if self.is_aquaint:
            # $SRC/$YYYY/$YYYY$mm$dd_$SRC
            return self.base_paths["aquaint"] + \
                   "{0}/{1}/{1}{2}{3}_{4}".format(self.src.lower(), self.yyyy, self.mm, self.dd, self.src)
        else:
            # data/$src_$lang/$src_$lang_$YYYY$mm.xml
            return self.base_paths["aquaint2"] + "data/{0}_{1}/{0}_{1}_{2}{3}.xml".format(self.src, self.lang, self.yyyy, self.mm).lower()


class Docset(object):
    def __init__(self, docset_id, docset):
        self.docset_id = docset_id
        self.docset = docset

    def __iter__(self):
        yield from self.docset

    def __len__(self):
        return len(self.docset)


class Topic(object):
    def __init__(self, _id, title, narrative, docset):
        self._id = _id
        self.title = title
        self.narrative = narrative
        self.docset = docset
        self.stories = set()

    def id(self):
        return self._id

    def add_story(self, story):
        self.stories.add(story)

    def add_stories(self, stories):
        self.stories.update(stories)


class Story(object):
    def __init__(self, headline, sentences):
        self.headline = headline
        self.sentences = sentences

    def get_sentences(self):
        return self.sentences

    def get_headline(self):
        return self.headline


if __name__ == "__main__":
    base_path = "/dropbox/17-18/573/AQUAINT/"
    #id = "NYT_ENG_20041001.0042"
    id = "NYT19990330.0349"
    # doc = Document(id)
    # print(base_path + doc.to_path())
    # print(doc.id())
