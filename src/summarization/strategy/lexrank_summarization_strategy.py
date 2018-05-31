from .summarization_strategy import SummarizationStrategy

from typing import TypeVar, Type, Dict, Set, Iterable

T = TypeVar("T", bound="SummarizationStrategy")

from .lexrank import LexRankSummarizer

from spacy.language import Language

from nltk.stem import PorterStemmer

from . import Document, Sentence, Embedder

@SummarizationStrategy.register_strategy
class LexRankSummarizationStrategy(SummarizationStrategy):

    def __init__(self, embedder_config, threshold, epsilon, similarity_threshold, nlp):
        stemmer = PorterStemmer()
        self.similarity_threshold = similarity_threshold
        self.lexrank = LexRankSummarizer(stemmer, embedder_config, threshold, epsilon, nlp)

    name = "lexrank"

    EMBEDDER_CONFIG_KEY = "embedder"
    THRESHOLD_CONFIG_KEY = "threshold"
    EPSILON_CONFIG_KEY = "epsilon"
    REDUNDANCY_THRESHOLD_KEY = "redundancy_tuner"  #comment out to turn off redundany removal based on thresholding

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict], nlp: Language) -> T:
        embedder_name = config.get(LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY)

        if embedder_name is None:
            raise ValueError("No lexrank strategy config entry for '{0}'".format(LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY))


        threshold = float(config.get(LexRankSummarizationStrategy.THRESHOLD_CONFIG_KEY) or 0.1)
        epsilon = float(config.get(LexRankSummarizationStrategy.EPSILON_CONFIG_KEY) or 0.1)
        embedder_config = config.get(LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY)
        similarity_threshold = float(config.get(LexRankSummarizationStrategy.REDUNDANCY_THRESHOLD_KEY) or 1.0)

        return cls(embedder_config, threshold, epsilon, similarity_threshold, nlp)


    def get_candidate_sentences(self, docs: Iterable[Document], word_limit: int) -> Iterable[Sentence]:

        sent_list = self.lexrank.summarize(docs)

        #near full-sentence redundancy removal during selecting top ranked sentences within word-limit
        sent_list_no_duplicates = self.lexrank.remove_duplicate_sent(sent_list, self.similarity_threshold)

        return self.take_while_under_word_count(sent_list_no_duplicates, word_limit)
