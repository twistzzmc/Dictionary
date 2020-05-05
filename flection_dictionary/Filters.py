from enum import Enum
from flection_dictionary.Labels import Labels, Adverb, Adjective, Verb


class Filters(Enum):
    AdverbComparison = 1
    AdjectionComparison = 2
    Participles = 3
    ParticiplesAndGerundive = 4


class FilterStructure:
    def __init__(self, filter):
        self.forms = dict()
        label_of_first = Labels.get_label_from_flectional_label(filter[1])
        if label_of_first == Labels.ADVERB:
            self.forms[Adverb.Positive_Form] = (filter[0], filter[1])
            self.forms[Adverb.Comparative_Form] = (filter[2], filter[3])
            self.forms[Adverb.Superlative_Form] = (filter[4], filter[5])
            self.filter_kind = Filters.AdverbComparison
        elif label_of_first == Labels.ADJECTIVE:
            self.forms[Adjective.Positive_Form] = (filter[0], filter[1])
            self.forms[Adjective.Comparative_Form] = (filter[2], filter[3])
            self.forms[Adjective.Superlative_Form] = (filter[4], filter[5])
            self.filter_kind = Filters.AdjectionComparison
        elif label_of_first == Labels.VERB:
            self.forms[Verb.Infinitive] = (filter[0], filter[1])
            participles = [Verb.Present_Adverbial_Participle, Verb.Active_Adjectival_Participle,
                           Verb.Passive_Adjectival_Participle, Verb.Perfect_Adverbial_Participle]
            for index, participle in enumerate(participles):
                if filter[2 * index + 2].isalpha():  # nie jest puste
                    self.forms[participle] = (filter[2 * index + 2], filter[2 * index + 3])
            if len(filter) == 10:
                self.filter_kind = Filters.Participles
            elif len(filter) == 12:
                self.filter_kind = Filters.ParticiplesAndGerundive
                if filter[10].isalpha():  # nie jest puste
                    self.forms[Verb.Gerundive] = (filter[10], filter[11])

    def __repr__(self):
        return str(self.forms) + str(self.filter_kind)

    @staticmethod
    def get_filter_structures(filters):
        filter_structures = []
        for filter in filters:
            filter_structure = FilterStructure(filter)
            filter_structures.append(filter_structure)
        return filter_structures
