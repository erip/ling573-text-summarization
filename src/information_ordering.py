#!/usr/bin/env python3

import logging

class InformationOrderer(object):
    def __init__(self, experts, expert_weights):
        """
        :param experts: a set of experts
        :param expert_weights: a dictionary specifying the weight we place on each expert's prediction.
                               The key of the dictionary is `.Expert.name`.
        """
        self.logger = logging.getLogger(__name__)

        self.experts = experts

        self.logger.debug("Running information ordering with {0}".format(
            ', '.join(expert.name() for expert in self.experts))
        )

        self.expert_weights = expert_weights


    def order(self, doc1, doc2, partial_summary):
        """Given two documents, this method will use the provided experts to order the documents"""

        # Given an expert, its contribution will be its weight times its ordering score.
        expert_weighted_contribution = lambda expert: self.expert_weights.get(expert.name(), 0.0) * \
                                                      expert.order(doc1, doc2, partial_summary)

        ordered_weight = sum(expert_weighted_contribution(e) for e in self.experts)

        doc1_first = ordered_weight > 0.5

        self.logger.debug("Prefer doc1 to doc2? {0}".format(doc1_first))

        return doc1_first