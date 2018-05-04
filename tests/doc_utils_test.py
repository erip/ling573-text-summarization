from unittest import TestCase, skipUnless

from src import Document

import os

class DocumentTestCase(TestCase):

    base_paths = {
        "aquaint": "/aquaint",
        "aquaint2": "/aquaint2"
    }

    def test_aquaint2_parse(self):
        year, month, day = ("2004", "11", "13")

        _id = "0001"
        src = "XIN"
        lang = "ENG"

        doc_id = "{0}_{1}_{2}{3}{4}.{5}".format(src, lang, year, month, day, _id)

        doc = Document(DocumentTestCase.base_paths, doc_id)

        self.assertTrue(doc.is_aquaint2)
        self.assertEqual(doc.yyyy, year)
        self.assertEquals(doc.mm, month)
        self.assertEquals(doc.dd, day)
        self.assertEquals(doc.lang, lang)
        self.assertEquals(doc.src, src)

    @skipUnless(os.path.sep == "/", "Test only works for unix systems")
    def test_aquaint2_to_path(self):
        year, month, day = ("2004", "11", "13")

        _id = "0001"
        src = "XIN"
        lang = "ENG"

        doc_id = "{0}_{1}_{2}{3}{4}.{5}".format(src, lang, year, month, day, _id)

        doc = Document(DocumentTestCase.base_paths, doc_id)

        expected_path = "/aquaint2/data/{0}_{1}/{0}_{1}_{2}{3}.xml".format(src, lang, year, month).lower()
        self.assertEquals(doc.get_path(), expected_path)
        self.assertEquals(doc.id(), doc_id)

    def test_aquaint_parse(self):
        year, month, day = ("1999", "03", "30")

        _id = "0001"
        src = "NYT"

        doc_id = "{0}{1}{2}{3}.{4}".format(src, year, month, day, _id)


        doc = Document(DocumentTestCase.base_paths, doc_id)

        self.assertTrue(doc.is_aquaint)
        self.assertEqual(doc.yyyy, year)
        self.assertEquals(doc.mm, month)
        self.assertEquals(doc.dd, day)
        self.assertEquals(doc.src, src)

    @skipUnless(os.path.sep == "/", "Test only works for unix systems")
    def test_aquaint_xie_to_path(self):
        year, month, day = ("1998", "07", "21")

        _id = "0001"
        src = "XIE"
        real_src = "XIN"

        doc_id = "{0}{1}{2}{3}.{4}".format(src, year, month, day, _id)

        doc = Document(DocumentTestCase.base_paths, doc_id)

        expected_path = "/aquaint/{0}/{1}/{1}{2}{3}_{4}_ENG".format(src.lower(), year, month, day, real_src)
        self.assertEquals(doc.get_path(), expected_path)
        self.assertEquals(doc.id(), doc_id)


    @skipUnless(os.path.sep == "/", "Test only works for unix systems")
    def test_aquaint_xin_to_path(self):
        year, month, day = ("1998", "07", "21")

        _id = "0001"
        src = "XIN"

        doc_id = "{0}{1}{2}{3}.{4}".format(src, year, month, day, _id)

        doc = Document(DocumentTestCase.base_paths, doc_id)

        expected_path = "/aquaint/{0}/{1}/{1}{2}{3}_{4}_ENG".format(src.lower(), year, month, day, src)
        self.assertEquals(doc.get_path(), expected_path)
        self.assertEquals(doc.id(), doc_id)

    @skipUnless(os.path.sep == "/", "Test only works for unix systems")
    def test_aquaint_apw_to_path(self):
        year, month, day = ("1998", "07", "21")

        _id = "0001"
        src = "APW"

        doc_id = "{0}{1}{2}{3}.{4}".format(src, year, month, day, _id)

        doc = Document(DocumentTestCase.base_paths, doc_id)

        expected_path = "/aquaint/{0}/{1}/{1}{2}{3}_{4}_ENG".format(src.lower(), year, month, day, src)
        self.assertEquals(doc.get_path(), expected_path)
        self.assertEquals(doc.id(), doc_id)