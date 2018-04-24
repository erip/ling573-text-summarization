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
    :return: List of all sentences in every document in docSet A for input to lexrank summarize
    """
    all_sent_list = []

    for s in topic.stories:
        this_list = s.get_sentences() #get a nested list of outer list representing sentences and inner list the list of words in each sentence
        all_sent_list += this_list

    return all_sent_list

def get_candidate_sentences(lexrank_input_doc,max_word_count):
    """
    Runs lexrank summarizer and creates list of candidate sentences for the final summary
    :param lexrank_input_doc: ??? #TODO: list/nested list??
    :param max_word_count: int denoting maximum number of words possible in output summary for 1 topic
    :return: List of candidate sentences
    """

    sent_num = 2  #random number to get the best 'sent_num' count of sentences from lexrank matrix calculations

    ''' 
    result_list = []
    for sent in summarizer.summarize(lexrank_input_doc, sent_num, max_word_count):
        result_list += sent
    return result_list
    '''

    #TODO: information ordering - add if required
    return summarizer.summarize(lexrank_input_doc, sent_num, max_word_count)

if __name__ == "__main__":

    """
    Generates the summary files for all topics given as input 
    ##TEMPORARY call to this module given below; To be modified to fit the pipeline
    cmd: python3 lexrank_driver.py path_to_config_yaml path_to_topic_file_xml num_words output_dir 
    """

    #READ Command line arguments
    p = argparse.ArgumentParser()
    p.add_argument('-c', dest='config_file', default='../conf/patas_config.yaml',
                   help='an xml config mapping the topic clustering to file locations')
    p.add_argument('-t', dest='topic_file', default='../conf/UpdateSumm09_test_topics.xml',
                   help='an AQUAINT config file with topic clustering')
    p.add_argument('-n', dest='num_words', help='maximum number of words allowed in summary', type=int)
    p.add_argument('-th', dest='threshold', default=0.1, help='threshold for when to draw a edge between sentences in lexrank')
    p.add_argument('-e', dest='epsilon', default=0.1, help='epsilon value to control convergence of eigenvectors in lexrank matrix')
    p.add_argument('-d', dest='output_dir', default='../outputs/D2/', help='dir to write output summaries to')
    args = p.parse_args()

    #create stemmer and summarizer objects
    stemmer = PorterStemmer()
    summarizer = LexRankSummarizer(stemmer, threshold=args.threshold, epsilon=args.epsilon, stop_words=set(stopwords.words('english')))

    #get all documents in docSet 'X'
    corpusInfoObj = Corpus.from_config(args.config_file, args.topic_file)
    corpusInfoObj.preprocess_topic_docs() #preprocess docs for all topic ids

    for topic in corpusInfoObj.topics:

        #generate a combined doc of text in all stories for this topic
        lexrank_input_doc = combine_all_sentences(topic)
        candidates = get_candidate_sentences(lexrank_input_doc,args.num_words)

        with open('{0}{1}'.format(args.output_dir, make_filename(topic.id(), args.num_words)), 'w') as outfile:
            if candidates:
                for sentence in candidates:
                    outfile.write('{}\n'.format(sentence))
            else:
                outfile.write('\n')  # write blank file if no candidates



