'''
A script that creates the stupidest possible baselines for muliple document summarization.
Either random or single sentences.
Command to run: baseline.py baseline_type -n num_words

baseline_type: "first" or "random"
num_words: integer of max word length
'''

import argparse
import random

import sys

from corpus import Corpus


def make_filename(topic_id, num_words):
    """Given topic id and max num words, return filename for storing summary
    :param topic_id: A string representing the unique topic id
    :param num_words: A maximum number of words for the summary length"""
    some_unique_alphanum = 1  # this is a placeholder until instructor specifies what kind of ID he wants here
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
        selected_sent.append(s.get_sentences()[index])

    return selected_sent


def check_above_threshold(sentences, num_words):
    """Take nested list of sentences and word, return boolean of whether the total word count is above threshold"""
    # currently only counts things with alphanumeric characters as words
    if sum([len(list(filter(str.isalnum, sent))) for sent in sentences]) > num_words:
        return True
    else:
        return False


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('baseline_type', help='the type of baseline, either "random" or "first"')
    p.add_argument('-n', dest='num_words', help='maximum number of words allowed in summary', type=int)
    p.add_argument('-d', dest='output_dir', default='../outputs/D2/', help='dir to write output summaries to')
    args = p.parse_args()
        
    # reader = Corpus.from_config("../conf/patas_config.yaml", "../conf/UpdateSumm09_test_topics.xml")
    reader = Corpus.from_config("../conf/local_config.yaml", "../conf/UpdateSumm09_test_topics.xml")
    reader.preprocess_topic_docs()

    for topic in reader.topics:
        candidates = get_candidate_sentences(topic, args.baseline_type)
        if args.num_words:
            while check_above_threshold(candidates, args.num_words):
                candidates = candidates[:-1]

        with open('{0}{1}'.format(args.output_dir, make_filename(topic.id(), args.num_words)), 'w') as outfile:
            for i in range(len(candidates)):
                outfile.write('{}\n'.format(" ".join(candidates[i])))