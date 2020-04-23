from codecs import open
from random import randint, choice
from string import ascii_lowercase, ascii_uppercase

class Generator:

    def __init__(self, ends_path):
        self.vowel = list('aeiouy')
        self.ends_list = dict()
        self.polish_letter_without_vowel = set('bcdfghjklmnprstwz')
        ends = open(ends_path, "r", encoding='utf8')
        for line in ends:
            split_line = line.split(":")
            split_line.pop()
            self.ends_list[split_line[1]] = split_line

    def generate_random_word(self):
        num_letters = randint(3, 9)  # przynajmniej 2 litery w słowie
        word = ""
        for i in range(num_letters):
            if i % 2 == 1:  # przynajmniej połowa to samogłoski
                word += choice(self.vowel)
            else:
                word += choice(ascii_lowercase)
        last_letter = word[-1]
        last_letters = {
            'a': "AD",
            'o': "F",
            'y': "C"
        }
        if last_letter in last_letters.keys():
            return word, last_letters[last_letter]
        kind = choice(['AA', 'AB', 'AC', 'AD', 'AA', 'AB', 'AC', 'AD', 'B', 'B', 'C', 'C', 'D', 'D', 'F', 'G'])
        if kind == 'AA' or kind == 'AB' or kind == 'AC':
            if last_letters in self.vowel:
                word += choice(self.polish_letter_without_vowel)
        elif kind == 'AD':
            if last_letters != 'a':
                word += 'a'
        elif kind == 'B':
            word += 'eść'
        elif kind == 'C':
            word += 'y'
        elif kind == 'D':
            word += 'en'
        elif kind == 'F':
            word += 'no'
        elif kind == 'G':
            kind = choice(['G', 'H', 'I'])
        return word, kind

    def generate_random_kind(self, kind):
        num_letters = randint(1, 6)  # przynajmniej 1 litera dodana do etykiety
        for i in range(num_letters):
            kind += choice(ascii_uppercase)
        return kind

    def generate_words(self, number_of_words):
        file = open("generated.txt", "w", encoding='utf8')
        for i in range(number_of_words):
            word, kind = self.generate_random_word()
            ends = self.ends_list[kind]
            first_end = ends[0]
            if first_end != '':
                word = word.rstrip(first_end)
            flection_list = []
            for i, end in enumerate(ends):
                if i == 1:
                    kind = self.generate_random_kind(kind)
                    flection_list.append(kind)
                else:
                    flection_word = f'{word}{end}'
                    flection_list.append(flection_word)
            result = ":".join(flection_list)
            file.write(result)
            file.write("\n")


if __name__ == "__main__":
    generator = Generator("ends.txt")
    generator.generate_words(1000000)