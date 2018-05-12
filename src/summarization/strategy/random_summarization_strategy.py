from .summarization_strategy import SummarizationStrategy

from typing import TypeVar, Type, Dict, Set

T = TypeVar("T", bound="SummarizationStrategy")

from . import Document

import random

@SummarizationStrategy.register_strategy
class RandomSummarizationStrategy(SummarizationStrategy):

    name = "random"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict]) -> T:
        return cls()

    def summarize(self, docs: Set[Document], word_limit: int) -> str:
        return ""

    def get_candidate_sentences(self, topic):
        # Get the raw text of a random span for each story.
        return [s.get_raw(s.get_spans()[random.randint(0, s.num_sentences() - 1)]) for s in topic.stories]