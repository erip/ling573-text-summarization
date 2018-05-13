#!/usr/bin/env python3

from .utils.document import Document
from .strategy import SummarizationStrategy

from typing import Set, Dict

class Summarizer(object):
    """The summarizer class."""

    WORD_LIMIT_KEY = "word_limit"
    CONFIG_STRATEGY_KEY = "strategy"

    def __init__(self, word_limit: int, strategy: SummarizationStrategy):
        """
        :param word_limit: the maximum number of words allowed in the summary.
        :param strategy: the strategy for summarizing: this can be LexRank, first-sentence, etc.
        """
        self.word_limit = word_limit
        self.strategy = strategy

    def summarize(self, documents: Set[Document]):
        """Uses the provided summarization strategy to summarize a set documents."""
        return self.strategy.summarize(documents, self.word_limit)

    @classmethod
    def from_config(cls, config: Dict):

        # Parse out the word limit from configuration. Raise an exception if it doesn't exist.
        word_limit = config.get(Summarizer.WORD_LIMIT_KEY)
        if word_limit is None:
            raise ValueError("No config entry for '{0}'".format(Summarizer.WORD_LIMIT_KEY))

        word_limit = int(word_limit)

        # Parse out the strategy configuration. Raise an exception if it doesn't exist.
        strategy_config = config.get(Summarizer.CONFIG_STRATEGY_KEY)
        if strategy_config is None:
            raise ValueError("No config entry for '{0}'".format(Summarizer.CONFIG_STRATEGY_KEY))

        strategy = SummarizationStrategy.from_config(config)
        return cls(word_limit, strategy)