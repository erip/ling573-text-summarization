from unittest import TestCase

import spacy

from summarization.utils import Embedder, SpacyEmbedder, TfidfEmbedder

class EmbedderTestCase(TestCase):

    def setUp(self):
        self.nlp = spacy.blank('en')

    def test_embedder_from_config_with_spacy_info(self):
        sentences = ["hello, world"]
        spacy_embedder_config = {
            Embedder.CONFIG_EMBED_NAME_KEY: SpacyEmbedder.name,
        }

        embedder = Embedder.from_config(spacy_embedder_config, self.nlp, sentences)
        self.assertIsInstance(embedder, SpacyEmbedder)

    def test_embedder_from_config_with_tfidf_info(self):
        sentences = ["hello, world"]
        tfidf_embedder_config = {
            Embedder.CONFIG_EMBED_NAME_KEY: TfidfEmbedder.name,
        }

        embedder = Embedder.from_config(tfidf_embedder_config, self.nlp, sentences)
        self.assertIsInstance(embedder, TfidfEmbedder)