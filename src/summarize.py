#!/usr/bin/env python3

import spacy

import yaml

from summarization.strategy import SummarizationStrategy, LexRankSummarizationStrategy
from summarization.utils import Embedder, SpacyEmbedder, TfidfEmbedder
from summarization.information_ordering import InformationOrderer, ChronologicalExpert
from summarization import Summarizer

from corpus import Corpus

import argparse

def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-c', dest='config_file', default='../conf/local_config.yaml',
                   help='a yaml config mapping the topic clustering to file locations')
    p.add_argument('-t', dest='topic_file', default='../conf/GuidedSumm_MINE_test_topics.xml',
                   help='an AQUAINT config file with topic clustering')
    p.add_argument('-d', dest='output_dir', default='../outputs/D4/', help='dir to write output summaries to')
    p.add_argument('-m', dest='model_path', default='', help='path for a pre-trained embedding model')
    return p.parse_args()

def make_filename(topic_id, num_words):
    """Given topic id and max num words, return filename for storing summary
    :param topic_id: A string representing the unique topic id
    :param num_words: A maximum number of words for the summary length"""
    some_unique_alphanum = 4  # this is our groupnumber for identification
    return '{0}-A.M.{2}.{1}.{3}'.format(topic_id[:-1], topic_id[-1], num_words, some_unique_alphanum)

def setup_information_orderer():

    chronological_expert = ChronologicalExpert()
    experts = { chronological_expert }
    weights = { ChronologicalExpert.name: 1.0 }

    return InformationOrderer(experts, weights)

def read_yaml_config(config_file):
    return yaml.load(open(config_file))


if __name__ == "__main__":

    args = setup_argparse()

    nlp = spacy.load('en_vectors_web_lg')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

    print("Reading config...")
    config = read_yaml_config(args.config_file)

    print("Reading corpus...")
    corpus = Corpus.from_config(config, args.topic_file, nlp)
 
    print("Summarizing...")
    summarizer = Summarizer.from_config(config, nlp)

    print("Ordering...")
    information_orderer = setup_information_orderer()

    for topic in corpus.topics:
        candidates = summarizer.summarize(topic)
        summary = information_orderer.order_all(candidates)
        with open('{0}{1}'.format(args.output_dir, make_filename(topic.id(), config.get(Summarizer.WORD_LIMIT_KEY))), 'w') as outfile:
            for sentence in summary:
                outfile.write('{}\n'.format(sentence.text))
            outfile.write('\n')  # write blank file if no candidates
