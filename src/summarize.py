#!/usr/bin/env python3

from summarization.summarizer import Summarizer
from corpus import Corpus

if __name__ == "__main__":
    yaml_file = "./foo.yaml"
    xml_path = "./foo.xml"
    corpus = Corpus.from_config(yaml_file, xml_path)