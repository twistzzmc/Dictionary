import marisa_trie as mt
from Parser import *
import pygtrie
import time


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
        for i in range(len(file_paths)):
            if file_types[i] == 0:  # 0 - regular file
                self.regulars = parse_regular_file(file_paths[i])
                words_map = self.parse_regulars(self.regulars, words_map)

            if file_types[i] == 1:  # 1 - filter file
                self.filters = parse_regular_file(file_paths[i])
                words_map = self.parse_filters(self.filters, words_map)

            # TODO 2 - multi segment file

        bt = self.pack_multiple_nodes(list(words_map.keys()), list(words_map.values()))
        self.binary_trie = bt
        print(len(bt.items()))  # checking how many words are in the trie

    @staticmethod
    def parse_regulars(regulars, words_map):
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
    def parse_filters(filters, words_map):
        for i in range(len(filters)):
            for j in range(len(filters[i])):
                if filters[i][j] not in words_map:
                    words_map[filters[i][j]] = WordNode(filters[i])
                elif i not in words_map.get(filters[i][j]).filters:
                    words_map.get(filters[i][j]).filters.append(i)

        return words_map

    @staticmethod
    def pack_multiple_nodes(keys, nodes):
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
