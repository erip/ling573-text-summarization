"""
Example commands to run:
python lexrank_driver.py -c ../conf/patas_devtest_config.yaml -t ../conf/GuidedSumm10_test_topics.xml -n 100 -v tfidf -th 0.1 -e 0.1 -d ../outputs/D3/
python lexrank_driver.py -c ../conf/patas_devtest_config.yaml -t ../conf/GuidedSumm10_test_topics.xml -n 100 -v spacy -th 0.1 -e 0.1 -d ../outputs/D3/
python lexrank_driver.py -c ../conf/patas_devtest_config.yaml -t ../conf/GuidedSumm10_test_topics.xml -n 100 -v doc2vec -th 0.1 -e 0.1 -d ../outputs/D3/ -m /dropbox/17-18/573/other_resources/word_embeddings/eng_gw/dw100M_cased.vecs

"""

from gensim.models import Doc2Vec
from lexrank import LexRankSummarizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from corpus import Corpus
from information_ordering import InformationOrderer
from experts import ChronologicalExpert
import argparse

from itertools import combinations

import spacy

from collections import Counter

def make_filename(topic_id, num_words):
    """Given topic id and max num words, return filename for storing summary
    :param topic_id: A string representing the unique topic id
    :param num_words: A maximum number of words for the summary length"""
    some_unique_alphanum = 4  # this is our groupnumber for identification
    return '{0}-A.M.{2}.{1}.{3}'.format(topic_id[:-1], topic_id[-1], num_words, some_unique_alphanum)

if __name__ == "__main__":

    """
    Generates the summary files for all topics given as input 
    ##TEMPORARY call to this module given below; To be modified to fit the pipeline
    cmd: python3 lexrank_driver.py path_to_config_yaml path_to_topic_file_xml num_words output_dir 
    """

    #READ Command line arguments
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
    args = p.parse_args()

    nlp = spacy.load('en_vectors_web_lg')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

    #check for model params
    if args.model_path:
        if args.vector_type == 'doc2vec':
            model = Doc2Vec.load(args.model_path)
        elif args.vector_type == 'word2vec':
            pass
            #TODO add word2vec support
    else:
        model = None


    #create summarizer objects
    stemmer = PorterStemmer()
    summarizer = LexRankSummarizer(stemmer, threshold=args.threshold, epsilon=args.epsilon, stop_words=set(stopwords.words('english')), model=model)

    chronological_expert = ChronologicalExpert()

    experts = { chronological_expert }
    weight = { chronological_expert.name: 1.0 }

    info_orderer = InformationOrderer(experts, weight)

    #get all documents in docSet 'X'
    corpusInfoObj = Corpus.from_config(args.config_file, args.topic_file, nlp)
    corpusInfoObj.preprocess_topic_docs()

    for topic in corpusInfoObj.topics:

        #generate a combined doc of text in all stories for this topic
        candidates = get_candidate_sentences(topic, args.num_words, args.vector_type)

        summary = order_sentences(info_orderer, candidates)

        with open('{0}{1}'.format(args.output_dir, make_filename(topic.id(), args.num_words)), 'w') as outfile:
            if summary:
                for sentence in summary:
                    outfile.write('{}\n'.format(sentence.text))
            else:
                outfile.write('\n')  # write blank file if no candidates



