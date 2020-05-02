from enum import Enum
from Labels import Labels, Przyslowek, Przymiotnik, Czasownik
from Lexeme import Lexeme


class Filters(Enum):
    AdverbComparison = 1
    AdjectionComparison = 2
    Participles = 3
    ParticiplesAndGerundive = 4


class FilterStructure:
    forms = dict()

    def __init__(self, filter):
        label_of_first = Labels.get_label_from_flectional_label(filter[1])
        if label_of_first == Labels.PRZYSLOWEK:
            self.forms[Przyslowek.Positive_Form] = (filter[0], filter[1])
            self.forms[Przyslowek.Comparative_Form] = (filter[2], filter[3])
            self.forms[Przyslowek.Superlative_Form] = (filter[4], filter[5])
            self.filter_kind = Filters.AdverbComparison
        elif label_of_first == Labels.PRZYMIOTNIK:
            self.forms[Przymiotnik.Positive_Form] = (filter[0], filter[1])
            self.forms[Przymiotnik.Comparative_Form] = (filter[2], filter[3])
            self.forms[Przymiotnik.Superlative_Form] = (filter[4], filter[5])
            self.filter_kind = Filters.AdjectionComparison
        elif label_of_first == Labels.CZASOWNIK:
            self.forms[Czasownik.Infinitive] = (filter[0], filter[1])
            self.forms[Czasownik.Present_Adverbial_Participle] = (filter[2], filter[3])
            self.forms[Czasownik.Active_Adjectival_Participle] = (filter[4], filter[5])
            self.forms[Czasownik.Passive_Adjectival_Participle] = (filter[6], filter[7])
            self.forms[Czasownik.Perfect_Adverbial_Participle] = (filter[8], filter[9])
            if len(filter) == 10:
                self.filter_kind = Filters.Participles
            elif len(filter) == 12:
                self.filter_kind = Filters.ParticiplesAndGerundive
                self.forms[Czasownik.Gerundive] = (filter[10], filter[11])

    @staticmethod
    def get_filter_structures(filters):
        filter_structures = []
        for filter in filters:
            filter_structures.append(FilterStructure(filter))
        return filter_structures
