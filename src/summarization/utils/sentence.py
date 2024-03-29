
from datetime import date

import numpy as np
from spacy.tokens.span import Span as SpacySent

class Sentence(object):
    def __init__(self, doc_id: str, doc_timestamp: date, sent: SpacySent, sent_number: int, embedding: np.array=None):

        self._sent = sent
        self.text = sent.text
        self.document_id = doc_id
        self.doc_timestamp = doc_timestamp
        self.sent_index = sent_number
        self.embedding = embedding

    def __len__(self):
        """returns word count in sentence, does not count tokens unless entirely alphanumeric"""
        return len(list(filter(str.isalnum, [token.text for token in self.tokens()])))

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

