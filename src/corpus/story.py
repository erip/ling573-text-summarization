class Story(object):
    def __init__(self, headline, sentences):
        """
        A single story from a newspaper
        :param headline: string
        :param sentences: nested list of lists (tokenized into both sentences and words)
        :param raw_text: a block string of the story
        :param spans: a list of tuples of the sentence boundaries
        """
        self.headline = headline
        self.sentences = sentences