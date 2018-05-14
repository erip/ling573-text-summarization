#!/usr/bin/env python3

import numpy as np

from abc import ABC, abstractmethod
from embeddings import SentenceEmbedding, make_tfidf_embeddings
from sklearn.metrics import pairwise

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

    def order(self, d1, d2, partial_summary):
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

    ##TODO: After code refactor: remove this method if able to pass sentences and partial summary as vectors and vector matrix respectively
    def getSimilarity(self,sentence1,sentence2,vec_type):
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

    def getTopic(self,d,all_sentences_matrix,m1):
        '''
        Finds the sentence that is closest to the given sentence by using cosine similarity measure computed for vector A and B as A.dot(B)/(magnitude(A) * magnitude(B))
        :param d: vector representation of document
        :param all_sentences_matrix: all sentences in summary as vectors
        :param m1 : vector magnitude of the all_sentences_matrix
        :return: Sentence that has the more similar value to the given document
        '''

        ##TODO: After code refactor: remove if params are vectors/vector matrix
        '''max_sent = ""
        max_value = -99999
        for sent in all_sentences_matrix:
            this_value = self.getSimilarity(d,sent)
            if this_value > max_value:
                max_value = this_value
                max_sent = sent

        return max_sent'''

        dotPdt = np.dot(all_sentences_matrix,np.transpose(d))

        #m1 is magnitude of vector d; this is a scalar value
        m2 = np.linalg.norm(d)
        denominator = m1 * m2
        cosineSimList = np.divide(dotPdt,denominator)
        predictedVecIndex = np.argmax(cosineSimList)
        return all_sentences_matrix[predictedVecIndex]


    def order(self, d1, d2, partial_summary_matrix):
        '''
        Return the preference value for the two given sentences d1 and d2
        :param d1: vector for sentence 1
        :param d2: vector for sentence 2
        :param partial_summary: current state of the summary - a nested list of sentence vectors
        :return: 1, if d1 preferred over d2
                0, if d2 preferred over d1
                0.5, equal preferrence for both documents
        '''

        m1 = np.linalg.norm(partial_summary_matrix, axis=1)

        if self.getTopic(d1,partial_summary_matrix,m1) == self.getTopic(d2,partial_summary_matrix,m1):
            return 0.5
        elif self.getTopic(d1,partial_summary_matrix,m1) > self.getTopic(d2,partial_summary_matrix,m1):
            return 1
        else:
            return 0
