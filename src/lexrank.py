#!/usr/bin/env python3

"""
Borrow heavily from https://github.com/miso-belica/sumy/blob/dev/sumy/summarizers/_summarizer.py

"""

from collections import namedtuple, Counter
from operator import attrgetter

import numpy as np
from sklearn.metrics import pairwise
import spacy

from embeddings import SentenceEmbedding

#GLOBAL SETTINGS
SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rating",))
nlp = spacy.load('en_vectors_web_lg')  #TODO this has to be downloaded in advance and is enormous, need to add to readme
nlp.add_pipe(nlp.create_pipe('sentencizer')) #necessary to recovering sentence boundaries. If we want to speed things up later we can fuck with the sentence boundaries


class ItemsCount(object):
    """This is absolute black magick.
    serif: It appears to be an object oriented way of ensuring we get the top x sentences regardless of whether a
    hard number or a percentage is given. It could almost certainly be done more simply. But apart from headspinning is
    not causing problems.
    """
    def __init__(self, value):
        """a number, or a percentage"""
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

        infos = (SentenceInfo(s, o, rate(s, *args, **kwargs))
            for o, s in enumerate(sentences))

        # sort sentences by rating in descending order
        infos = sorted(infos, key=attrgetter("rating"), reverse=True)
        if not isinstance(count, ItemsCount):
            count = ItemsCount(count)

        infos = count(infos)
        # sort sentences by their order in document.
        #TODO either make it so "document" ordering has meaning, or remove this line.
        #infos = sorted(infos, key=attrgetter("order"))
        sent_list = [i.sentence.raw for i in infos]

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

    def summarize(self, document, num_sentences_count, max_word_count, vec_type='spacy'):
        """
        Generate summary of the document
        :param document: Input document to be summarized - raw string
        :param num_sentences_count: integer number of best sentences to be returned
        :param max_word_count: integer max number of words in summary
        :param vec_type: string to identify the type of vector representation to use for sentenes
        :return: number of best sentences as determined by LexRank
        """

        #tokenize the input document.
        #TODO generalise this so it isn't spacy specific. It's easy.
        spacy_doc = nlp(document)
        # this is now a list of SentenceEmbedding objects where the vector is vec_type
        if vec_type == 'spacy':
            sentences = [SentenceEmbedding(sent.string.strip(), [tok.text for tok in sent], vec_type, sent.vector)
                         for sent in spacy_doc.sents]

        matrix = self._create_matrix(sentences, self.threshold)
        scores = self.power_method(matrix, self.epsilon)
        ratings = dict(zip(sentences, scores))

        return self._get_best_sentences(sentences, num_sentences_count, max_word_count, ratings)

    def _to_words_set(self, words):
        """
        :param words: all words in a sentence
        :return:  set of all words in sentence minus stop-words
        """
        words = map(self.normalize_word, words)
        return [self.stem_word(w) for w in words if w not in self.stop_words]


    def _create_matrix(self, sentences, threshold):
        """
        Creates matrix of shape |sentences|×|sentences|. Based on cosine similarity between sentences

        :param sentences: a list of lists: outer list is sentences, tokenised into inner list which is words.
        :param threshold: float, lexrank hyperparameter
        """
        # create matrix |sentences|×|sentences| filled with zeroes
        sentences_count = len(sentences)
        matrix = np.zeros((sentences_count, sentences_count))
        degrees = np.zeros((sentences_count, ))

        for row_idx in range(sentences_count):
            for col_idx in range(sentences_count):
                matrix[row_idx, col_idx] = self.cosine_similarity(sentences[row_idx].embedding,
                                                                  sentences[col_idx].embedding) # sentences: row_idx will be a list of tokenised words

                if matrix[row_idx, col_idx] > threshold:
                    matrix[row_idx, col_idx] = 1.0
                    degrees[row_idx] += 1
                else:
                    matrix[row_idx, col_idx] = 0

        for row in range(sentences_count):
            for col in range(sentences_count):
                if degrees[row] == 0:
                    degrees[row] = 1

                matrix[row][col] = matrix[row][col] / degrees[row]

        return matrix

    @staticmethod
    def cosine_similarity(sentence1, sentence2):
        """
        Take 2 sentence vectors, compute cosine similarity.
        It's cosine similarity of these two sentences (vectors) A, B computed as cos(x, y) = A . B / (|A| . |B|)

        :param sentence1: vector representation of first sentence
        :param sentence2: vector representation of second sentence
        :rtype: float
        :return: Returns -1.0 for opposite similarity, 1.0 for the same sentence and zero for no similarity between sentences.
        """
        return pairwise.cosine_similarity([sentence1], [sentence2]) #TODO forcing these to be 2D is janky. cleanup

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
