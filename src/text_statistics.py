'''
A script that
Command to run:
'''

import argparse
import os
from collections import defaultdict, Counter
from itertools import chain

import numpy as np
import sys

from corpus import preprocess_text


def process_files_in_dirs(source_directories):
    """ take list of source dirs, return dict of key=dir key=filename val=nested list of tokenised sentences & words  """
    file_dict = defaultdict(dict)
    for source_dir in source_directories:
        with os.scandir(source_dir) as curr_dir:
            for file in curr_dir:
                if file.is_file() and not file.name.startswith('.'):
                    #full_filepath = '{}/{}'.format(source_dir)
                    with open(file.path, 'r') as curr_file:
                        try:
                            text = curr_file.read()
                        except UnicodeDecodeError:
                            print('weird characters in file {}. Skipping.'.format(file.path), file=sys.stderr)
                        sent_words = preprocess_text(text)
                        file_dict[source_dir][file.name] = sent_words

    return file_dict

def lexical_diversity(word_counts):
    """
    Takes words and counts and calculates resulting lexical diversity
    :param word_counts: dict of words and counts
    :return: lexical diversity score
    """
    unique_words = len(word_counts)
    total_words = sum(val for val in word_counts.values())
    return unique_words/total_words


def get_min_max_avg(sentences):
    num_sent = len(sentences)
    sent_lengths = list(map(len, sentences))

    return min(sent_lengths), max(sent_lengths), sum(sent_lengths)/num_sent


def basic_metrics(data_dict):
    """take a dict of tokenized data and return basic metrics about it: for each file and for all files

    Metrics: words per sent (min,max, avg), lexical diversity
    :param data_dict: {filegroup: file: [[s1w1, s1w2, s1w3...s1wn], [s2w1, s2w2, s2w3...s2wn], ...[snw1,...snwn]]}

    """
    word_distributions, diversity_distributions = [], []
    for group in data_dict:
        word_avgs, lexical_div = [], []  # for storing to average for a full directory at the end
        num_files = len(data_dict[group])
        for file in data_dict[group]:
            sentences = data_dict[group][file]
            min_words, max_words, avg_words = get_min_max_avg(sentences)
            word_avgs.append(avg_words)
            lexical_div.append(lexical_diversity(Counter(chain.from_iterable(sentences))))
            #print("File: {0}\nMin: {1} Max: {2} Avg: {3:f}\n".format(file, min_words, max_words, avg_words))
        print("\n***** Group: {0} Overall Words per Sent: {1:f} Overall Lexical Diversity: {2:f} *****\n".format(
            group, sum(word_avgs)/num_files, sum(lexical_div)/num_files))
        word_distributions.append(word_avgs)
        diversity_distributions.append(lexical_div)
    print(diversity_distributions)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('source_dir', nargs='*', help='')
    args = p.parse_args()

    data = process_files_in_dirs(args.source_dir)
    basic_metrics(data)
    