""""
Module to generate embeddings.

Command to run:
"""

import argparse
import sys

import spacy

# GLOBALS
#necessary for spacy package
nlp = spacy.load('en_vectors_web_lg')
nlp.add_pipe(nlp.create_pipe('sentencizer'))


class SentenceEmbedding(object):
    """A sentence embedding.
    :param raw: the raw string representation of the sentence
    :param tokens: a list of tokens
    :param embed_type: a string representing the type of embedding
    :param embedding: the actual vector
    Options:
        - spacy
        - tfidf
    """
    def __init__(self, raw=None, tokens=None, embed_type=None, embedding=None):
        self.raw = raw
        self.tokens = tokens
        self.embed_type = embed_type
        self.embedding = embedding

    def __len__(self):
        """return dimensions of embedding vector"""
        if self.embedding is not None:
            return len(self.embedding)
        else:
            return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('type', help='Options: '
                                'tfidf '
                                'spacy '
                                '...', default='tfidf')
    args = p.parse_args()

    test_sent = ["I must not fear.", "Fear is the mind-killer.",
                 "Fear is the little death that brings total obliteration."]
    test_doc = 'I must not fear. Fear is the mind-killer. Fear is the little death that brings total obliteration. ' \
               'I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will ' \
               'turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain.'

    if args.type == 'spacy':
        doc = nlp(test_doc)
        #print(len(doc.vector))
        embeddings = [SentenceEmbedding(sent.string.strip(), 'spacy') for sent in doc.sents]
        for i in embeddings:
            for j in embeddings:
                print(i.embedding, j.embedding, len(i), len(j))
