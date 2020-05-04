import unittest, types

from flection_dictionary.DictLib import DictLib
from flection_dictionary.Labels import Czasownik, Przymiotnik


class TestDictLib(unittest.TestCase):
    def setUp(self):
        files = ["../files/pospolite (1).txt", "../files/adj.txt", "../files/WS_tylko_rzecz.txt", "../files/adv.txt",
                 "../files/im_nom.txt"]
        file_types = [0, 1, 2, 1, 1]
        self.bt = DictLib(files, file_types)

    def test_find_czasownik_in_jedzac(self):
        lexem = self.bt.get_lexem(("jedząc", "G"))
        result = lexem.find_flection(Czasownik.Infinitive)
        self.assertEqual(result, "jeść")

    def test_rasing_error_while_searching_wrong_enum(self):
        lexem = self.bt.get_lexem(("jedząc", "G"))
        with self.assertRaises(ValueError):
            result = lexem.find_flection(Przymiotnik.Positive_Form)


