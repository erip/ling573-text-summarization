from .summarization_strategy import SummarizationStrategy

from typing import TypeVar, Type, Dict, Set

from . import Document, Topic

from spacy.language import Language


T = TypeVar("T", bound="SummarizationStrategy")

@SummarizationStrategy.register_strategy
class FirstSentenceSummarizationStrategy(SummarizationStrategy):

    name = "first"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict], nlp: Language) -> T:
        return cls()

    def summarize(self, docs: Set[Document], word_limit: int) -> str:
        return ""

    def get_candidate_sentences(self, topic: Topic):
        # Get the raw text of the first span for each story.
        return [s.get_raw(s.get_spans()[0]) for s in topic.stories]