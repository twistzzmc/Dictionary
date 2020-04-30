from Labels import Labels


class MultiSegment:
    def __init__(self, line):
        self.line = line

    def __repr__(self):
        #TODO change repr
        return str(self.line)


class Lexeme:
    """
    Basic_form, flectional_label i label są chyba dobre.
    flection dla wszystkich słów występujących w regular powinno też być dobrze
    ale sprawdź dla tych co się usuwało czy na pewno (ja nie ogarniam tego)

    Problem w flection z filtrami, dodałem na końcu listu jako para słowo z etykietą
    (jak było w pliku z filtrem)

    Multi segment dobrze, tylko trzeba dodać dobre motody w klasie MultiSegment i powinno śmigać
    Zostawiłem printy do zobaczenia jak to wygląda
    """
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

    @staticmethod
    def _get_filters(filters):
        filter_words = []
        for filter_line in filters:
            for i in range(0, len(filter_line), 2):
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
