
import sys
import yaml
import lxml.etree as ET
from bs4 import BeautifulSoup

from itertools import chain
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer

from .corpus_document import CorpusDocument
from .story import Story
from .topic import Topic
from .docset import Docset

class Corpus(object):
    """Stores information about the corpus, including topic descriptions and docsets."""
    def __init__(self, topics, nlp):
        self.topics = topics
        self.preprocess_topic_docs()
        self.nlp = nlp

    @classmethod
    def from_config(cls, yaml_file, xml_path, nlp):
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
        print("Processing {0} Topics in Corpus".format(len(all_topics)), file=sys.stderr)
        for topic in all_topics:
            print("Processing {0} Docs in Topic".format(len(topic.docset)), file=sys.stderr)
            for doc in topic.docset:
                #print(doc.id(), doc.get_path(), doc.is_aquaint2)
                if doc.is_aquaint2:
                    parser = ET.XMLParser(recover=True)
                    xml_root = ET.parse(doc.get_path(), parser=parser)
                    #xml_root = ET.parse(doc.get_path())
                    curr_doc = xml_root.find('.//DOC[@id="{0}"]'.format(doc.id()))  # find (vs findall): should only be one
                    doc_timestamp = None
                    headline_text = "HEADLINE"
                    text_text = "TEXT"
                    text_iterator = curr_doc.find("TEXT").itertext()

                else:
                    # for AQ 1 fall back to beautiful soup for weird encodings and to make the weird heirarchy easier
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

                headline = curr_doc.find(headline_text)
                if headline is not None:
                    headline = headline.text.strip()  # CURRENTLY NOT PREPROCESSING HEADLINE
                body, raw_body = [], []  # less elegant than a list comprehension, but with a comp we'd have to flatten a nest later
                for text in text_iterator:
                    if text:
                        text = ' '.join(text.strip().split())  # this split and join is to get rid of all the weird kinds of whitespace characters from the xml parse
                        body.extend(preprocess_text(text))
                        raw_body.append(text)
                #body = [preprocess_text(t) for t in curr_doc.find("TEXT").itertext() if t.strip()]
                raw_body = " ".join(raw_body)
                # doc_id, doc_timestamp, raw_text, sent_number, nlp
                sents = {
                    Sentence(doc.id(), doc_timestamp, sent, i, self.nlp)
                    for i, sent in enumerate(self.nlp(raw_body).sents)
                }
                topic.add_story(Story(headline, sents))


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
    reader = Corpus.from_config("../conf/local_config.yaml", "../conf/GuidedSumm10_test_topics.xml")

    topic_ids = {"D1002A", "D1003A"}  # {"D0903A", "D0909B"}
    reader.preprocess_topic_docs(topic_ids)
    #reader.preprocess_topic_docs()  # this version does whole corpus

    for topic in reader.topics:
        if topic.id() in topic_ids:
            print("\ntopic id: {0}, topic title: {1}, topic narrative: {2}".format(topic.id(), topic.title, topic.narrative))
            for s in topic.stories:
                print("\nHEADLINE: {0}\n".format(s.get_headline()))
                print(" ".join(list(chain.from_iterable(s.get_sentences()))))
        #for doc in topic.docset:
        #    print("doc id: {0}, doc path: {1}".format(doc.id(), doc.get_path()))
