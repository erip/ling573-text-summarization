from unittest import TestCase

from summarization.strategy import *

class SummarizationStrategyTestCase(TestCase):

    def setUp(self):

        self.config_with_no_name = {}

        self.config_with_invalid_name= {
            SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY: "invalid"
        }

        self.valid_lexrank_config = {
            SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY: LexRankSummarizationStrategy.name
        }

        self.valid_random_config = {
            SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY: RandomSummarizationStrategy.name
        }

        self.valid_first_config = {
            SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY: FirstSentenceSummarizationStrategy.name
        }

    def test_summarization_strategy_from_config_throws_when_strategy_config_has_no_name(self):
        with self.assertRaises(ValueError):
            SummarizationStrategy.from_config(self.config_with_no_name)

    def test_summarization_strategy_from_config_throws_when_strategy_config_has_invalid_name(self):
        with self.assertRaises(ValueError):
            SummarizationStrategy.from_config(self.config_with_invalid_name)

    def test_summarization_strategy_from_config_correctly_instantiates_lexrank_strategy(self):
        stategy = SummarizationStrategy.from_config(self.valid_lexrank_config)
        self.assertTrue(isinstance(stategy, LexRankSummarizationStrategy))

    def test_summarization_strategy_from_config_correctly_instantiates_random_strategy(self):
        stategy = SummarizationStrategy.from_config(self.valid_random_config)
        self.assertTrue(isinstance(stategy, RandomSummarizationStrategy))

    def test_summarization_strategy_from_config_correctly_instantiates_first_strategy(self):
        stategy = SummarizationStrategy.from_config(self.valid_first_config)
        self.assertTrue(isinstance(stategy, FirstSentenceSummarizationStrategy))