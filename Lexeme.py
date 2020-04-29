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
        self.label = Labels(regular[1][0]) if regular[1][0] != '*' else Labels(regular[1][1])
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
        for i in range(len(regular) - 2):
            if self.label == Labels.CZASOWNIK:
                if i >= 11:
                    enum_type = self.label.get_enum(i - 2)
                elif i >= 8:
                    enum_type = self.label.get_enum(i - 1)
                else:
                    enum_type = self.label.get_enum(i)
            elif self.label == Labels.PRZYMIOTNIK:
                if i >= 43:
                    enum_type = self.label.get_enum(i - 2)
                elif i >= 42:
                    enum_type = self.label.get_enum(i - 1)
                else:
                    enum_type = self.label.get_enum(i)
            elif self.label == Labels.PRZYSLOWEK:
                if i >= 2:
                    enum_type = self.label.get_enum(i - 2)
                elif i >= 1:
                    enum_type = self.label.get_enum(i - 1)
                else:
                    enum_type = self.label.get_enum(i)
            else:
                enum_type = self.label.get_enum(i)

            flection.append((regular[i + 2], enum_type))

        for filter_word in self._get_filters(filters):
            flection.append(filter_word)

        return flection

    def _get_filters(self, filters):
        filter_words = []
        for i in range(len(filters)):
            if i % 2 == 0 and self.basic_form != filters[i] and '#' not in filters[i]:
                filter_words.append((filters[i], filters[i + 1]))
        return filter_words
