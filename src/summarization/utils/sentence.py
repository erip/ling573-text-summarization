
from datetime import date

from spacy.language import Language

from spacy.tokens.span import Span as SpacySent

from .embedding import Embedding


class Sentence(object):
    def __init__(self, doc_id: str, doc_timestamp: date, sent: SpacySent, sent_number: int, embedding: Embedding=None):

        self._sent = sent
        self.text = sent.text
        self.document_id = doc_id
        self.doc_timestamp = doc_timestamp
        self.sent_index = sent_number
        self.embedding = embedding

    def doc_id(self):
        return self.document_id

    def text(self):
        return self.text

    def get_timestamp(self):
        return self.doc_timestamp

    def get_sent_index(self):
        return self.sent_index

    def tokens(self):
        return self._sent

