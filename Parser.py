from codecs import open


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


def parse_multi_segment_file(path):
    utf8 = False
    try:
        with open(path, encoding="utf8") as f:
            f.read()
        utf8 = True
    except:
        pass

    if not utf8:
        file = open(path, "r", encoding='cp1250')
    else:
        file = open(path, "r", encoding='utf8')

    words = []
    lines = []
    for line in file:
        line = line.strip('\n')
        line = line.replace('\r', '')
        line = line.replace('\t', '')
        split_line = line.split(';')
        for i in range(len(split_line)):
            split_line[i] = split_line[i].strip()
        lines.append(split_line)

        split_word = split_line[0].split(' ')
        for i in range(len(split_word) - 1, -1, -1):
            if split_word[i] == '' or split_word[i] == '$' or split_word[i] == '#':
                split_word.pop(i)
            else:
                is_label = True
                for j in range(len(split_word[i])):
                    if split_word[i][j] == '*':
                        is_label = True
                        break
                    elif ord(split_word[i][j]) > 90 or ord(split_word[i][j]) < 60:
                        is_label = False
                        break
                if is_label:
                    split_word.pop(i)
        words.append(split_word)

    file.close()

    return lines, words
