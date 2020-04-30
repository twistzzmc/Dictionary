from DictLib import *
import time
import marisa_trie as mt
import os

if __name__ == "__main__":
    files = ["files/pospolite (1).txt", "files/adj.txt", "files/WS_tylko_rzecz.txt", "files/adv.txt", "files/im.txt"]
    file_types = [0, 1, 2, 1, 1]
    bt = DictLib(files, file_types)  # creates WordLib structure
    # bt.print_word("amatorsko")
    biel = bt.find("bielić")
    for b in biel:
        print(b)

    # bt.print_word("biały")

    # bt.save()
    # dl = bt.load()
    # print("Załadowany")
    # while True:
    #     input_ = input()
    #     if input_ == "exit":
    #         break
    #     bt.find(input_)
    # bt.delete()
