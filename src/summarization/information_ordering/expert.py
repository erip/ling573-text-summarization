#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Iterable

from . import Sentence
import numpy as np
from ..utils import tfidf_embedder
from ..utils import spacy_embedder
from ..utils import embedder

class Expert(ABC):
    """The abstract base class for information ordering experts."""

    @property
    def name(self):
        return self._name

    @abstractmethod
    def order(self, d1, d2, partial_summary):
        """Orders two documents."""

class ChronologicalExpert(Expert):
    def __init__(self):
        self._name = "chronological"

    def order(self, d1: Sentence, d2: Sentence, partial_summary: Iterable[Sentence]):
        sents_from_same_doc = d1.doc_id() == d2.doc_id()
        both_docs_have_time_stamp = d1.get_timestamp() and d2.get_timestamp()
        doc1_sent_index = d1.get_sent_index()
        doc2_sent_index = d2.get_sent_index()

        # T(u) < T(v)
        if both_docs_have_time_stamp and d1.get_timestamp() < d2.get_timestamp():
            return 1
        # [D(u) == D(v)] & [N(u) < N(v)]
        elif sents_from_same_doc and doc1_sent_index < doc2_sent_index:
            return 1
        # [T(u) == T(v)] & [D(u) != D(v)]
        elif both_docs_have_time_stamp and d1.get_timestamp() == d2.get_timestamp() and not sents_from_same_doc:
            return 0.5
        # otherwise
        return 0


class TopicalClosenessExpert(Expert):
    def __init__(self):
        self._name = "topical"

    EMBEDDER_CONFIG_KEY = 'embedder'

    #UNUSED FUNCTION #TODO: remove
    ##TODO: After code refactor: remove this method if able to pass sentences and partial summary as vectors and vector matrix respectively
    def getSimilarity(self, sentence1, sentence2, vec_type):
        '''
        Computes the cosine similarity of vector A and B as A.dot(B)/(magnitude(A) * magnitude(B))
        :param sentence1: vector representation of first sentence
        :param sentence2: vector representation of second sentence
        :return: cosine similarity value
        '''

        if vec_type == "tfidf":
            unique_words1 = frozenset(sentence1.tokens)
            unique_words2 = frozenset(sentence2.tokens)
            common_words = unique_words1 & unique_words2

            numerator = 0.0
            for term in common_words:
               numerator += sentence1.embedding[term]*sentence2.embedding[term] * self.idf_metrics[term]**2

            denominator1 = sum((sentence1.embedding[t]*self.idf_metrics[t])**2 for t in unique_words1)
            denominator2 = sum((sentence2.embedding[t]*self.idf_metrics[t])**2 for t in unique_words2)

            if denominator1 > 0 and denominator2 > 0:
                return numerator / (np.sqrt(denominator1) * np.sqrt(denominator2))
            else:
                return 0.0
        else:
            return pairwise.cosine_similarity([sentence1.embedding],
                                            [sentence2.embedding])

    def getTopic(self, doc: Sentence, all_sentences_matrix, m1):
        '''
        Finds the sentence that is closest to the given sentence by using cosine similarity measure computed for vector A and B as A.dot(B)/(magnitude(A) * magnitude(B))
        :param doc: document as Sentence object
        :param all_sentences_matrix: all sentences in summary as vectors
        :param m1 : vector magnitude of the all_sentences_matrix
        :return: Sentence that has the more similar value to the given document
        '''

        ##TODO: After code refactor: remove if params are vectors/vector matrix

        doc_vector = doc.embedding

        dotPdt = np.dot(all_sentences_matrix, np.transpose(doc_vector))

        #m1 is magnitude of vector d; this is a scalar value
        m2 = np.linalg.norm(doc_vector)
        denominator = m1 * m2
        cosineSimList = np.divide(dotPdt, denominator)
        predictedVecIndex = np.argmax(cosineSimList)
        return all_sentences_matrix[predictedVecIndex]

    def order(self, d1: Sentence, d2: Sentence, partial_summary : Iterable[Sentence]):
        '''
        Return the preference value for the two given sentences d1 and d2
        :param d1: Sentence object for sentence 1
        :param d2: Sentence object for sentence 2
        :param partial_summary: current state of the summary - an iterable of Sentence Objects
        :return: 1, if d1 preferred over d2
                0, if d2 preferred over d1
                0.5, equal preferrence for both documents
        '''

        ##create a matrix of all sentence embeddings

        #Store the norm of each sentence in the magnitude vector to avoid recomputation


        m1 = np.linalg.norm(partial_summary_matrix, axis=1)

        if self.getTopic(d1, partial_summary_matrix, m1) == self.getTopic(d2, partial_summary_matrix, m1):
            return 0.5
        elif self.getTopic(d1, partial_summary_matrix, m1) > self.getTopic(d2, partial_summary_matrix, m1):
            return 1
        else:
            return 0


if __name__ == "__main__":
