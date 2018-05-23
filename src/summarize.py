#!/usr/bin/env python3

import spacy

from summarization.strategy import SummarizationStrategy, LexRankSummarizationStrategy
from summarization.utils import Embedder, SpacyEmbedder
from summarization import Summarizer

if __name__ == "__main__":

    nlp = spacy.load('en')

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
