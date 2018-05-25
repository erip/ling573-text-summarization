from .embedder import Embedder

from sklearn.feature_extraction.text import TfidfVectorizer

from .sentence import Sentence

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

@Embedder.register_strategy
class TfidfEmbedder(Embedder):

    name = "tfidf"

    def __init__(self, nlp, sentences):
        super().__init__(nlp)

        self.stopwords = frozenset(stopwords.words('english'))
        self.stemmer = PorterStemmer()

        self.sent2processed_sent = { sentence: self.preprocess_sentence(sentence) for sentence in sentences }

        self.sent_to_index = {s: i for i, s in enumerate(self.sent2processed_sent.values())}
        self.tfidf_matrix = TfidfVectorizer().fit_transform(self.sent2processed_sent.values())

        # Compute the similarity matrix for every sentence
        self.sims = (self.tfidf_matrix * self.tfidf_matrix.T).toarray()

    def preprocess_sentence(self, sentence):
        # Get tokens without stopwords
        tokens = (token.text for token in self.nlp(sentence) if token.text not in self.stopwords)
        # Stem
        stemmed_tokens = map(self.stemmer.stem, tokens)
        # Join naively -- doesn't matter if this is done correctly as long as this is consistent
        return ' '.join(stemmed_tokens)

    def embed(self, sentence):
        preprocessed_sent = self.sent2processed_sent[sentence.text]
        sent_number = self.sent_to_index[preprocessed_sent]
        feature_index = self.tfidf_matrix[sent_number, :].nonzero()[1]
        return self.tfidf_matrix[sent_number, feature_index]

    # Overriding Embedder's `cosine_similarity`
    def cosine_similarity(self, sentence1: Sentence, sentence2: Sentence):
        preprocessed_sent1 = self.sent2processed_sent[sentence1.text]
        preprocessed_sent2 = self.sent2processed_sent[sentence2.text]
        # Pull out the similarity for sentence 1 and sentence 2
        return self.sims[self.sent_to_index[preprocessed_sent1]][self.sent_to_index[preprocessed_sent2]]

    @classmethod
    def from_embedding_config(cls, config, nlp, sentences):
        return cls(nlp, sentences)

if __name__ == "__main__":
    import spacy
    from sentence import Sentence

    nlp = spacy.load('en')
    raw_sents = ["hello, my name is Elijah.", "How are you today?", "I am great, thanks.", "Hi, my name is Elijah"]
    embedder = TfidfEmbedder(raw_sents, nlp)

    embedded_sents = [Sentence("a", "timestamp", sentence, i, nlp, embedder.embed(sentence)) for i, sentence in enumerate(raw_sents)]
    print(embedder.cosine_similarity(embedded_sents[0], embedded_sents[-1]))
