#!/usr/bin/env python3

import spacy

from summarization.strategy import SummarizationStrategy, LexRankSummarizationStrategy
from summarization.utils import Embedder, SpacyEmbedder, TfidfEmbedder
from summarization import Summarizer

from corpus import Corpus

import argparse

def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-c', dest='config_file', default='../conf/local_config.yaml',
                   help='a yaml config mapping the topic clustering to file locations')
    p.add_argument('-t', dest='topic_file', default='../conf/GuidedSumm_MINE_test_topics.xml',
                   help='an AQUAINT config file with topic clustering')
    p.add_argument('-n', dest='num_words', help='maximum number of words allowed in summary', type=int, default=100)
    p.add_argument('-v', dest='vector_type', help='the type of vector representation to use for sentences. Choose from:'
                                                  'spacy, doc2vec, tfidf, word2vec',  default='tfidf')
    p.add_argument('-th', dest='threshold', default=0.1, type=float, help='threshold for when to draw a edge between sentences in lexrank')
    p.add_argument('-e', dest='epsilon', default=0.1, type=float, help='epsilon value to control convergence of eigenvectors in lexrank matrix')
    p.add_argument('-d', dest='output_dir', default='../outputs/D2/', help='dir to write output summaries to')
    p.add_argument('-m', dest='model_path', default='', help='path for a pre-trained embedding model')
    return p.parse_args()


if __name__ == "__main__":

    args = setup_argparse()

    nlp = spacy.load('en')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

    corpus = Corpus.from_config(args.config_file, args.topic_file, nlp)

    config = {
        Summarizer.WORD_LIMIT_KEY: 100,
        Summarizer.CONFIG_STRATEGY_KEY: {
            SummarizationStrategy.CONFIG_STRATEGY_NAME_KEY: LexRankSummarizationStrategy.name,
            LexRankSummarizationStrategy.EMBEDDER_CONFIG_KEY: {
                Embedder.CONFIG_EMBED_NAME_KEY: TfidfEmbedder.name,
            },
            LexRankSummarizationStrategy.EPSILON_CONFIG_KEY: 0.11,
            LexRankSummarizationStrategy.THRESHOLD_CONFIG_KEY: 0.09,
        }
    }

    summarizer = Summarizer.from_config(config, nlp)

    for topic in corpus.topics:
        candidates = summarizer.summarize(topic)
        print("Candidates:")
        for can in candidates:
            print(can._sent)
