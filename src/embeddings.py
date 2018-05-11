""""
Module to generate embeddings.

Command to run:
"""

import argparse
import sys
from collections import Counter

import spacy
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import numpy as np

# GLOBALS
#necessary for spacy package
nlp = spacy.load('en_vectors_web_lg')
nlp.add_pipe(nlp.create_pipe('sentencizer'))

#stemmer and stopwords
stop_words = stopwords.words('english')
stemmer = PorterStemmer()


class SentenceEmbedding(object):
    """A sentence embedding.
    :param raw: the raw string representation of the sentence
    :param tokens: a list of tokens
    :param embed_type: a string representing the type of embedding
    :param embedding: the actual vector
    Options:
        - spacy
        - doc2vec
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

    def set_embedding(self, embedding):
        self.embedding = embedding


# this cannot be a property of sentence embedding since it requires the whole document or document set for idf
def make_tfidf_embeddings(all_sentences, tok_sentences):
    """ take all sentences, and return Sentence Embedding with tfidf vectors for each sentence
    :param all_sentences: a list of all raw sentence strings
    :param tok_sentences: nested list of all sentences in document where a sentences is a list of words
    :return a list of SentenceEmbedding objects and the idf_metrics dict for all of them
    """

    sentences_words = [to_words_set(sent) for sent in tok_sentences]  #sent is the variable for list of words in each sentence

    tf_metrics = compute_tf(sentences_words)
    idf_metrics = compute_idf(sentences_words)
    # when vec_type is tfidf, the SentenceEmbedding.embedding will be the tf_metrics dict and tokens will be tfidf processed
    sentences = [SentenceEmbedding(sent, tokens, 'tfidf', tf)
                 for sent, tokens, tf in zip(all_sentences, sentences_words, tf_metrics)]

    return sentences, idf_metrics


def compute_tf(sentences):
    """take list of lists of words representing sentences, return list of tf metrics for each sentence"""
    tf_values = map(Counter, sentences)

    tf_metrics = []
    for sentence in tf_values:
        metrics = {}
        max_tf = find_tf_max(sentence)

        for term, tf in sentence.items():
            metrics[term] = tf / max_tf

        tf_metrics.append(metrics)

    return tf_metrics


def find_tf_max(terms):
    return max(terms.values()) if terms else 1


def compute_idf(sentences):
    idf_metrics = {}
    sentences_count = len(sentences)

    for sentence in sentences:
        for term in sentence:
            if term not in idf_metrics:
                n_j = sum(1 for s in sentences if term in s)
                idf_metrics[term] = np.log(sentences_count / (1 + n_j))

    return idf_metrics

def to_words_set(words):
    """
    take list of words return stemmed and normalised
    :param words: list of all words in a sentence
    :return: list of all words in sentence, normalized and stemmed, minus stop-words
    """
    words = map(normalize_word, words)
    return [stem_word(w) for w in words if w not in stop_words]


def stem_word(word):
    """take word return stemmed word. stemmer is global"""
    s = stemmer.stem(word)
    return s


def normalize_word(word):
    return word.lower()


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
