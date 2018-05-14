#!/usr/bin/env python3

import os

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
            # $SRC/$YYYY/$YYYY$mm$dd_$SRC for NYT, $SRC/$YYYY/$YYYY$mm$dd_$SRC_$LANG for xie and apw
            # xie is sometimes xin so hardcoding that too :(
            if self.src == "NYT":
                groups = (self.src.lower(), self.yyyy, "{0}{1}{2}_{3}".format(self.yyyy, self.mm, self.dd, self.src))
            elif self.src == "XIE":
                groups = (self.src.lower(), self.yyyy, "{0}{1}{2}_XIN_ENG".format(self.yyyy, self.mm, self.dd))
            else:
                groups = (self.src.lower(), self.yyyy, "{0}{1}{2}_{3}_ENG".format(self.yyyy, self.mm, self.dd, self.src))
            return os.path.join(self.base_paths["aquaint"], *groups)

        else:
            groups = ("data", "{0}_{1}".format(self.src, self.lang), "{0}_{1}_{2}{3}.xml".format(self.src, self.lang, self.yyyy, self.mm))

            return os.path.join(self.base_paths["aquaint2"], *groups).lower()


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

class Sentence(object):
    def __init__(self, doc_id, doc_timestamp, sentence_object, sent_number, nlp):
        self.document_id = doc_id
        self.doc_timestamp = doc_timestamp
        self.text = sentence_object.text
        self.vector = sentence_object.vector
        self.sent_index = sent_number
        self.nlp = nlp

    def doc_id(self):
        return self.document_id

    def get_timestamp(self):
        return self.doc_timestamp

    def get_sent_index(self):
        return self.sent_index

    def tokens(self):
        return self.nlp(self.text)

class Story(object):
    def __init__(self, headline, sentences):
        """
        A single story from a newspaper
        :param headline: string
        :param sentences: nested list of lists (tokenized into both sentences and words)
        :param raw_text: a block string of the story
        :param spans: a list of tuples of the sentence boundaries
        """
        self.headline = headline
        self.sentences = sentences

    def get_sentences(self):
        return self.sentences

    def get_headline(self):
        return self.headline

    def get_raw(self):
        return ' '.join(sentence.text for sentence in self.sentences)

    def num_sentences(self):
        return len(self.sentences)


if __name__ == "__main__":
    base_path = {
        "aquaint": "/data/aquaint/",
        "aquaint2": "/data/aquaint2/"
    }
    #id = "NYT_ENG_20041001.0042"
    id = "NYT19990330.0349"
    doc = Document(base_path, id)
    print(base_path["aquaint"] + doc.get_path())
    print(doc.id())
