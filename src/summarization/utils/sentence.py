class Sentence(object):
    def __init__(self, sentence_index, doc_id, text, timestamp):
        self.sentence_index = sentence_index
        self.doc_id = doc_id
        self.text = text
        self.timestamp = timestamp