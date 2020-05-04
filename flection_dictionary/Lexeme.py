from flection_dictionary.Labels import Labels, Adverb, Verb, Adjective
from flection_dictionary.Filters import Filters

class MultiSegment:
    def __init__(self, line):
        self.line = line

    def __repr__(self):
        line = []
        line += self.line[0].split(' ')

        for i in range(len(line) - 1, -1, -1):
            if line[i] == '' or line[i] == '$' or line[i] == '#':
                line.pop(i)
            else:
                is_label = True
                for j in range(len(line[i])):
                    if line[i][j] == '*':
                        is_label = True
                        break
                    elif ord(line[i][j]) > 90 or ord(line[i][j]) < 60:
                        is_label = False
                        break
                if is_label:
                    line.pop(i)
        multi_segment = ''
        for word in line:
            multi_segment += word + ' '
        return multi_segment


class Lexeme:
    def __init__(self, regular, multi_segments=None):
        if regular is not None:
            self.basic_form = regular[0]
            self.flectional_label = regular[1]
            self.flection = []
            self.label = Labels.get_label_from_flectional_label(self.flectional_label)
            for index, word in enumerate(regular):
                if index in {0, 1}:
                    continue
                if word.isalpha():
                    self.flection.append((word, self.label.get_enum(index - 2)))
        else:
            self.basic_form = "None"
            self.flectional_label = "None"
            self.label = "None"
            self.flection = []
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]

    @staticmethod
    def pairwise(list_):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(list_)
        return zip(a, a)

    def __repr__(self):
        lexeme = f"Basic form --- {self.basic_form}\nLabel --- {self.flectional_label} - {self.label}\n"
        lexeme += "Flections: \n"
        for flection in self.flection:
            lexeme += "\t" + flection[0] + " --- " + str(flection[1]) + "\n"
        if self.multi_segments:
            lexeme += "Multi segments: \n"
            for multi_segment in self.multi_segments:
                lexeme += f"\t{str(multi_segment)}"
        return lexeme

    @staticmethod
    def get_key(my_dict, val):
        for key, value in my_dict.items():
            if val == value:
                return key
        return "key doesn't exist"

    def find_flection_enums(self, searched_word):
        enums = []
        for word, enum in self.flection:
            if word == searched_word:
                enums.append(enum)
        return enums

    def find_flection(self, searched_enum):
        allowed_enums = self.label.get_enum_list()
        """rzeczownik może być gerundium; przymiotnik, nieodmienny - imiesłowami"""
        if self.label == Labels.NOUN or self.label == Labels.ADJECTIVE or self.label == Labels.UNINFLECTED:
            allowed_enums.append(Verb.Infinitive)
        print(allowed_enums)
        if searched_enum not in allowed_enums:
            raise ValueError("You cannot search {} in {}".format(searched_enum, self.label))
        for word, enum in self.flection:
            if enum == searched_enum:
                return word
        return None


class NounLexeme(Lexeme):  # Rzeczownik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular, multi_segments)
        self.gerundive = False
        if filter_structure and Verb.Gerundive in filter_structure.forms.keys():
            self.is_gerundive = True
            self.flection.append((filter_structure.forms[Verb.Infinitive][0], Verb.Infinitive))
            self.verb_data = filter_structure.forms[Verb.Infinitive]

    def __repr__(self):
        result = f"{super().__repr__()}\n"
        if self.gerundive:
            result += f"Czasownik: {self.verb_data}"
        return result

    def get_verb_data(self):
        return self.verb_data

    def is_gerundive(self):
        return self.gerundive


