import unittest, types

from flection_dictionary.DictLib import DictLib
from flection_dictionary.Labels import Verb, Adjective, Numeral, Noun


class TestDictLib(unittest.TestCase):
    def setUp(self):
        files = ["../files/pospolite (1).txt", "../files/adj.txt", "../files/WS_tylko_rzecz.txt", "../files/adv.txt",
                 "../files/im_nom.txt"]
        file_types = [0, 1, 2, 1, 1]
        self.bt = DictLib(files, file_types)

    def test_if_find_zlego_return_2_lexemes(self):
        lexemes = self.bt.find("złego")
        self.assertEqual(len(lexemes), 2)

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

    def test_get_verb_data_grzmienie_returns_grzmiec_lexeme_data(self):
        lexeme = self.bt.get_lexeme(("grzmienie", "ABCA"))
        result = self.bt.get_lexeme(lexeme.get_verb_data())
        expected = self.bt.get_lexeme(("grzmieć", "BBBB"))
        self.assertEqual(result, expected)

    def test_get_gerundive_data_bielic_returns_bielenie_lexeme_data(self):
        lexeme = self.bt.get_lexeme(("bielić", "BBCA"))
        result = self.bt.get_lexeme(lexeme.get_gerundive_data())
        expected = self.bt.get_lexeme(("bielenie", "ABCA"))
        self.assertEqual(result, expected)

    def test_get_gerundive_data_wolno_returns_none(self):
        lexeme = self.bt.get_lexeme(("wolno", "BFBA"))
        result = lexeme.get_gerundive_data()
        self.assertEqual(result, None)

    def test_get_grades_for_lepszy(self):
        lexeme = self.bt.get_lexeme(("większy", "*CAB"))
        result = lexeme.get_grades()
        expected = {Adjective.Positive_Form: ("duży", "*CAB"), Adjective.Superlative_Form: ("największy", "*CAB")}
        self.assertEqual(result, expected)

    def test_get_participle_kind_for_zjedzony(self):
        lexeme = self.bt.get_lexeme(("zjedzony", "CAB"))
        result = lexeme.get_participle_kind()
        expected = Verb.Passive_Adjectival_Participle
        self.assertEqual(result, expected)

    def test_is_participle_for_zjedzony_true(self):
        lexeme = self.bt.get_lexeme(("zjedzony", "CAB"))
        result = lexeme.is_participle
        self.assertEqual(result, True)

    def test_is_gradable_for_zjedzony_false(self):
        lexeme = self.bt.get_lexeme(("zjedzony", "CAB"))
        result = lexeme.is_gradable
        self.assertEqual(result, False)

    def test_get_verb_data_for_zjedzony_is_zjesc(self):
        lexeme = self.bt.get_lexeme(("zjedzony", "CAB"))
        result = lexeme.get_verb_data()
        expected = ("zjeść", "BDD")
        self.assertEqual(result, expected)

    def test_get_participle_kind_for_zjadlszy(self):
        lexeme = self.bt.get_lexeme(("zjadłszy", "G"))
        result = lexeme.get_participle_kind()
        expected = Verb.Perfect_Adverbial_Participle
        self.assertEqual(result, expected)

    def test_get_verb_data_for_zjadlszy_is_zjesc(self):
        lexeme = self.bt.get_lexeme(("zjadłszy", "G"))
        result = lexeme.get_verb_data()
        expected = ("zjeść", "BDD")
        self.assertEqual(result, expected)
