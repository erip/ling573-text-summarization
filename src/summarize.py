#!/usr/bin/env python3

import spacy

import yaml

from summarization.strategy import SummarizationStrategy, LexRankSummarizationStrategy
from summarization.utils import Embedder, SpacyEmbedder, TfidfEmbedder
from summarization.utils.sentence import Sentencizer
from summarization.information_ordering import InformationOrderer, ChronologicalExpert
from summarization import Summarizer

from corpus import Corpus

import argparse


def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-c', dest='config_file', default='../conf/local_config.yaml',
                   help='a yaml config mapping the topic clustering to file locations')
    p.add_argument('-d', dest='output_dir', default='../outputs/D4/', help='dir to write output summaries to')
    p.add_argument('-m', dest='model_path', default='', help='path for a pre-trained embedding model')
    return p.parse_args()


def make_filename(file_base, strategy, num_words):
    """return filename for storing summary"""

    return '{0}.{1}.{2}'.format(file_base, strategy, num_words)


def setup_information_orderer():

    chronological_expert = ChronologicalExpert()
    experts = { chronological_expert }
    weights = { ChronologicalExpert.name: 1.0 }

    return InformationOrderer(experts, weights)


def read_yaml_config(config_file):
    return yaml.load(open(config_file))


def customize_spacy(config, nlp):

    if config.get("sentence_boundary"):
        # custom sentence boundary detection
        nlp.add_pipe(Sentencizer(set(config.get("sentence_boundary"))).sbd)
    else:
        # spacy default. This is naive punctuation based, for dependency parse need a smaller model
        nlp.add_pipe('sentencizer')

    for key in config.get("special_chars"):
        nlp.tokenizer.add_special_case(key, [dict(ORTH=key)])
        nlp.Defaults.stop_words.add(key)

    # There is currently as of Oct 2018 a bug in spacy where not all models use their stop_word info even when they have it
    # This is a workaround to fix it. It won't hurt even if it is all working perfectly.
    for w in nlp.Defaults.stop_words:
        lex = nlp.vocab[w]
        lex.is_stop = True



if __name__ == "__main__":

    args = setup_argparse()

    nlp = spacy.load('en_vectors_web_lg') # Note that as of now this has vectors but does not have other bells and whistles like dependency parse

    print("Reading config...")
    config = read_yaml_config(args.config_file)

    print("Customizing NLP pipeline...")
    customize_spacy(config, nlp)

    print("Reading corpus...")
    corpus = Corpus.from_config(config, nlp)
 
    print("Reading summarizer...")
    summarizer = Summarizer.from_config(config, nlp)
    
    num_topics = len(corpus.topics)

    for document in corpus.documents:
        filename = make_filename(document.doc_path, config.get('strategy').get('name'),
                                 config.get(Summarizer.WORD_LIMIT_KEY))
        with open(filename, 'w') as outfile:
            for i, topic in enumerate(sorted([topic for topic in document.topics], key=lambda t: t.id())):
                candidates = summarizer.summarize(topic)
                print("Summarized {0}/{1} topics".format(i, num_topics))
                for sentence in sorted([sent for sent in candidates], key=lambda s: s.sent_index):
                    outfile.write('{} '.format(sentence.text))
                #outfile.write('*************')
                outfile.write('\n')  # write blank line between summaries
