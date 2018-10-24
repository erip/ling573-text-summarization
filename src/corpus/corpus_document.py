
import os

class CorpusDocument(object):
    def __init__(self, doc_path, topics):
        self.doc_path = doc_path
        self.topics = topics

    def add_topics(self, topics):
        self.topics.update(topics)

    def topics(self):
        return self.topics