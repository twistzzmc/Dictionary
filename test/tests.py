import unittest, types

from flection_dictionary.DictLib import DictLib
from flection_dictionary.Labels import Verb, Adjective, Numeral, Noun


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

    def test_find_flection_returns_none_if_such_flection_doesnt_exist(self):
        lexem = self.bt.get_lexeme(("czternaście", "DBCA"))  # nie ma liczby pojedynczej
        result = lexem.find_flection(Numeral.Singular_Nominative_Masculine_Personal)
        self.assertEqual(result, None)

    def test_method_find_flection_enums_for_zjedzenie(self):
        lexem = self.bt.get_lexeme(("zjedzenie", "ABCA"))
        result = lexem.find_flection_enums("zjedzenie")
        expected = [Noun.Singular_Nominative, Noun.Singular_Accusative, Noun.Singular_Vocative]
        self.assertEqual(result, expected)

    def test_method_find_flection_for_zly(self):
        lexem = self.bt.get_lexeme(("zły", "*ABC"))
        result = lexem.find_flection(Noun.Singular_Accusative)
        expected = "złego"
        self.assertEqual(result, expected)
