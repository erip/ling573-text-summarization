class Docset(object):
    def __init__(self, docset_id, docset):
        self.docset_id = docset_id
        self.docset = docset

    def __iter__(self):
        yield from self.docset

    def __len__(self):
        return len(self.docset)