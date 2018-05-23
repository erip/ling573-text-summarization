from .embedder import Embedder

import numpy as np

@Embedder.register_strategy
class SpacyEmbedder(Embedder):

    name = "spacy"

    def __init__(self, nlp):
        super().__init__(nlp)

    def embed(self, sentence):
        return self.nlp(sentence).vector.reshape(1, -1)

    @classmethod
    def from_embedding_config(cls, config, nlp):
        return cls(nlp)

if __name__ == "__main__":

    import spacy
    from sentence import Sentence

    nlp = spacy.load('en')
    raw_sents = ["hello, my name is Elijah.", "How are you today?", "I am great, thanks.", "Hi, my name is Elijah"]
    embedder = SpacyEmbedder(raw_sents, nlp)

    embedded_sents = [Sentence("a", "timestamp", sentence, i, nlp, embedder.embed(sentence)) for i, sentence in enumerate(raw_sents)]
    print(embedder.cosine_similarity(embedded_sents[0], embedded_sents[1]))