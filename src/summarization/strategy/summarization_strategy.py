
from utils import Document, Topic, Sentence

from typing import TypeVar, Type, Dict, Set, Iterable
from abc import ABCMeta, abstractmethod

from spacy.language import Language

T = TypeVar("T", bound="SummarizationStrategy")

from functools import reduce

class SummarizationStrategy(metaclass=ABCMeta):

    __name_to_strategy = dict()

    CONFIG_STRATEGY_NAME_KEY = "name"

    def __take_while_under_word_count(self, sentences: Iterable[Sentence], word_count: int) -> Iterable[Sentence]:
        kept_sentences, _ = reduce(
            # Append the sentence and update the total word count so far if
            lambda acc, sentence: (acc[0] + [sentence], acc[1] + len(sentence)) if
                # The current word count + the number of tokens in the sentence is under the allowed word count
                acc[1] + len(sentence) <= word_count
                # Otherwise, take the current sentences and total word count
                else acc,
            # Apply this to all sentences
            sentences,
            # Base case
            ([], 0)
        )
        return kept_sentences

    @property
    @abstractmethod
    def name(cls):
        """Name of the summarization strategy"""

    @classmethod
    def register_strategy(cls, scls):
        """Adds the subclasses to the mapping where the key is `SummarizationStrategy.name` and the
        value is the class.

        :param scls: the subclass to register
        :return: the subclass
        """
        cls.__name_to_strategy[scls.name] = scls
        return scls

    @classmethod
    def from_config(cls: Type[T], config: Dict, nlp: Language) -> T:
        """Reads the summarization strategy from a dictionary."""

        # Get the name of the strategy to be used for summarization from the strategy configuration.
        strategy_name = config.get(SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY)
        if strategy_name is None:
            raise ValueError("No strategy config entry for '{0}'".format(SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY))

        # Get the class name of the strategy to be used for summarization by name.
        # Raise an exception if the strategy name is unknown.
        strategy = SummarizationStrategy.__name_to_strategy.get(strategy_name.lower())
        if strategy is None:
            raise ValueError("No strategy name '{0}'".format(strategy_name))

        # Create the strategy instance from the strategy config.
        return strategy.from_strategy_config(config, nlp)

    @classmethod
    @abstractmethod
    def from_strategy_config(cls, config: Dict, nlp: Language):
        pass

    def summarize(self, topic: Topic, word_limit: int) -> Set[Sentence]:
        """Summarize a set of documents within a given word limit."""
        return self.get_candidate_sentences(topic.stories, word_limit)

    @abstractmethod
    def get_candidate_sentences(self, docs: Set[Document], word_limit: int) -> Set[Sentence]:

        """Gets candidate sentences that describe the topic within the word limit"""