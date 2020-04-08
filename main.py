from Parser import *
from WordNode import *
import marisa_trie as mt
import pygtrie
import time

if __name__ == "__main__":
    bt = WordLib(["files/pospolite (1).txt", "files/adj.txt"], [0, 1])  # creates WordLib structure
    string = bt.binary_trie.get("biały")  # gets the packed value of this word
    string = WordNode.unpack_from_string(string)  # unpacks the value turning it into WordNode type
    lines = bt.get_regular_lines(string)  # gets all associated lines with the word
    for l in lines:
        for line in l:
            print(line)
