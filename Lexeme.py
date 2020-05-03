from Labels import Labels, Przyslowek, Czasownik, Forms


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
        else:
            self.basic_form = "None"
            self.flectional_label = "None"
            self.label = "None"
            self.flection = "None"
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]

    @staticmethod
    def pairwise(list_):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(list_)
        return zip(a, a)

    def __repr__(self):
        lexeme = f"Basic form --- {self.basic_form}\nLabel --- {self.flectional_label}\n"
        lexeme += "Flections: \n"
        for flection in self.flection:
            lexeme += "\t" + flection[0] + " --- " + str(flection[1]) + "\n"
        if self.multi_segments:
            lexeme += "Multi segments: \n"
            for multi_segment in self.multi_segments:
                lexeme += f"\t{str(multi_segment)}"
        return lexeme


class NounLexeme(Lexeme):  # Rzeczownik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular, multi_segments)
        self.label = Labels.RZECZOWNIK
        for index, word in enumerate(regular):
            if index in {0, 1}:
                continue
            self.flection.append((word, self.label.get_enum(index - 2)))
        self.gerundive = False
        if filter_structure and Czasownik.Gerundive in filter_structure.forms.keys():
            self.is_gerundive = True
            self.flection.append((filter_structure.forms[Czasownik.Infinitive][0], Czasownik.Infinitive))
            self.verb_data = filter_structure.forms[Czasownik.Infinitive]

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
        self.label = Labels.CZASOWNIK
        for index, word in enumerate(regular):
            if index in {0, 1}:
                continue
            if word.isalpha():
                self.flection.append((word, self.label.get_enum(index - 2)))
        participles = [Czasownik.Present_Adverbial_Participle, Czasownik.Active_Adjectival_Participle,
                       Czasownik.Passive_Adjectival_Participle, Czasownik.Perfect_Adverbial_Participle]
        self.participles = dict()
        if filter_structure:
            for participle in participles:
                if participle in filter_structure.forms.keys():
                    self.flection.append((filter_structure.forms[participle][0], participle))
                    self.participles[participle] = filter_structure.forms[participle]
            if Czasownik.Gerundive in filter_structure.forms.keys():
                self.flection.append((filter_structure.forms[Czasownik.Gerundive][0], Czasownik.Gerundive))
                self.gerundive = filter_structure.forms[Czasownik.Gerundive]

    def get_participles_enums(self):
        return self.participles

    def get_present_adverbial_participle_data(self):
        enum = Czasownik.Present_Adverbial_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_active_adjectival_participle_data(self):
        enum = Czasownik.Active_Adjectival_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_passive_adjectival_participle_data(self):
        enum = Czasownik.Passive_Adjectival_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_perfect_adverbial_participle_data(self):
        enum = Czasownik.Perfect_Adverbial_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_gerundive_data(self):
        enum = Czasownik.Gerundive
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None


class AdjectiveLexeme(Lexeme):  # Przymiotnik
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


class NumeralLexeme(Lexeme):  # Liczebnik
    def __init__(self, regular, filters=None, mulit_segments=None):
        super().__init__(regular, filters, mulit_segments)


class PronounLexeme(Lexeme):  # Zaimek
    def __init__(self, regular, filters=None, mulit_segments=None):
        super().__init__(regular, filters, mulit_segments)


class AdverbLexeme(Lexeme):  # Przysłówek
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular, multi_segments)
        self.is_gradable = False
        self.flection.append((regular[0], Przyslowek.Positive_Form))
        if filter_structure:
            self.is_gradable = True
            self.flection.append((filter_structure.forms[Przyslowek.Comparative_Form][0], Przyslowek.Comparative_Form))
            self.flection.append((filter_structure.forms[Przyslowek.Superlative_Form][0], Przyslowek.Superlative_Form))


class UninflectedLexeme(Lexeme):  # Nieodmienne
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


class TextLexeme(Lexeme):  # Text
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


class AcronymLexeme(Lexeme):  # Skrótowiec, Akronim
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)
