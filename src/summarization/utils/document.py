
from .sentence import Sentence

class Document(object):
    def __init__(self, doc_id, topic, sentences, timestamp = None):
        self.doc_id = doc_id
        self.topic = topic
        self.sentences = [Sentence(i, doc_id, sentence, timestamp) for i, sentence in enumerate(sentences)]