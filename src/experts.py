#!/usr/bin/env python3

from abc import ABC, abstractmethod

class Expert(ABC):
    """The abstract base class for information ordering experts."""

    @property
    def name(self):
        return self._name

    @abstractmethod
    def order(self, d1, d2, partial_summary):
        """Orders two documents."""