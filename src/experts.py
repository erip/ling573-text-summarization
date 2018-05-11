#!/usr/bin/env python3

from abc import ABC, abstractmethod

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
        elif d1.get_timestamp() == d2.get_timestamp() and not sents_from_same_doc:
            return 0.5
        # otherwise
        return 0