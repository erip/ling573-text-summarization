from unittest import TestCase

import spacy

from summarization.utils import Embedder, SpacyEmbedder

class EmbedderTestCase(TestCase):

    def setUp(self):
        self.nlp = spacy.blank('en')

    def test_embedder_from_config_with_spacy_info(self):
        spacy_embedder_config = {
            Embedder.CONFIG_EMBED_NAME_KEY: SpacyEmbedder.name,
        }

        embedder = Embedder.from_config(spacy_embedder_config, self.nlp)
        self.assertIsInstance(embedder, SpacyEmbedder)