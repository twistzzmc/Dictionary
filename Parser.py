def parse_regular_file(path):
    file = open(path, "r", encoding='utf8')

    words = []

    for line in file:
        split_line = line.split(":")

        for i in range(len(split_line)):
            new_word = split_line[i].strip("\t")
            new_word = split_line[i].strip()
            split_line[i] = new_word
        split_line.pop()

        words.append(split_line)

    file.close()

    return words
