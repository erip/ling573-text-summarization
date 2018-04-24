#!/usr/bin/env python3

"""Borrow heavily from https://github.com/miso-belica/sumy/blob/dev/sumy/summarizers/_summarizer.py
"""

from collections import namedtuple, Counter
from operator import attrgetter

import numpy as np
from nltk.tokenize.moses import MosesDetokenizer

SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rating",))

class ItemsCount(object):
    """This is absolute black magick.
    """
    def __init__(self, value):
        self._value = value

    def __call__(self, sequence):
        string_types = (bytes, str,)
        if isinstance(self._value, string_types):
            if self._value.endswith("%"):
                total_count = len(sequence)
                percentage = int(self._value[:-1])
                # at least one sentence should be chosen
                count = max(1, total_count*percentage // 100)
                return sequence[:count]
            else:
                return sequence[:int(self._value)]
        elif isinstance(self._value, (int, float)):
            return sequence[:int(self._value)]
        else:
            ValueError("Unsuported value of items count '%s'." % self._value)

    def __repr__(self):
        return "<ItemsCount: %r>".format(self._value)

class AbstractSummarizer(object):
    def __init__(self, stemmer):
        self._stemmer = stemmer

    def __call__(self, document, sentences_count):
        raise NotImplementedError("This method should be overriden in subclass")

    def stem_word(self, word):
        s = self._stemmer.stem(word)
        return s

    def normalize_word(self, word):
        return word.lower()

    def _get_best_sentences(self, sentences, count, max_word_count, rating, *args, **kwargs):
        """

        :param sentences: input document to be summarized - TODO - add here the format of document
        :param count: int for number of best sentences to be chosen from sentences list
        :param max_word_count: int for max words in summary
        :param rating: sentence rating
        :param args:
        :param kwargs: tuple of final summary sentences
        :return:
        """
        rate = rating
        if isinstance(rating, dict):
            assert not args and not kwargs
            rate = lambda s: rating[s]

        infos = (SentenceInfo(s, o, rate(s, *args, **kwargs))
            for o, s in enumerate(sentences))

        # sort sentences by rating in descending order
        infos = sorted(infos, key=attrgetter("rating"), reverse=True)
        if not isinstance(count, ItemsCount):
            count = ItemsCount(count)

        infos = count(infos)
        # sort sentences by their order in document
        infos = sorted(infos, key=attrgetter("order"))
        sent_list = [i.sentence for i in infos]

        #output word count check
        '''if self.check_below_threshold(sent_list):
            # get `count` first best rated sentences
            #TODO: add more sentences if word count below 100
            return tuple(sent_list)
        else:
            #clipped summary
            n = self.get_output_sentence_count(sent_list)
            return tuple(sent_list[:n+1])
        '''
        return tuple(sent_list)

class LexRankSummarizer(AbstractSummarizer):
    """
    LexRank: Graph-based Centrality as Salience in Text Summarization
    Source: http://tangra.si.umich.edu/~radev/lexrank/lexrank.pdf
    """
    def __init__(self, stemmer, threshold=0.1, epsilon=0.1, stop_words=None):
        super().__init__(stemmer)
        self.threshold = threshold
        self.epsilon = epsilon
        self.stop_words = stop_words if stop_words is not None else frozenset()

    def summarize(self, document, num_sentences_count,max_word_count):
        """
        Generate summary of the document
        :param document: Input document to be summarized
        :param num_sentences_count: number of best sentences to be returned
        :return: num_sentences_count number of best sentences as determined by LexRank
        """
        sentences_words = [self._to_words_set(sent) for sent in document]  #sent is the variable for list of words in each sentence

        if not sentences_words:
            return tuple()

        tf_metrics = self._compute_tf(sentences_words)
        idf_metrics = self._compute_idf(sentences_words)

        matrix = self._create_matrix(sentences_words, self.threshold, tf_metrics, idf_metrics)
        scores = self.power_method(matrix, self.epsilon)
        detokenizer = MosesDetokenizer()
        detokenized_sents = [detokenizer.detokenize(sent, return_str=True) for sent in document]

        ratings = dict(zip(detokenized_sents, scores))

        return self._get_best_sentences(detokenized_sents, num_sentences_count, max_word_count, ratings)

    def _to_words_set(self, words):
        """
        :param words: all words in a sentence
        :return:  set of all words in sentence minus stop-words
        """
        words = map(self.normalize_word, words)
        return [self.stem_word(w) for w in words if w not in self.stop_words]

    def _compute_tf(self, sentences):
        tf_values = map(Counter, sentences)

        tf_metrics = []
        for sentence in tf_values:
            metrics = {}
            max_tf = self._find_tf_max(sentence)

            for term, tf in sentence.items():
                metrics[term] = tf / max_tf

            tf_metrics.append(metrics)

        return tf_metrics

    @staticmethod
    def _find_tf_max(terms):
        return max(terms.values()) if terms else 1

    @staticmethod
    def _compute_idf(sentences):
        idf_metrics = {}
        sentences_count = len(sentences)

        for sentence in sentences:
            for term in sentence:
                if term not in idf_metrics:
                    n_j = sum(1 for s in sentences if term in s)
                    idf_metrics[term] = np.log(sentences_count / (1 + n_j))

        return idf_metrics

    def _create_matrix(self, sentences, threshold, tf_metrics, idf_metrics):
        """
        Creates matrix of shape |sentences|×|sentences|.
        """
        # create matrix |sentences|×|sentences| filled with zeroes
        sentences_count = len(sentences)
        matrix = np.zeros((sentences_count, sentences_count))
        degrees = np.zeros((sentences_count, ))

        for row, (sentence1, tf1) in enumerate(zip(sentences, tf_metrics)):
            for col, (sentence2, tf2) in enumerate(zip(sentences, tf_metrics)):
                matrix[row, col] = self.cosine_similarity(sentence1, sentence2, tf1, tf2, idf_metrics)

                if matrix[row, col] > threshold:
                    matrix[row, col] = 1.0
                    degrees[row] += 1
                else:
                    matrix[row, col] = 0

        for row in range(sentences_count):
            for col in range(sentences_count):
                if degrees[row] == 0:
                    degrees[row] = 1

                matrix[row][col] = matrix[row][col] / degrees[row]

        return matrix

    @staticmethod
    def cosine_similarity(sentence1, sentence2, tf1, tf2, idf_metrics):
        """
        We compute idf-modified-cosine(sentence1, sentence2) here.
        It's cosine similarity of these two sentences (vectors) A, B computed as cos(x, y) = A . B / (|A| . |B|)
        Sentences are represented as vector TF*IDF metrics.
        :param sentence1:
            Iterable object where every item represents word of 1st sentence.
        :param sentence2:
            Iterable object where every item represents word of 2nd sentence.
        :type tf1: dict
        :param tf1:
            Term frequencies of words from 1st sentence.
        :type tf2: dict
        :param tf2:
            Term frequencies of words from 2nd sentence
        :type idf_metrics: dict
        :param idf_metrics:
            Inverted document metrics of the sentences. Every sentence is treated as document for this algorithm.
        :rtype: float
        :return:
            Returns -1.0 for opposite similarity, 1.0 for the same sentence and zero for no similarity between sentences.
        """
        unique_words1 = frozenset(sentence1)
        unique_words2 = frozenset(sentence2)
        common_words = unique_words1 & unique_words2

        numerator = 0.0
        for term in common_words:
            numerator += tf1[term]*tf2[term] * idf_metrics[term]**2

        denominator1 = sum((tf1[t]*idf_metrics[t])**2 for t in unique_words1)
        denominator2 = sum((tf2[t]*idf_metrics[t])**2 for t in unique_words2)

        if denominator1 > 0 and denominator2 > 0:
            return numerator / (np.sqrt(denominator1) * np.sqrt(denominator2))
        else:
            return 0.0

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
