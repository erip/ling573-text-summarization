class Story(object):
    def __init__(self, headline, sentences, raw_text, spans):
        """
        A single story from a newspaper
        :param headline: string
        :param sentences: nested list of lists (tokenized into both sentences and words)
        :param raw_text: a block string of the story
        :param spans: a list of tuples of the sentence boundaries
        """
        self.headline = headline
        self.sentences = sentences
        self.raw_text = raw_text
        self.spans = spans

    def get_sentences(self):
        return self.sentences

    def get_headline(self):
        return self.headline

    def get_raw(self, span=None):
        """Return the raw text. If tuple is provided, return only raw text that spans over those indices"""
        if not span:
            return self.raw_text
        else:
            return self.raw_text[span[0]:span[1]]

    def get_spans(self):
        return self.spans

    def num_sentences(self):  # this counts based on spans because sometimes they disagree. Which is weird since it's the same tokenizer, but will add that to backlog
        return len(self.spans)
