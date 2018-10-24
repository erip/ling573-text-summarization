
from datetime import date

import numpy as np
import spacy
from spacy.tokens.span import Span as SpacySent


class Sentence(object):
    def __init__(self, sent: SpacySent, sent_number: int, embedding: np.array=None):

        self._sent = sent
        self.text = sent.text
        self.sent_index = sent_number
        self.embedding = embedding

    def __len__(self):
        """returns word count in sentence, does not count tokens unless entirely alphanumeric"""
        return len(list(filter(str.isalnum, [token.text for token in self.tokens()])))


    def text(self):
        return self.text

    def get_sent_index(self):
        return self.sent_index

    def tokens(self):
        return self._sent


class Sentencizer:
    def __init__(self, boundary_char_set):
        self.boundary_char_set = boundary_char_set

    def sbd(self, doc):
        """used in pipelines for sentence boundary detection"""
        for i, token in enumerate(doc[:-1]):
            if token.text in self.boundary_char_set:
                doc[i + 1].sent_start = True
            else:
                doc[i + 1].sent_start = False
        return doc