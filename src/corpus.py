#!/usr/bin/env python3
import sys
import yaml
import xml.etree.ElementTree as ET

from itertools import chain
from nltk import word_tokenize, sent_tokenize

from doc_utils import Document, Docset, Topic, Story


class Corpus(object):
    """Stores information about the corpus, including topic descriptions and docsets."""
    def __init__(self, topics):
        self.topics = topics

    @classmethod
    def from_config(cls, yaml_file, xml_path):
        """Given a yaml config file and xml path, this will read
        information about the corpus and return a Corpus object.
        :param yaml_file: filesystem configuration information (e.g., where the data live, etc.)
        :param xml_path: the task description
        :return: A Corpus object 
        """
        yaml_conf = yaml.load(open(yaml_file))
        xml_root = ET.parse(xml_path)
        topics = set()
        for topic in xml_root.findall("topic"):
            topic_id = topic.get("id")
            topic_title = topic.find("title").text.strip()
            topic_narrative = topic.find("narrative").text.strip()
            docsetA_element = topic.find("docsetA")
            docsetA = set()
            docset_id = docsetA_element.get("id")
            for doc in docsetA_element:
                docsetA.add(Document(yaml_conf['documentCollections'], doc.get("id")))
            docset = Docset(docset_id, docsetA)
            topics.add(Topic(topic_id, topic_title, topic_narrative, docset))
        return cls(topics)

    def preprocess_topic_docs(self, topic_ids=None):
        """
        Process newswire style xml into text and Story objects

        Grabs headline elements and body text elements, preprocesses them, creates Story objects, and stores them in
        Topic objects.
        Stories are an attribute of Topics rather than of Documents (which represent large collections
        of stories) because for current implementation, we don't care what Document a story comes from, just what Topic
        it belongs to.

        :param topic_ids: an optional list of strings matching topic ids. If not provided, preprocesses entire corpus.
        :return: None, modifies Corpus object
        """
        print("Processing {0} Topics in Corpus".format(len(self.topics)), file=sys.stderr)
        for topic in self.topics:
            print("Processing {0} Docs in Topic".format(len(topic.docset)), file=sys.stderr)
            for doc in topic.docset:
                #TODO add is AQUAINT vs AQUAINT2 to the docset object since traversal will be different. The below is AQUAINT-2 ONLY
                xml_root = ET.parse(doc.get_path())
                curr_doc = xml_root.find('.//DOC[@id="{0}"]'.format(doc.id()))  # find (vs findall): should only be one
                headline = preprocess_text(curr_doc.find("HEADLINE").text)
                body = []  # less elegant than a list comprehension, but with a comp we'd have to flatten a nest later
                for t in curr_doc.find("TEXT").itertext():
                    if t.strip():
                        body.extend(preprocess_text(t))
                #body = [preprocess_text(t) for t in curr_doc.find("TEXT").itertext() if t.strip()]
                topic.add_story(Story(headline, body))


def preprocess_text(text_block):
    """Tokenize and lowercase a block of text, return nested list of sentences and words

    :param text_block: a block of English text whitespace separated
    :return a nested list of lists of tokenized text [[w1,w2...wn],[w1,w2...wn]] where the outer list sentences and the
    inner is words int that sentence. Note that if text_block was only one sentence, it will still be nested.
    """
    words = [word_tokenize(sent.lower()) for sent in sent_tokenize(text_block.strip())]
    return words


if __name__ == "__main__":
    #reader = Corpus.from_config("../conf/patas_config.yaml", "../conf/UpdateSumm09_test_topics.xml")
    reader = Corpus.from_config("../conf/local_config.yaml", "../conf/UpdateSumm09_test_topics.xml")

    reader.preprocess_topic_docs()
    for topic in reader.topics:
        print("\ntopic id: {0}, topic title: {1}, topic narrative: {2}".format(topic.id(), topic.title, topic.narrative))
        for s in topic.stories:
            print("\nHEADLINE: {0}\n".format(" ".join(list(chain.from_iterable(s.get_headline())))))
            print(" ".join(list(chain.from_iterable(s.get_sentences()))))
        #for doc in topic.docset:
        #    print("doc id: {0}, doc path: {1}".format(doc.id(), doc.get_path()))
