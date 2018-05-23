from .summarization_strategy import SummarizationStrategy

from typing import TypeVar, Type, Dict, Set, Iterable

T = TypeVar("T", bound="SummarizationStrategy")

from .lexrank import LexRankSummarizer

from spacy.language import Language

from nltk.stem import PorterStemmer

from . import Document, Sentence, Embedder

@SummarizationStrategy.register_strategy
class LexRankSummarizationStrategy(SummarizationStrategy):

    def __init__(self, embedder, threshold, epsilon, num_sentence_count):
        stemmer = PorterStemmer()
        self.lexrank = LexRankSummarizer(stemmer, embedder, threshold, epsilon, num_sentence_count)

    name = "lexrank"

    EMBEDDER_CONFIG_KEY = "embedder"
    THRESHOLD_CONFIG_KEY = "threshold"
    EPSILON_CONFIG_KEY = "epsilon"
    NUM_SENTENCE_COUNT = "num_sentence_count"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict], nlp: Language) -> T:
        embedder_name = config.get(LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY)

        if embedder_name is None:
            raise ValueError("No lexrank strategy config entry for '{0}'".format(LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY))

        threshold = float(config.get(LexRankSummarizationStrategy.THRESHOLD_CONFIG_KEY) or 0.1)
        epsilon = float(config.get(LexRankSummarizationStrategy.EPSILON_CONFIG_KEY) or 0.1)
        num_sentence_count = float(config.get(LexRankSummarizationStrategy.NUM_SENTENCE_COUNT) or 10)

        embedder = Embedder.from_config(config.get(LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY), nlp)
        return cls(embedder, threshold, epsilon, num_sentence_count)

    def get_candidate_sentences(self, docs: Iterable[Document], word_limit: int) -> Iterable[Sentence]:

        sent_list = self.lexrank.summarize(docs)

        return self.__take_while_above_word_count(sent_list, word_limit)