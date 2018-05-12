
from . import Document

from typing import TypeVar, Type, Dict, Set
from abc import ABCMeta, abstractmethod

T = TypeVar("T", bound="SummarizationStrategy")

class SummarizationStrategy(metaclass=ABCMeta):

    __name_to_strategy = dict()

    CONFIG_STRATEGY_NAME_KEY = "name"

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
    def from_config(cls: Type[T], config: Dict) -> T:
        """Reads the summarization strategy from a yaml config."""

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
        return strategy.from_strategy_config(config)

    @classmethod
    @abstractmethod
    def from_strategy_config(cls, config: Dict):
        pass

    @abstractmethod
    def summarize(self, docs: Set[Document], word_limit: int) -> str:
        """Summarize a set of documents within a given word limit."""

@SummarizationStrategy.register_strategy
class LexRankSummarizationStrategy(SummarizationStrategy):

    name = "lexrank"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict]) -> T:
        return cls()

    def summarize(self, docs: Set[Document], word_limit: int) -> str:
        return ""

@SummarizationStrategy.register_strategy
class RandomSummarizationStrategy(SummarizationStrategy):

    name = "random"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict]) -> T:
        return cls()

    def summarize(self, docs: Set[Document], word_limit: int) -> str:
        return ""

@SummarizationStrategy.register_strategy
class FirstSentenceSummarizationStrategy(SummarizationStrategy):

    name = "first"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict]) -> T:
        return cls()

    def summarize(self, docs: Set[Document], word_limit: int) -> str:
        return ""