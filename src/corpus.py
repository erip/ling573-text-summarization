#!/usr/bin/env python3

import yaml
import xml.etree.ElementTree as ET

from doc_utils import Document, Docset, Topic

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
            topic_id = topic.get(id)
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


if __name__ == "__main__":
    reader = Corpus.from_config("../conf/patas_config.yaml", "../conf/UpdateSumm09_test_topics.xml")

    for topic in reader.topics:
        for doc in topic.docset:
            print("doc id: {0}, doc path: {1}".format(doc.id(), doc.get_path()))
