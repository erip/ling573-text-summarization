
from unittest import TestCase

from datetime import datetime, timedelta

from src.experts import *

class Document:
    """A stub document. Actual documents passed into the experts must conform to this interface.
    """
    def __init__(self, _id, sent, index, timestamp=None):
        self._id = _id
        self.sent = sent
        self.index = index
        self.timestamp = timestamp

    def doc_id(self):
        return self._id

    def get_timestamp(self):
        return self.timestamp

    def get_sent_index(self):
        return self.index

"""
        
        elif d1.get_timestamp() == d2.get_timestamp() and not sents_from_same_doc:
            return 0.5
        # otherwise
        return 0"""

class ExpertTestCase(TestCase):

    def test_prefer_older_doc(self):
        expert = ChronologicalExpert()

        doc1_id = "doc1"
        doc2_id = "doc2"

        doc1_sent_idx = 0
        doc2_sent_idx = 1

        t1 = datetime.now()
        t2 = t1 + timedelta(minutes=5)

        # T(u) < T(v)
        self.assertTrue(t1 < t2)

        doc1 = Document(doc1_id, "some dummy string", doc1_sent_idx, t1)
        doc2 = Document(doc2_id, "some other dummy string", doc2_sent_idx, t2)
        self.assertEqual(1, expert.order(doc1, doc2, []))

    def test_prefer_older_sentence(self):
        expert = ChronologicalExpert()

        doc1_id = "doc1"
        doc2_id = "doc1"

        doc1_sent_idx = 0
        doc2_sent_idx = 1

        t1 = datetime.now()
        t2 = t1 + timedelta(minutes=5)

        # [D(u) == D(v)] & [N(u) < N(v)]
        self.assertEqual(doc1_id, doc2_id)
        self.assertTrue(doc1_sent_idx < doc2_sent_idx)

        doc1 = Document(doc1_id, "some dummy string", doc1_sent_idx, t1)
        doc2 = Document(doc2_id, "some other dummy string", doc2_sent_idx, t2)
        self.assertEqual(1, expert.order(doc1, doc2, []))

    def test_no_preference_for_same_timestamp_but_different_doc_ids(self):
        expert = ChronologicalExpert()

        doc1_id = "doc1"
        doc2_id = "doc2"

        doc1_sent_idx = 0
        doc2_sent_idx = 1

        t1 = datetime.now()
        t2 = t1

        # [T(u) == T(v)] & [D(u) != D(v)]
        self.assertEqual(t1, t2)
        self.assertNotEqual(doc1_id, doc2_id)

        doc1 = Document(doc1_id, "some dummy string", doc1_sent_idx, t1)
        doc2 = Document(doc2_id, "some other dummy string", doc2_sent_idx, t2)
        self.assertEqual(0.5, expert.order(doc1, doc2, []))

    def test_no_order_if_one_doc_has_no_timestamp(self):
        expert = ChronologicalExpert()

        doc1_id = "doc1"
        doc2_id = "doc2"

        doc1_sent_idx = 0
        doc2_sent_idx = 1

        t1 = datetime.now()
        t2 = None

        self.assertIsNone(t2)

        doc1 = Document(doc1_id, "some dummy string", doc1_sent_idx, t1)
        doc2 = Document(doc2_id, "some other dummy string", doc2_sent_idx, t2)
        self.assertEqual(0, expert.order(doc1, doc2, []))

    def test_no_order_if_neither_doc_has_a_timestamp(self):
        expert = ChronologicalExpert()

        doc1_id = "doc1"
        doc2_id = "doc2"

        doc1_sent_idx = 0
        doc2_sent_idx = 1

        t1 = None
        t2 = None

        self.assertIsNone(t1)
        self.assertIsNone(t2)

        doc1 = Document(doc1_id, "some dummy string", doc1_sent_idx, t1)
        doc2 = Document(doc2_id, "some other dummy string", doc2_sent_idx, t2)
        self.assertEqual(0, expert.order(doc1, doc2, []))