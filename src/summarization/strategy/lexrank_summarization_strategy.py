from .summarization_strategy import SummarizationStrategy

from typing import TypeVar, Type, Dict, Set

T = TypeVar("T", bound="SummarizationStrategy")

from .lexrank import LexRankSummarizer

from . import Document

@SummarizationStrategy.register_strategy
class LexRankSummarizationStrategy(SummarizationStrategy):

    def __init__(self):
        self.lexrank = LexRankSummarizer(None)

    name = "lexrank"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict]) -> T:
        return cls()

    def summarize(self, docs: Set[Document], word_limit: int) -> str:
        return ""

    @classmethod
    def check_above_threshold(cls, sent_list, max_word_count, pretokenized=False):
        """
        Take list of sentences return boolean of whether the total word count is below threshold
        :param sent_list: a list of sentences, or a nested list of sentences that have been tokenized
        :param max_word_count: int for max words in summary
        :param pretokenized: whether the sentences are strings or pretokenized. defaults to False
        """
        if pretokenized:
            # currently only counts things with alphanumeric characters as words
            word_count = sum([len(list(filter(str.isalnum, sent))) for sent in sent_list])
        else:
            # consider whitespace for wordcount
            word_count = sum([len(sent.split()) for sent in sent_list])

        return word_count > max_word_count

    def get_candidate_sentences(self, topic, word_limit):

        lexrank_input_doc = ' '.join(s.get_raw() for s in topic.stories)

        sent_list = self.lexrank.summarize(lexrank_input_doc, 10, word_limit)

        if word_limit:
            while LexRankSummarizationStrategy.check_above_threshold(sent_list, word_limit):
                sent_list = sent_list[:-1]

        return sent_list