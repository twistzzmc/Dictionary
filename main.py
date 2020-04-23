from DictLib import *

if __name__ == "__main__":
    files = ["files/pospolite (1).txt", "files/adj.txt", "files/WS_tylko_rzecz.txt", "files/adv.txt"]
    file_types = [0, 1, 2, 1]
    bt = DictLib(files, file_types)  # creates WordLib structure
    bt.print_word("biały")