class VerbLexeme(Lexeme):  # Czasownik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)
        self.label = Labels.VERB
        participles = [Verb.Present_Adverbial_Participle, Verb.Active_Adjectival_Participle,
                       Verb.Passive_Adjectival_Participle, Verb.Perfect_Adverbial_Participle]
        self.participles = dict()
        if filter_structure:
            for participle in participles:
                if participle in filter_structure.forms.keys():
                    self.flection.append((filter_structure.forms[participle][0], participle))
                    self.participles[participle] = filter_structure.forms[participle]
            if Verb.Gerundive in filter_structure.forms.keys():
                self.flection.append((filter_structure.forms[Verb.Gerundive][0], Verb.Gerundive))
                self.gerundive = filter_structure.forms[Verb.Gerundive]

    def get_present_adverbial_participle_data(self):
        enum = Verb.Present_Adverbial_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_active_adjectival_participle_data(self):
        enum = Verb.Active_Adjectival_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_passive_adjectival_participle_data(self):
        enum = Verb.Passive_Adjectival_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_perfect_adverbial_participle_data(self):
        enum = Verb.Perfect_Adverbial_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_gerundive_data(self):
        if self.gerundive:
            return self.gerundive
        else:
            return None


class AdjectiveLexeme(Lexeme):  # Przymiotnik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)
        self.is_gradable = False
        self.is_participle = False
        if filter_structure:
            if filter_structure.filter_kind == Filters.AdjectionComparison:
                my_grade = Lexeme.get_key(filter_structure.forms, (self.basic_form, self.flectional_label))
                grades = {Adjective.Positive_Form, Adjective.Comparative_Form, Adjective.Superlative_Form}
                grades.remove(my_grade)
                self.grades = dict()
                for grade in grades:
                    self.flection.append((filter_structure.forms[grade][0], grade))
                    self.grades[grade] = filter_structure.forms[grade]
                self.is_gradable = True
                self.my_grade = my_grade
            else:
                self.flection.append((filter_structure.forms[Verb.Infinitive][0], Verb.Infinitive))
                self.is_participle = True
                self.verb_data = filter_structure.forms[Verb.Infinitive]

    def get_grades(self):
        if hasattr(self, "grades"):
            return self.grades
        return None

    def get_verb_data(self):
        if hasattr(self, "verb_data"):
            return self.verb_data
        return None

    def get_my_grade(self):
        if hasattr(self, "my_grade"):
            return self.my_grade
        return None


class NumeralLexeme(Lexeme):  # Liczebnik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)


class PronounLexeme(Lexeme):  # Zaimek
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)


class AdverbLexeme(Lexeme):  # Przysłówek
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular, multi_segments)
        if filter_structure:
            if filter_structure.filter_kind == Filters.AdverbComparison:
                self.is_gradable = True
                self.my_grade = Adverb.Positive_Form
                grades = [Adverb.Comparative_Form, Adverb.Superlative_Form]
                self.grades = dict()
                for grade in grades:
                    self.flection.append((filter_structure.forms[grade][0], grade))
                    self.grades[grade] = filter_structure.forms[grade]
        else:  # w pospolite niestopniowalne przysłówki nie mają 3 kolumny :/
            self.flection.append((regular[0], Adverb.Positive_Form))
            self.is_gradable = False


class UninflectedLexeme(Lexeme):  # Nieodmienne
    def __init__(self, regular, filter_structure, multi_segments=None):
        self.basic_form = regular[0]
        self.flectional_label = regular[1]
        self.flection = []
        self.label = Labels.UNINFLECTED
        self.flection.append((regular[2], Labels.UNINFLECTED))
        self.is_participle = False
        if filter_structure:  # imiesłów przysłówkowy
            self.flection.append((filter_structure.forms[Verb.Infinitive][0], Verb.Infinitive))
            self.is_participle = True
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]


class TextLexeme(Lexeme):  # Text
    def __init__(self, regular, filter_structure, multi_segments=None):
        self.basic_form = regular[0]
        self.flectional_label = regular[1]
        self.flection = []
        self.label = Labels.TEXT
        self.flection.append((regular[2], Labels.TEXT))
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]


class AcronymLexeme(Lexeme):  # Skrótowiec, Akronim
    def __init__(self, regular, filter_structure, multi_segments=None):
        self.basic_form = regular[0]
        self.flectional_label = regular[1]
        self.flection = []
        self.label = Labels.ACRONYM
        self.flection.append((regular[2], Labels.ACRONYM))
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]
