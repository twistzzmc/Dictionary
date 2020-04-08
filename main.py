from Parser import *
from DictLib import *
import marisa_trie as mt
import pygtrie
import time

if __name__ == "__main__":
    bt = DictLib(["files/pospolite (1).txt", "files/adj.txt", "files/WS_tylko_rzecz.txt", "files/adv.txt"], [0, 1, 2, 1])  # creates WordLib structure
    string = bt.binary_trie.get("szybko")  # gets the packed value of this word
    string = WordNode.unpack_from_string(string)  # unpacks the value turning it into WordNode type
    lines = bt.get_regular_lines(string)  # gets all associated lines with the word
    for i in range(len(lines)):
        if i == 0:
            print("Regulars:")
        elif i == 1:
            print("\nFilters:")
        else:
            print("\nMulti segments:")
        for line in lines[i]:
            print(line)
