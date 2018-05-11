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
import argparse


def make_filename(topic_id, num_words):
    """Given topic id and max num words, return filename for storing summary
    :param topic_id: A string representing the unique topic id
    :param num_words: A maximum number of words for the summary length"""
    some_unique_alphanum = 4  # this is our groupnumber for identification
    return '{0}-A.M.{2}.{1}.{3}'.format(topic_id[:-1], topic_id[-1], num_words, some_unique_alphanum)


def combine_all_sentences(topic):
    """
    Form one document of all stories for given topic
    :param topic: Topic object
    :return: string of all sentences in every document in docSet A for input to lexrank summarize
    """
    all_sent = ''
    for s in topic.stories:
        all_sent += s.get_raw()  # TODO change this to .format so that it is faster
    return all_sent


def get_candidate_sentences(lexrank_input_doc, max_word_count=None, vector_type='tfidf'):
    """
    Runs lexrank summarizer and creates list of candidate sentences for the final summary
    :param lexrank_input_doc: a single string representing the doc or multiple docs to summarize
    :param max_word_count: int denoting maximum number of words possible in output summary for 1 topic. Optional.
    :param vector_type: the type of sentence representation to use
    :return: A list of candidate sentences, truncated to be below the max word count
    """
    #TODO make this so it isn't hard coded
    sent_num = 10  #random number to get the best 'sent_num' count of sentences from lexrank matrix calculations

    sent_list = summarizer.summarize(lexrank_input_doc, sent_num, max_word_count, vector_type)

    if max_word_count:
        while check_above_threshold(sent_list, max_word_count):
            sent_list = sent_list[:-1]

    return sent_list


def check_above_threshold(sent_list, max_word_count, pretokenized=False):
    """
    Take list of sentences return boolean of whether the total word count is below threshold
    :param sent_list: a list of sentences, or a nested list of sentences that have been tokenized
    :param max_word_count: int for max words in summary
    :param pretokenized: whether the sentences are strings or pretokenized. defaults to False
    """
    if pretokenized:
       # currently only counts things with alphanumeric characters as words
       word_count = sum([len(list(filter(str.isalnum, sent))) for sent in sent_list])
    else:
       # consider whitespace for wordcount
       word_count = sum([len(sent.split()) for sent in sent_list])

    if word_count > max_word_count:
       return True
    else:
       return False

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

    #get all documents in docSet 'X'
    corpusInfoObj = Corpus.from_config(args.config_file, args.topic_file)
    corpusInfoObj.preprocess_topic_docs()

    for topic in corpusInfoObj.topics:

        #generate a combined doc of text in all stories for this topic
        lexrank_input_doc = combine_all_sentences(topic)
        candidates = get_candidate_sentences(lexrank_input_doc, args.num_words, args.vector_type)

        with open('{0}{1}'.format(args.output_dir, make_filename(topic.id(), args.num_words)), 'w') as outfile:
            if candidates:
                for sentence in candidates:
                    outfile.write('{}\n'.format(sentence))
            else:
                outfile.write('\n')  # write blank file if no candidates



