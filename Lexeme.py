from Labels import Labels


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
    def __init__(self, regular, filters=None, multi_segments=None):
        if regular is not None:
            self.basic_form = regular[0]
            self.flectional_label = regular[1]
            self.label = Labels.get_label_from_flectional_label(regular[1])
            self.flection = self._handle_flection(regular, filters)
        else:
            self.basic_form = "None"
            self.flectional_label = "None"
            self.label = "None"
            self.flection = self._get_filters(filters)
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]

        # print(self.basic_form, self.flectional_label, self.label)
        # print(self.flection)
        # print(self.multi_segments)
        #
        # print(regular)
        # print(filters)
        # print(multi_segments)
        # print()

    @staticmethod
    def get_lexeme(regular, filters=None, multi_segments=None):
        label = regular[1].strip('*')[0] if regular is not None else None

        if label == 'B':
            return LexemeVerb(regular, filters, multi_segments)
        elif label == 'A':
            return LexemeNoun(regular, filters, multi_segments)
        elif label == 'C':
            return LexemeAdjective(regular, filters, multi_segments)
        elif label == 'F':
            return LexemeAdverb(regular, filters, multi_segments)
        elif label == 'DONT KNOW':
            return LexemeParticiple(regular, filters, multi_segments)
        elif label == 'G':
            return LexemeUninflected(regular, filters, multi_segments)
        else:
            return Lexeme(regular, filters, multi_segments)

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
        for filter_line in filters:
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
    # def _get_my_filter(self, filters):
    #     for filter in filters:
    #         if self.flectional_label == filter[1]:
    #             return filter

    @staticmethod
    def pairwise(list_):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(list_)
        return zip(a, a)

    def __repr__(self):
        lexeme = "Basic for --- " + self.basic_form + "\nLabel --- " + self.flectional_label + " --- " + str(self.label)
        lexeme += "\nOther flections: \n"
        for flection in self.flection:
            lexeme += "\t" + flection[0] + " --- " + str(flection[1]) + "\n"

        lexeme += "Multi segments: \n"
        for multi_segment in self.multi_segments:
            lexeme += "\t" + str(multi_segment) + "\n"
        return lexeme + "\n\n"


class LexemeVerb(Lexeme):  # Czasownik
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)

    def get_Present_Adverbial_Participle_lexeme(self):
        # TODO
        return None


class LexemeNoun(Lexeme):  # Rzeczownik
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


class LexemeAdjective(Lexeme):  # Przymiotnik
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


class LexemeAdverb(Lexeme):  # Przysłówek
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


class LexemeParticiple(Lexeme):  # Imiesłów
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)


class LexemeUninflected(Lexeme):  # Nieodmienne
    def __init__(self, regular, filters=None, multi_segments=None):
        super().__init__(regular, filters, multi_segments)
