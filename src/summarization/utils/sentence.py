
from datetime import date

from spacy.language import Language

from .embedding import Embedding


class Sentence(object):
    def __init__(self, doc_id: str, doc_timestamp: date, text: str, sent_number: int, nlp: Language,
                 embedding: Embedding=None):

        self.nlp = nlp
        self.__sentence = self.nlp(text)
        self.document_id = doc_id
        self.doc_timestamp = doc_timestamp
        self.text = self.__sentence.text
        self.sent_index = sent_number
        self.embedding = embedding

    def doc_id(self):
        return self.document_id

    def get_timestamp(self):
        return self.doc_timestamp

    def get_sent_index(self):
        return self.sent_index

    def tokens(self):
        return self.nlp(self.text)

    def get_embedding(self):
        return self.embedding

