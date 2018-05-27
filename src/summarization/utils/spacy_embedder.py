from typing import Dict, List

from .embedder import Embedder
from .sentence import Sentence

import numpy as np
from spacy.language import Language

@Embedder.register_strategy
class SpacyEmbedder(Embedder):

    name = "spacy"

    def __init__(self, nlp: Language):
        super().__init__(nlp)

    def embed(self, sentence: Sentence) -> np.array:
        """Returns the GLoVe vector of a sentence's tokens.

        :param sentence: the sentence to be embedded
        :return: the GLoVe vector
        """
        return sentence.tokens().vector.reshape(1, -1)

    @classmethod
    def from_embedding_config(cls, config: Dict, nlp: Language, sentences: List[str]):
        """Creates a SpaCy embedder with the language object. Sentences are
        not needed globally for embedding, so they are ignored.

        :param config: the config to optionally use
        :param nlp: the SpaCy language model
        :param sentences: a list of raw strings
        :return:
        """
        return cls(nlp)