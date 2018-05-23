
from abc import ABCMeta, abstractmethod

import numpy as np

from sklearn.metrics import pairwise


class Embedding(metaclass=ABCMeta):

    @abstractmethod
    def value(self) -> np.array:
        """"""

class TfidfEmbedding(Embedding):

    def __init__(self, vector):
        self.vector = vector

    def value(self):
        return self.vector

class SpacyEmbedding(Embedding):
    def __init__(self, vector):
        self.vector = vector

    def value(self):
        return self.vector

class Doc2VecEmbedding(Embedding):
    pass

class Word2VecEmbedding(Embedding):
    pass