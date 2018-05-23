#!/usr/bin/env python3

from utils import Document, Topic

from strategy import SummarizationStrategy

from spacy.language import Language

import spacy

from typing import Dict

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

    def summarize(self, topic: Topic):
        """Uses the provided summarization strategy to summarize a set documents."""
        return self.strategy.summarize(topic, self.word_limit)

    @classmethod
    def from_config(cls, config: Dict, nlp: Language):

        # Parse out the word limit from configuration. Raise an exception if it doesn't exist.
        word_limit = config.get(Summarizer.WORD_LIMIT_KEY)
        if word_limit is None:
            raise ValueError("No config entry for '{0}'".format(Summarizer.WORD_LIMIT_KEY))

        word_limit = int(word_limit)

        # Parse out the strategy configuration. Raise an exception if it doesn't exist.
        strategy_config = config.get(Summarizer.CONFIG_STRATEGY_KEY)
        if strategy_config is None:
            raise ValueError("No config entry for '{0}'".format(Summarizer.CONFIG_STRATEGY_KEY))

        strategy = SummarizationStrategy.from_config(config.get(Summarizer.CONFIG_STRATEGY_KEY), nlp)
        return cls(word_limit, strategy)

if __name__ == "__main__":

    nlp = spacy.load('en')

    from strategy.lexrank_summarization_strategy import LexRankSummarizationStrategy
    from utils import Embedder
    from utils import SpacyEmbedder

    config = {
        Summarizer.WORD_LIMIT_KEY: 100,
        Summarizer.CONFIG_STRATEGY_KEY: {
            SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY: LexRankSummarizationStrategy.name,
            LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY: {
                Embedder.CONFIG_EMBED_NAME_KEY: SpacyEmbedder.name,
            },
            LexRankSummarizationStrategy.EPSILON_CONFIG_KEY: 0.11,
            LexRankSummarizationStrategy.THRESHOLD_CONFIG_KEY: 0.09,
        }
    }

    summarizer = Summarizer.from_config(config, nlp)