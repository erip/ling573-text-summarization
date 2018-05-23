
from typing import Set

from .document import Document

class Topic(object):
    def __init__(self, stories: Set[Document]):
        self.stories = stories