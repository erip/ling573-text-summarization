
class Topic(object):
    def __init__(self, _id, title, narrative, docset):
        self._id = _id
        self.title = title
        self.narrative = narrative
        self.docset = docset
        self.stories = set()

    def id(self):
        return self._id

    def add_story(self, story):
        self.stories.add(story)

    def add_stories(self, stories):
        self.stories.update(stories)
