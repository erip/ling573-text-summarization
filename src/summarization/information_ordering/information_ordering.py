#!/usr/bin/env python3

import logging

from itertools import combinations
from collections import Counter

class InformationOrderer(object):
    def __init__(self, experts, expert_weights, threshold=0.5):
        """
        :param experts: a set of experts
        :param expert_weights: a dictionary specifying the weight we place on each expert's prediction.
                               The key of the dictionary is `.Expert.name`.
        :param threshold: the threshold above which we assume the first document in the pair is the better
                          leading document.
        """
        self.logger = logging.getLogger(__name__)

        self.experts = experts
        self.threshold = threshold

        self.logger.debug("Running information ordering with {0}".format(
            ', '.join(expert.name for expert in self.experts))
        )

        self.threshold = threshold

        if sum(expert_weights.values()) != 1.0:
            raise ValueError("The confidences of the experts' weights should sum to 1.0")

        self.expert_weights = expert_weights


    def order(self, doc1, doc2, partial_summary):
        """Given two documents, this method will use the provided experts to order the documents"""

        # Given an expert, its contribution will be its weight times its ordering score.
        expert_weighted_contribution = lambda expert: self.expert_weights.get(expert.name, 0.0) * \
                                                      expert.order(doc1, doc2, partial_summary)

        ordered_weight = sum(expert_weighted_contribution(e) for e in self.experts)

        doc1_first = ordered_weight > self.threshold

        self.logger.debug("Prefer doc1 to doc2? {0}".format(doc1_first))

        return doc1_first

    def order_all(self, sentences):
        ordering = Counter()

        for doc1, doc2 in combinations(sentences, 2):

            prefer_doc1 = self.order(doc1, doc2, sentences)

            preference = doc1 if prefer_doc1 else doc2
            # Update preference
            ordering[preference] += 1

        return list(sorted(ordering, key=ordering.get, reverse=True))