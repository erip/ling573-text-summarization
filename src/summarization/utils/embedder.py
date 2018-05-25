from abc import ABCMeta, abstractmethod

from .sentence import Sentence

from typing import Type, Dict, TypeVar, Iterable

from spacy.language import Language

from sklearn.metrics import pairwise

T = TypeVar("T", bound="Embedder")


class Embedder(metaclass=ABCMeta):

    __name_to_embedder = dict()

    CONFIG_EMBED_NAME_KEY = "name"

    @property
    @abstractmethod
    def name(cls):
        """Name of the summarization strategy"""

    @classmethod
    def register_strategy(cls, scls):
        cls.__name_to_embedder[scls.name] = scls
        return scls

    def __init__(self, nlp):
        self.nlp = nlp

    @classmethod
    def from_config(cls: Type[T], config: Dict, nlp: Language, sentences: Iterable[str]) -> T:
        """Reads the summarization strategy from a dictionary."""

        embedder_name = config.get(Embedder.CONFIG_EMBED_NAME_KEY)
        if embedder_name is None:
            raise ValueError("No embedding config entry for '{0}'".format(Embedder.CONFIG_EMBED_NAME_KEY))

        embedder = Embedder.__name_to_embedder.get(embedder_name.lower())
        if embedder is None:
            raise ValueError("No embedder named '{0}'".format(embedder_name))

        # Create the strategy instance from the strategy config.
        return embedder.from_embedding_config(config, nlp, sentences)

    @classmethod
    @abstractmethod
    def from_embedding_config(cls, config: Dict, nlp: Language, sentences: Iterable[str]):
        pass

    @abstractmethod
    def embed(self, sentence):
        """Creates an embedding of a sentence"""

    def cosine_similarity(self, sentence1: Sentence, sentence2: Sentence) -> float:
        return pairwise.cosine_similarity(sentence1.embedding, sentence2.embedding)[0][0]