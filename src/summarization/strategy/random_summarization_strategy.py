from .summarization_strategy import SummarizationStrategy

from typing import TypeVar, Type, Dict, Iterable

from utils import Sentence

T = TypeVar("T", bound="SummarizationStrategy")

from spacy.language import Language

from utils import Document

import random

@SummarizationStrategy.register_strategy
class RandomSummarizationStrategy(SummarizationStrategy):

    name = "random"

    @classmethod
    def from_strategy_config(cls: Type[T], config: Dict[str, dict], nlp: Language) -> T:
        return cls()

    def get_candidate_sentences(self, docs: Iterable[Document], word_limit: int) -> Iterable[Sentence]:
        random_sentences = {random.choice(doc.sentences) for doc in docs}
        return self.__take_while_under_word_count(random_sentences, word_limit)