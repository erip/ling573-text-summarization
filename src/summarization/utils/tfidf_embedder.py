from .embedder import Embedder

from sklearn.feature_extraction.text import TfidfVectorizer

from .sentence import Sentence


@Embedder.register_strategy
class TfidfEmbedder(Embedder):

    name = "tfidf"

    def __init__(self, nlp, sentences):
        super().__init__(nlp)
        self.sent_to_index = {s: i for i, s in enumerate(sentences)}
        self.tfidf_matrix = TfidfVectorizer(tokenizer=self._tokenize).fit_transform(sentences)

    def embed(self, sentence):
        if sentence not in self.sent_to_index.keys():
            raise ValueError("Sentence '{0}' has not been seen before.".format(sentence))
        sent_number = self.sent_to_index[sentence]
        feature_index = self.tfidf_matrix[sent_number, :].nonzero()[1]
        return self.tfidf_matrix[sent_number, feature_index]

    # Overriding Embedder's `cosine_similarity`
    def cosine_similarity(self, sentence1: Sentence, sentence2: Sentence):
        # Compute the similarity matrix for every sentence
        sims = (self.tfidf_matrix * self.tfidf_matrix.T).toarray()
        # Pull out the similarity for sentence 1 and sentence 2
        return sims[self.sent_to_index[sentence1.text]][self.sent_to_index[sentence2.text]]

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