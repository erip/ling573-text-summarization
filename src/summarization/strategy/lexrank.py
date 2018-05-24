#!/usr/bin/env python3

"""
Borrow heavily from https://github.com/miso-belica/sumy/blob/dev/sumy/summarizers/_summarizer.py

"""

import sys
from collections import namedtuple
from operator import attrgetter

import numpy as np

from . import Document, Embedder

from typing import Iterable

from itertools import product

SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rating",))

class AbstractSummarizer(object):
    def __init__(self, stemmer):
        self._stemmer = stemmer

    def _get_best_sentences(self, sentences, rating, *args, **kwargs):
        """

        :param sentences: list of SentenceEmbedding objects. If we prefer later on, this could be raw
        sentences, there is no reason they *need* to be objects at this point.
        :param count: int for number of best sentences to be chosen from sentences list
        :param max_word_count: int for max words in summary
        :param rating: sentence rating
        :param args:
        :param kwargs: tuple of final summary sentences
        :return:
        """
        #TODO consider moving max_word_count here from the lexrank driver. Post discussion around where it belongs. Leaving here for now as changing it is not important
        #TODO why args and kwargs??
        rate = rating
        if isinstance(rating, dict):
            assert not args and not kwargs
            rate = lambda s: rating[s]

        infos = (SentenceInfo(s, o, rate(s, *args, **kwargs)) for o, s in enumerate(sentences))

        # sort sentences by rating in descending order
        infos = sorted(infos, key=attrgetter("rating"), reverse=True)

        sent_list = [i.sentence for i in infos]

        return tuple(sent_list)

class LexRankSummarizer(AbstractSummarizer): #TODO stemmer and stopwords are now in embeddings
    """
    LexRank: Graph-based Centrality as Salience in Text Summarization
    Source: http://tangra.si.umich.edu/~radev/lexrank/lexrank.pdf
    """
    def __init__(self, stemmer, embedder_config, threshold, epsilon, nlp):
        super().__init__(stemmer)

        self.embedder_config = embedder_config
        self.nlp = nlp

        self.threshold = threshold or 0.1
        self.epsilon = epsilon or 0.1

    def summarize(self, docs: Iterable[Document]):
        """
        Generate summary of the document
        :param document: Input document to be summarized - raw string
        :param num_sentences_count: integer number of best sentences to be returned
        :param max_word_count: integer max number of words in summary
        :param vec_type: string to identify the type of vector representation to use for sentences
        :param model: if using a model to generate embeddings, can include it here
        :return: number of best sentences as determined by LexRank
        """

        #tokenize the input document. This requires a full (not very fast) spacy load as it uses a dependency parse

        sentences = [sent for doc in docs for sent in doc.sentences]

        raw_sentences = [sent.text for sent in sentences]
        embedder = Embedder.from_config(self.embedder_config, self.nlp, raw_sentences)

        for sent in sentences:
            sent.embedding = embedder.embed(sent)

        matrix = self._create_matrix(embedder, sentences, self.threshold)
        scores = self.power_method(matrix, self.epsilon)
        ratings = dict(zip(sentences, scores))

        return self._get_best_sentences(sentences, ratings)


    def _create_matrix(self, embedder, sentences, threshold):
        """
        Creates matrix of shape |sentences|×|sentences|. Based on cosine similarity between sentences

        :param sentences: a list of sentence embedding objects
        :param threshold: float, lexrank hyperparameter
        """
        # create matrix |sentences|×|sentences| filled with zeroes
        sentences_count = len(sentences)

        matrix = np.zeros((sentences_count, sentences_count))
        degrees = np.zeros((sentences_count, ))

        for row_idx, col_idx in product(range(sentences_count), repeat=2):
            matrix[row_idx, col_idx] = self._cosine_similarity(embedder, sentences[row_idx],
                                                              sentences[col_idx])

            if matrix[row_idx, col_idx] > threshold:
                matrix[row_idx, col_idx] = 1.0
                degrees[row_idx] += 1
            else:
                matrix[row_idx, col_idx] = 0

        for row, col in product(range(sentences_count), repeat=2):
            if degrees[row] == 0:
                degrees[row] = 1

            matrix[row][col] = matrix[row][col] / degrees[row]

        return matrix

    def _cosine_similarity(self, embedder, sentence1, sentence2):
        """
        Take 2 sentence vectors, compute cosine similarity.
        It's cosine similarity of these two sentences (vectors) A, B computed as cos(x, y) = A . B / (|A| . |B|)

        :param sentence1: vector representation of first sentence
        :param sentence2: vector representation of second sentence
        :rtype: float
        :return: Returns -1.0 for opposite similarity, 1.0 for the same sentence and zero for no similarity between sentences.
        """
        return embedder.cosine_similarity(sentence1, sentence2)

    @staticmethod
    def power_method(matrix, epsilon):
        transposed_matrix = matrix.T
        sentences_count = len(matrix)
        p_vector = np.array([1.0 / sentences_count] * sentences_count)
        lambda_val = 1.0

        while lambda_val > epsilon:
            next_p = np.dot(transposed_matrix, p_vector)
            lambda_val = np.linalg.norm(np.subtract(next_p, p_vector))
            p_vector = next_p

        return p_vector
