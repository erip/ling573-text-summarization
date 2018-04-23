'''
A script that creates the stupidest possible baselines for muliple document summarization.
Either random or single sentences.
Command to run: baseline.py baseline_type -n num_words -d dir

baseline_type: "first" or "random"
num_words: integer of max word length. If unspecified will not limit length.
dir: directory to write files too. If unspecified, will default
'''

import argparse
import random

import sys

from corpus import Corpus


def make_filename(topic_id, num_words):
    """Given topic id and max num words, return filename for storing summary
    :param topic_id: A string representing the unique topic id
    :param num_words: A maximum number of words for the summary length"""
    some_unique_alphanum = 4  # this is our groupnumber for identification
    return '{0}-A.M.{2}.{1}.{3}'.format(topic_id[:-1], topic_id[-1], num_words, some_unique_alphanum)


def get_candidate_sentences(topic, baseline_type):
    """Take Topic & baseline type, return a nested list of sentences selected and their indices in original text"""
    selected_sent = []
    for s in topic.stories:
        if baseline_type == "first":
            index = 0
        elif baseline_type == "random":
            index = random.randint(0, s.num_sentences()-1)
        else:
            print("Out of luck mate, your only options are 'first' or 'random'", file=sys.stderr)
        #selected_sent.append(s.get_sentences()[index])
        span = s.get_spans()[index]
        selected_sent.append(s.get_raw(span))

    return selected_sent


def check_above_threshold(sentences, num_words, pretokenized=False):
    """
    Take list of sentences return boolean of whether the total word count is above threshold
    :param sentences: a list of sentences, or a nested list of sentences that have been tokenized
    :param num_words: int for max words in summary
    :param pretokenized: whether the sentences are strings or pretokenized. defaults to False
    """
    if pretokenized:
        # currently only counts things with alphanumeric characters as words
        word_count = sum([len(list(filter(str.isalnum, sent))) for sent in sentences])
    else:
        # consider whitespace for wordcount
        word_count = sum([len(sent.split()) for sent in sentences])
    if word_count > num_words:
        return True
    else:
        return False


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('baseline_type', help='the type of baseline, either "random" or "first"')
    p.add_argument('-c', dest='config_file', default='../conf/patas_config.yaml',
                   help='an xml config mapping the topic clustering to file locations')
    p.add_argument('-t', dest='topic_file', default='../conf/UpdateSumm09_test_topics.xml',
                   help='an ACQUAINT config file with topic clustering')
    p.add_argument('-n', dest='num_words', help='maximum number of words allowed in summary', type=int)
    p.add_argument('-d', dest='output_dir', default='../outputs/D2/', help='dir to write output summaries to')
    args = p.parse_args()

    # topic_ids = {"D0903A", "D0909B"}
    # reader = Corpus.from_config("../conf/local_config.yaml", "../conf/UpdateSumm09_test_topics.xml")

    reader = Corpus.from_config(args.config_file, args.topic_file)
    reader.preprocess_topic_docs()

    for topic in reader.topics:
        candidates = get_candidate_sentences(topic, args.baseline_type)
        if args.num_words:
            while check_above_threshold(candidates, args.num_words):
                candidates = candidates[:-1]

        with open('{0}{1}'.format(args.output_dir, make_filename(topic.id(), args.num_words)), 'w') as outfile:
            for sentence in candidates:
                outfile.write('{}\n'.format(sentence))