
import os
import gzip
import logging
import itertools
from datetime import datetime
from typing import Dict, List

from spacy.language import Language

from . import Sentence
from .corpus_document import CorpusDocument
from .docset import Docset
from .story import Story
from .topic import Topic


class Corpus(object):
    """Stores information about the corpus."""
    def __init__(self, topics, base_paths, documents, nlp):
        self.topics = topics
        self.base_paths = base_paths
        self.documents = documents
        self.nlp = nlp
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.preprocess_topic_docs()

    @classmethod
    def from_config(cls, conf: Dict, nlp: Language):
        """Given a yaml config file and a , this will read
        information about the corpus and return a Corpus object.

        :param yaml_file: filesystem configuration information (e.g., where the data live, etc.)
        :param nlp: a SpaCy language object
        :return: A Corpus object
        """
        document_collections = conf.get('documentCollections') # This is a nested dict of directory paths
        if not document_collections:
            raise ValueError("Config is missing 'documentCollections'")

        topics, documents = set(), set()
        # assume file is raw text
        title_end = conf.get("title_boundary")
        for dir_path in document_collections.values():
            with os.scandir(dir_path) as source_dir:
                files = [file.path for file in source_dir if file.is_file() and not file.name.startswith('.')]
                for file_path in files:
                    this_doc = CorpusDocument(file_path, set())
                    with open(file_path, "r") as fin:
                        for i, line in enumerate(fin):
                            if title_end and title_end != "None":
                                topic_title, topic_narrative = line.strip().split(title_end)
                            else:
                                topic_title, topic_narrative = "", line.strip()
                            # i is the id,
                            topics.add(Topic(i, topic_title, topic_narrative, file_path))
                    this_doc.add_topics(topics)
                    assert(this_doc not in documents), "Two documents have same full path. " \
                                                       "If content differs, only one will be preserved, so we won't let you do that"
                    documents.add(this_doc)

        return cls(topics, document_collections, documents, nlp)


    def __process_document(self, doc: Topic):
        """Given a document, parses information from the document to create a story.

        :param doc: a Topic
        :return: the story in the document
        """
        sents = { Sentence(sent, i) for i, sent in enumerate(self.nlp(doc.narrative).sents) }
        return Story(sents)

    def preprocess_topic_docs(self, topic_ids: List[str] = None):
        """Process topics into text and Story objects

        :param topic_ids: an optional set of strings matching topic ids. If not provided, preprocesses entire corpus.
        :return: None, modifies Corpus object
        """
        # filter the IDS to preprocess
        if topic_ids:
            all_topics = [topic for topic in self.topics if topic.id() in topic_ids]
        else:
            all_topics = self.topics

        print("Processing {0} Topics in Corpus".format(len(all_topics)))
        for topic in all_topics:
            story = self.__process_document(topic)
            topic.add_story(story)

