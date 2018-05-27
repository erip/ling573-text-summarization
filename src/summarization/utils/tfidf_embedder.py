from typing import Dict, List

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.language import Language

from .embedder import Embedder
from .sentence import Sentence


@Embedder.register_strategy
class TfidfEmbedder(Embedder):

    name = "tfidf"

    def __init__(self, nlp, sentences):
        super().__init__(nlp)

        self.stopwords = frozenset(stopwords.words('english'))
        self.stemmer = PorterStemmer()

        # Cache the preprocessed sentence since calling it is expensive.
        self.sent2processed_sent = { sentence: self.preprocess_sentence(sentence) for sentence in sentences }

        # Map the preprocessed sentence to its location in the tfidf matrix.
        self.sent_to_index = {s: i for i, s in enumerate(self.sent2processed_sent.values())}
        self.tfidf_matrix = TfidfVectorizer().fit_transform(self.sent2processed_sent.values())

        # Compute the similarity matrix for every sentence
        self.sims = (self.tfidf_matrix * self.tfidf_matrix.T).toarray()

    def preprocess_sentence(self, sentence: str):
        """A method to normalize a string sentence.

        Note: this is expensive, so it should not be called often.

        :param sentence: the sentence to be preprocessed
        :return: a normalized sentence
        """
        # Get tokens without stopwords
        tokens = (token.text for token in self.nlp(sentence) if token.text not in self.stopwords)
        # Stem
        stemmed_tokens = map(self.stemmer.stem, tokens)
        # Join naively -- doesn't matter if this is done correctly as long as this is consistent
        return ' '.join(stemmed_tokens)

    def embed(self, sentence: Sentence) -> np.array:
        """Pull out the tf-idf of a sentence from its matrix.
        """
        # Get the preprocessed text from the cache
        preprocessed_sent = self.sent2processed_sent[sentence.text]
        # Find the row of the sentence in the tf-idf matrix
        sent_number = self.sent_to_index[preprocessed_sent]
        # Find the "hot" words in the tf-idf matrix
        feature_index = self.tfidf_matrix[sent_number, :].nonzero()[1]
        # Pull out the weights from the tf-idf matrix
        return self.tfidf_matrix[sent_number, feature_index]

    def cosine_similarity(self, sentence1: Sentence, sentence2: Sentence):
        """Overriding Embedder's `cosine_similarity`
        """
        preprocessed_sent1 = self.sent2processed_sent[sentence1.text]
        preprocessed_sent2 = self.sent2processed_sent[sentence2.text]
        # Pull out the similarity for sentence 1 and sentence 2
        return self.sims[self.sent_to_index[preprocessed_sent1]][self.sent_to_index[preprocessed_sent2]]

    @classmethod
    def from_embedding_config(cls, config: Dict, nlp: Language, sentences: List[str]):
        return cls(nlp, sentences)
