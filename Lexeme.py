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
        self.basic_form = regular[0]
        self.flectional_label = regular[1]
        self.label = Labels.get_label_from_flectional_label(regular[1])
        self.flection = self._handle_flection(regular, filters)
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]

        print(self.basic_form, self.flectional_label, self.label)
        print(self.flection)
        print(self.multi_segments)

        print(regular)
        print(filters)
        print(multi_segments)
        print()

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
        filter = self._get_my_filter(filters)
        filter_words = []
        if filter:
            for word, flectional_label in self.pairwise(filter):
                if flectional_label not in {"#", "*"}:
                    filter_words.append((word, flectional_label))
        return filter_words

    def _get_my_filter(self, filters):
        for filter in filters:
            if self.flectional_label == filter[1]:
                return filter

    @staticmethod
    def pairwise(list_):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(list_)
        return zip(a, a)