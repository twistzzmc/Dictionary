import unittest, types

from flection_dictionary.DictLib import DictLib
from flection_dictionary.Labels import Verb, Adjective


class TestDictLib(unittest.TestCase):
    def setUp(self):
        files = ["../files/pospolite (1).txt", "../files/adj.txt", "../files/WS_tylko_rzecz.txt", "../files/adv.txt",
                 "../files/im_nom.txt"]
        file_types = [0, 1, 2, 1, 1]
        self.bt = DictLib(files, file_types)

    def test_find_czasownik_in_jedzac(self):
        lexem = self.bt.get_lexeme(("jedząc", "G"))
        result = lexem.find_flection(Verb.Infinitive)
        self.assertEqual(result, "jeść")

    def test_rasing_error_while_searching_wrong_enum(self):
        lexem = self.bt.get_lexeme(("jedząc", "G"))
        with self.assertRaises(ValueError):
            result = lexem.find_flection(Adjective.Positive_Form)


