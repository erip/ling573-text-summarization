
import lxml.etree as ET
from bs4 import BeautifulSoup

from .corpus_document import CorpusDocument
from .story import Story
from .topic import Topic
from .docset import Docset

from datetime import datetime

import logging

from . import Sentence

import re

class Corpus(object):
    """Stores information about the corpus, including topic descriptions and docsets."""
    def __init__(self, topics, nlp):
        self.topics = topics
        self.nlp = nlp
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.preprocess_topic_docs()

    @classmethod
    def from_config(cls, yaml_conf, xml_path, nlp):
        """Given a yaml config file and xml path, this will read
        information about the corpus and return a Corpus object.
        :param yaml_file: filesystem configuration information (e.g., where the data live, etc.)
        :param xml_path: the task description
        :return: A Corpus object
        """
        xml_root = ET.parse(xml_path)
        topics = set()
        for topic in xml_root.findall("topic"):
            topic_id = topic.get("id")
            topic_title = topic.find("title").text.strip()
            topic_narrative = topic.find("narrative")
            if topic_narrative is not None:
                topic_narrative = topic_narrative.text.strip()
            docsetA_element = topic.find("docsetA")
            docsetA = set()
            docset_id = docsetA_element.get("id")
            for doc in docsetA_element:
                docsetA.add(CorpusDocument(yaml_conf['documentCollections'], doc.get("id")))
            docset = Docset(docset_id, docsetA)
            topics.add(Topic(topic_id, topic_title, topic_narrative, docset))
        return cls(topics, nlp)


    def __process_document(self, doc):
        curr_doc, doc_timestamp, headline_text, text_iterator = \
            self.__process_aquaint2_document(doc) if doc.is_aquaint2 \
                else self.__process_aquaint_document(doc)

        headline = curr_doc.find(headline_text)
        if headline is not None:
            headline = headline.text.strip()  # CURRENTLY NOT PREPROCESSING HEADLINE
        raw_body = []  # less elegant than a list comprehension, but with a comp we'd have to flatten a nest later
        for text in text_iterator:
            if text:
                text = ' '.join(text.strip().split())  # this split and join is to get rid of all the weird kinds of whitespace characters from the xml parse
                raw_body.append(text)
        raw_body = ' '.join(raw_body)
        sents = { Sentence(doc.id(), doc_timestamp, sent, i) for i, sent in enumerate(self.nlp(raw_body).sents) }
        return Story(headline, sents)

    def __process_aquaint2_document(self, doc):
        parser = ET.XMLParser(recover=True)
        xml_root = ET.parse(doc.get_path(), parser=parser)
        curr_doc = xml_root.find('.//DOC[@id="{0}"]'.format(doc.id()))  # find (vs findall): should only be one
        doc_timestamp = None
        headline_text = "HEADLINE"
        text_iterator = curr_doc.find("TEXT").itertext()
        return curr_doc, doc_timestamp, headline_text, text_iterator

    def __process_aquaint_document(self, doc):
        with open(doc.get_path(), "r") as infile:
            xml_root = BeautifulSoup(infile, "lxml")
        curr_doc = xml_root.find("docno", text=" {} ".format(doc.id())).parent
        time = curr_doc.find("date_time")
        if time is None:
            doc_timestamp = None
        else:
            date = time.text.strip().split()[0]
            format = "%Y-%m-%d" if '-' in date else "%m/%d/%Y"
            doc_timestamp = datetime.strptime(date, format)
        headline_text = "headline"
        text_iterator = [tag.text for tag in curr_doc.find_all("text")]
        return curr_doc, doc_timestamp, headline_text, text_iterator

    def preprocess_topic_docs(self, topic_ids=None):
        """
        Process newswire style xml into text and Story objects

        Grabs headline elements and body text elements, preprocesses them, creates Story objects, and stores them in
        Topic objects.
        Stories are an attribute of Topics rather than of Documents (which represent large collections
        of stories) because for current implementation, we don't care what Document a story comes from, just what Topic
        it belongs to.

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
            print("Processing {0} Docs in Topic".format(len(topic.docset)))
            for doc in topic.docset:
                story = self.__process_document(doc)
                topic.add_story(story)

