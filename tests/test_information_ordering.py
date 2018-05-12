from unittest import TestCase


from src.summarization.information_ordering.information_ordering import InformationOrderer

from .example_expert import ExampleExpert

class InformationOrderingTestCase(TestCase):

    def test_information_orderer_throws_when_weights_do_not_sum_to_one(self):
        expert = ExampleExpert()
        experts = { expert }

        # Weights should sum to 1.0...
        weights = { expert.name: 1.1 }

        with self.assertRaises(ValueError):
            information_orderer = InformationOrderer(experts, weights)

    def test_example_expert_orders_first_doc_first(self):
        expert = ExampleExpert()
        experts = { expert }

        weights = { expert.name: 1.0 }

        doc1 = "first"
        doc2 = "second"
        partial_summary = []
        information_orderer = InformationOrderer(experts, weights)
        doc1_preferred = information_orderer.order(doc1, doc2, partial_summary)
        self.assertTrue(doc1_preferred)