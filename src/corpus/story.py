class Story(object):
    def __init__(self, sentences):
        """
        A single story
        :param sentences: nested list of lists (tokenized into both sentences and words)
        """
        self.sentences = sentences