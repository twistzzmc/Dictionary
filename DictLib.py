import marisa_trie as mt
from Parser import *
from Labels import Forms
import os
import pickle


class WordNode:
    def __init__(self, regulars=None, filters=None, multi_segment=None):
        self.regulars = [] if regulars is None else regulars
        self.filters = [] if filters is None else filters
        self.multi_segment = [] if multi_segment is None else multi_segment

    def __repr__(self):
        return "Regulars: " + str(self.regulars) + \
               " Filters: " + str(self.filters) + \
               " Multi Segments: " + str(self.multi_segment)

    def pack_to_string(self):
        """
        Changing WordNode into string so it can be fit into BytesTrie
        :return: str
        """
        filter_index = 4 + len(self.regulars)
        multi_segment_index = filter_index + len(self.filters) + 1

        index_list = [3, filter_index, multi_segment_index] + [len(self.regulars)] + self.regulars + \
                     [len(self.filters)] + self.filters + [len(self.multi_segment)] + self.multi_segment

        index_list = str(index_list)
        index_list = index_list.replace(" ", "")
        index_list = index_list.replace("\'", "")
        index_list = index_list.replace("]", ",")
        index_list = index_list.strip("[")

        return index_list

    @staticmethod
    def unpack_from_string(string):
        """
        Change the string into WordNode
        :param string: str
        :return: WordNode
        """
        if not isinstance(string, str):
            string = str(string)
            string = string[:len(string) - 2]
            string = string[3:]

        index_list = []
        number = ''
        for c in string:
            if c != ',':
                number += c
            else:
                index_list.append(int(number))
                number = ''

        regulars = index_list[index_list[0] + 1:index_list[0] + 1 + index_list[index_list[0]]]
        filters = index_list[index_list[1] + 1:index_list[1] + 1 + index_list[index_list[1]]]
        multi_segments = index_list[index_list[2] + 1:index_list[2] + 1 + index_list[index_list[2]]]

        return WordNode(regulars, filters, multi_segments)

    def get_regular_lines(self, regulars):
        lines = []
        for idx in self.regulars:
            lines.append(regulars[idx])
        return lines

    def get_filter_lines(self, filters):
        lines = []
        for idx in self.filters:
            lines.append(filters[idx])
        return lines

    def get_multi_segment_lines(self, multi_segments):
        lines = []
        for idx in self.multi_segment:
            lines.append(multi_segments[idx])
        return lines


class DictLib:
    def __init__(self, file_paths, file_types):
        self.binary_trie = None
        self.regulars = []
        self.filters = []
        self.multi_segment = []

        words_map = {}
        all_regulars = []
        all_filters = []
        all_multi_segments = []
        all_multi_segments_words = []

        for i in range(len(file_paths)):
            if file_types[i] == 0:  # 0 - regular file
                all_regulars += parse_regular_file(file_paths[i])

            if file_types[i] == 1:  # 1 - filter file
                all_filters += parse_regular_file(file_paths[i])

            if file_types[i] == 2:  # 2 - multi segment file
                lines, words = parse_multi_segment_file(file_paths[i])
                all_multi_segments += lines
                all_multi_segments_words += words

        self.regulars = all_regulars
        self.filters = all_filters
        self.multi_segment = all_multi_segments

        words_map = self._parse_regulars(self.regulars, words_map)
        words_map = self._parse_filters(self.filters, words_map)
        self._parse_multi_segments(all_multi_segments_words, words_map)

        bt = self._pack_multiple_nodes(list(words_map.keys()), list(words_map.values()))
        self.binary_trie = bt
        # print(len(bt.items()))  # checking how many words are in the trie

    def print_word(self, word):
        string = self.binary_trie.get(word)
        string = WordNode.unpack_from_string(string)
        lines = self.get_regular_lines(string)
        forms = Forms()
        for i, l in enumerate(lines):
            if i == 0:
                print("Regulars:")
                for line in l:
                    print(forms.get_forms(line, word))
                    print("Forma podstawowa:", line[0])
                    print(line)
            else:
                if i == 1:
                    print("\nFilters:")
                else:
                    print("\nMulti segments:")
                for line in l:
                    print("Forma podstawowa:", line[0])
                    print(line)

    @staticmethod
    def _parse_regulars(regulars, words_map):
        regulars_count = len(regulars)
        for i in range(regulars_count):

            words_count = len(regulars[i])
            for j in range(1, words_count):
                if j == 1 or '#' in regulars[i][j]:
                    continue
                if regulars[i][j] not in words_map:
                    words_map[regulars[i][j]] = WordNode(regulars=[i])
                elif i not in words_map.get(regulars[i][j]).regulars:
                    words_map.get(regulars[i][j]).regulars.append(i)

        return words_map

    @staticmethod
    def _parse_filters(filters, words_map):
        for i in range(len(filters)):
            for j in range(len(filters[i])):
                if filters[i][j] not in words_map:
                    words_map[filters[i][j]] = WordNode(filters=[i])
                elif i not in words_map.get(filters[i][j]).filters:
                    words_map.get(filters[i][j]).filters.append(i)

        return words_map

    @staticmethod
    def _parse_multi_segments(multi_segments, words_map):
        for i in range(len(multi_segments)):
            for j in range(len(multi_segments[i])):
                if multi_segments[i][j] not in words_map:
                    words_map[multi_segments[i][j]] = WordNode(multi_segment=[i])
                elif i not in words_map.get(multi_segments[i][j]).multi_segment:
                    words_map.get(multi_segments[i][j]).multi_segment.append(i)

    @staticmethod
    def _pack_multiple_nodes(keys, nodes):
        values = []
        for node in nodes:
            values.append(bytes(node.pack_to_string(), encoding='utf8'))

        binary_trie = mt.BytesTrie(zip(keys, values))

        return binary_trie

    def get_regular_lines(self, node):
        regulars = node.get_regular_lines(self.regulars)
        filters = node.get_filter_lines(self.filters)
        multi_segments = node.get_multi_segment_lines(self.multi_segment)

        lines = [regulars, filters, multi_segments]

        return lines

    def save(self, file_name='DictLib'):
        if os.path.isfile(file_name + '.pickle'):
            raise ValueError('File with name \"' + file_name + '\" already exists! Change name or delete file.')

        pickle.dump(self, open(file_name + '.pickle', 'wb'))

    @staticmethod
    def delete(file_name='DictLib'):
        if os.path.isfile(file_name + '.pickle'):
            os.remove(file_name + '.pickle')

    @staticmethod
    def load(file_name='DictLib'):
        return pickle.load(open(file_name + '.pickle', 'rb'))

    # Used for tests for the alternative pygtrie library (slower but more convenient)

    # @staticmethod
    # def pygtrie_tests():
    #     regulars = parse_regular_file('files/pospolite (1).txt')
    #
    #     pg = pygtrie.StringTrie()
    #
    #     for i in range(len(regulars)):
    #         for j in range(1, len(regulars[i])):
    #             if j == 1 or '#' in regulars[i][j]:
    #                 continue
    #             if regulars[i][j] not in pg:
    #                 word_node = WordNode()
    #                 word_node.regulars.append(i)
    #                 pg.update([(regulars[i][j], word_node)])
    #             else:
    #                 word_node = pg.get(regulars[i][j])
    #                 if i not in word_node.regulars:
    #                     word_node.regulars.append(i)
