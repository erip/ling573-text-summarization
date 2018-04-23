"""
Main Content Selection module, that given a list of sentences will select the important ones to include in a summary.


Next Steps:
Redocument everything
Have a cleanup of the xml into nice form
Make graph and understand graph algorithms
Error analysis methods
ROUGE Evaluation plug in

Have meeting and assign remainder parts of module

"""
#TODO Add thresholding to throw out words with lower than a certain tfidf weight?
#TODO should the limitations on length of summary be in this module or later?


from collections import Counter, defaultdict

import math
import numpy as np


class ContentSelection():
    """Not quite sure yet """
    def __init__(self, all_content):
        self.all_content = all_content #list of content from each doc in docSetA - [sent1, sent2, ...]
        self.d_size = len(all_content) #|D|
        self.word_freq_table = Counter()
        self.sent_freq_table = defaultdict(lambda: defaultdict(int))
        self.idf_values = defaultdict()
        self.word2idx = defaultdict() # len is vocab size


    def word_freq_corpus(self):
        """
        generate word frequencies for whole corpus

        make a dict of word_freq in whole given corpus of form {word_id: freq} and a nested dict of sent_freq
        (word freq on a per sent level) of form {sent_id: word_id: freq} and set as class attributes
        :return: no value
        """
        vocab_counter = 0

        #FIRST ITERATION
        #calculate word frequencies
        for sent_id in range(self.d_size):
            for word in self.all_content[sent_id]:
                #create word to id mapping
                if not(word in self.word2idx):
                    self.word2idx[word] = vocab_counter
                    vocab_counter += 1

                self.word_freq_table[self.word2idx[word]] += 1
                self.sent_freq_table[sent_id][self.word2idx[word]] += 1

    def calc_idf(self):
        """
        calculate and store IDF for all words in corpus
        :return: no value
        """
        # idf weights for a word are constant, tf weights for a word change by each sentence. So can precalc idf only.
        for word_id in self.word_freq_table:
            self.idf_values[word_id] = self.idf_helper(word_id)

    def idf_helper(self, word_id):
        #TODO: change to corpus
        #TODO: figure out if there is a standard for log base (though shouldn't matter as long as consistent)
        """
        Take a word id, return inverse document frequency.

        :param word_id: word in the corpus
        :return: idf of word
        """

        return math.log(self.d_size / self.word_freq_table[word_id])

    def make_tdfidf_vec(self):
        #TODO revise the docstring to reflect new functionality
        """
        Make tfidf vectors and....do something with them

        """

        tfidf_matrix = np.zeros((self.d_size, len(self.word_freq_table)))

        for sent_id in range(self.d_size):
            for word_id in self.sent_freq_table[sent_id]:
                # populate cells in each sent row with tfidf weights
                tfidf_matrix[sent_id][word_id] = self.sent_freq_table[sent_id][word_id] * self.idf_values[word_id]

        print(tfidf_matrix)


if __name__ == "__main__":
    test_strings = ['the project will provide the project electricity', 'the project project will not provide the water']
    test_strings = [sent.split() for sent in test_strings]

    MyContentSelection = ContentSelection(test_strings)

    MyContentSelection.word_freq_corpus()
    MyContentSelection.calc_idf()
    MyContentSelection.make_tdfidf_vec()

    #TODO have make_tfidf call the other method functions if values not set (rahter than requiring us to call them all)





