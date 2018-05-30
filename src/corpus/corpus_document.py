
import os

class CorpusDocument(object):
    def __init__(self, _id):
        self._id = _id
        self.is_aquaint2 = "_" in _id
        self.is_aquaint = not self.is_aquaint2

        if self.is_aquaint2:
            self.src, self.lang, rest = _id.split("_")
            self.yyyy = rest[0:4]
            self.mm = rest[4:6]
            self.dd = rest[6:8]
        else:
            self.src = _id[0:3]
            self.yyyy = _id[3:7]
            self.mm = _id[7:9]
            self.dd = _id[9:11]

    def id(self):
        return self._id

    def get_path(self):
        if self.is_aquaint:
            # $SRC/$YYYY/$YYYY$mm$dd_$SRC for NYT, $SRC/$YYYY/$YYYY$mm$dd_$SRC_$LANG for xie and apw
            # xie is sometimes xin so hardcoding that too :(
            if self.src == "NYT":
                groups = (self.src.lower(), self.yyyy, "{0}{1}{2}_{3}".format(self.yyyy, self.mm, self.dd, self.src))
            elif self.src == "XIE":
                groups = (self.src.lower(), self.yyyy, "{0}{1}{2}_XIN_ENG".format(self.yyyy, self.mm, self.dd))
            else:
                groups = (self.src.lower(), self.yyyy, "{0}{1}{2}_{3}_ENG".format(self.yyyy, self.mm, self.dd, self.src))
            return os.path.join(*groups)

        else:
            groups = ("data", "{0}_{1}".format(self.src, self.lang), "{0}_{1}_{2}{3}.xml".format(self.src, self.lang, self.yyyy, self.mm))

            return os.path.join(*map(str.lower, groups))
