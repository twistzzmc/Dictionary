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

    def _handle_flection(self, regular, filters):
        flection = []
        if self.label in {Labels.NIEODMIENNY, Labels.SKROT, Labels.TEKST}:
            flection.append((regular[2], self.label))
        else:
            for i in range(len(regular) - 2):
                enum_type = self.label.get_enum(i)
                flection.append((regular[i + 2], enum_type))

            for filter_word in self._get_filters(filters):
                flection.append(filter_word)

        return flection

    def _get_filters(self, filters):
        filter_words = []
        my_filters = self._get_my_filters(filters)
        for filter_line in my_filters:
            for i in range(0, len(filter_line), 2):
                if self.basic_form != filter_line[i]:
                    if '#' not in filter_line[i] and '#' not in filter_line[i + 1]:
                        filter_words.append((filter_line[i], filter_line[i + 1]))
                    elif '#' not in filter_line[i]:
                        filter_words.append((filter_line[i], None))
        return filter_words

    # def _get_filters(self, filters):
    #     filter = self._get_my_filter(filters)
    #     filter_words = []
    #     if filter:
    #         for word, flectional_label in self.pairwise(filter):
    #             if flectional_label not in {"#", "*"}:
    #                 filter_words.append((word, flectional_label))
    #     return filter_words
    #
    def _get_my_filters(self, filters):
        my_filters = []
        for filter in filters:
            if self.flectional_label == filter[1]:
                my_filters.append(filter)
        return my_filters

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
        self.gerundive = False
        print(regular)
        for index, word in enumerate(regular):
            if index in {0, 1}:
                continue
            self.flection.append((word, self.label.get_enum(index - 2)))
        if Czasownik.Gerundive in filter_structure.forms.keys():
            self.is_gerundive = True
            self.flection.append((filter_structure.forms[Czasownik.Infinitive][0], Czasownik.Infinitive))
            self.verb_data = filter_structure.forms[Czasownik.Infinitive]

    def __repr__(self):
        return f"{super().__repr__()}\n Czasownik: {self.verb_data}"

    def get_verb_data(self):
        return self.verb_data

    def is_gerundive(self):
        return self.gerundive


class VerbLexeme(Lexeme):  # Czasownik
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


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
