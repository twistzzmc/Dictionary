"""
Basic Enum not implemented yet.
"""
from enum import Enum, auto


class Labels(Enum):
    RZECZOWNIK = "A"
    CZASOWNIK = "B"
    PRZYMIOTNIK = "C"
    LICZEBNIK = "D"
    ZAIMEK = "E"
    PRZYSLOWEK = "F"
    NIEODMIENNY = "G"
    TEKST = "H"
    SKROT = "I"

    def __str__(self):
        switcherToName = {
            self.RZECZOWNIK: "Rzeczownik",
            self.CZASOWNIK: "Czasownik",
            self.PRZYMIOTNIK: "Przymiotnik",
            self.LICZEBNIK: "Liczebnik",
            self.ZAIMEK: "Zaimek",
            self.PRZYSLOWEK: "Przysłówek",
            self.NIEODMIENNY: "Nieodmienny",
            self.TEKST: "Tekst",
            self.SKROT: "Skrótowiec"
        }
        return switcherToName.get(self)


class Forms:
    def rzeczownik(self, index):
        enum_list = list(Rzeczownik)
        form = enum_list[index]
        return form.value

    def czasownik(self, index):
        enum_list = list(Czasownik)
        form = enum_list[index]
        return form.value

    def przymiotnik(self, index):
        enum_list = list(Przymiotnik)
        form = enum_list[index]
        return form.value

    def liczebnik(self, index):
        enum_list = list(Liczebnik)
        form = enum_list[index]
        return form.value

    def zaimek(self, index):
        enum_list = list(Zaimek)
        form = enum_list[index]
        return form.value

    def przyslowek(self, index):
        enum_list = list(Przyslowek)
        form = enum_list[index]
        return form.value

    def count_indexes(self, regular_list, checked_word):
        indexes = []
        for index, word in enumerate(regular_list):
            if word == checked_word:
                indexes.append(index)
        if 0 in indexes:
            indexes.remove(0)
        return indexes

    def get_forms(self, regural_list, word):
        indexes = self.count_indexes(regural_list, word)
        flectional_label = regural_list[1]
        label_string = flectional_label.strip('*')[0]
        label = Labels(label_string)
        forms = []
        for index in indexes:
            forms.append(str(self.get_form(index, label)))
        return str(label) + ":\n\t" + "\n\t".join(forms)

    def get_form(self, index, label):
        method_name = label.name.lower()
        if label in {Labels.NIEODMIENNY, Labels.TEKST, Labels.SKROT}:
            return ""
        method = getattr(self, method_name, lambda: "Invalid label")
        result = method(index)
        return str(result)


class Rzeczownik(Enum):
    F1 = "Liczba pojedyncza, Mianownik"
    F2 = "Liczba pojedyncza, Dopełniacz"
    F3 = "Liczba pojedyncza, Celownik"
    F4 = "Liczba pojedyncza, Biernik"
    F5 = "Liczba pojedyncza, Narzędnik"
    F6 = "Liczba pojedyncza, Miejscownik"
    F7 = "Liczba pojedyncza, Wołacz"
    F8 = "Liczba mnoga, Mianownik"
    F9 = "Liczba mnoga, Dopełniacz"
    F10 = "Liczba mnoga, Celownik"
    F11 = "Liczba mnoga, Biernik"
    F12 = "Liczba mnoga, Narzędnik"
    F13 = "Liczba mnoga, Miejscownik"
    F14 = "Liczba mnoga, Wołacz"


class Czasownik(Enum):
    F1 = "Bezokolicznik"
    F2 = "Czas teraźniejszy, 1 osoba liczby pojedynczej"
    F3 = "Czas teraźniejszy, 2 osoba liczby pojedynczej"
    F4 = "Czas teraźniejszy, 3 osoba liczby pojedynczej"
    F5 = "Czas teraźniejszy, 1 osoba liczby mnogiej"
    F6 = "Czas teraźniejszy, 2 osoba liczby mnogiej"
    F7 = "Czas teraźniejszy, 3 osoba liczby mnogiej"
    F8 = "Tryb rozkazujący, 1 osoba liczby pojedynczej"
    F9 = "brak"
    F10 = "Tryb rozkazujący, 1 osoba liczby mnogiej"
    F11 = "Tryb rozkazujący, 2 osoba liczby mnogiej"
    F12 = "brak"
    F13 = "Imiesłów przysłówkowy współczesny"
    F14 = "Imiesłów przysłowkowy czynny"
    F15 = "Czas przeszły, 1 osoba liczby pojedynczej, rodzaj męski"
    F16 = "Czas przeszły, 2 osoba liczby pojedynczej, rodzaj męski"
    F17 = "Czas przeszły, 3 osoba liczby pojedynczej, rodzaj męski"
    F18 = "Czas przeszły, 1 osoba liczby pojedynczej, rodzaj żeński"
    F19 = "Czas przeszły, 2 osoba liczby pojedynczej, rodzaj żeński"
    F20 = "Czas przeszły, 3 osoba liczby pojedynczej, rodzaj żeński"
    F21 = "Czas przeszły, 1 osoba liczby pojedynczej, rodzaj nijaki"
    F22 = "Czas przeszły, 2 osoba liczby pojedynczej, rodzaj nijaki"
    F23 = "Czas przeszły, 3 osoba liczby pojedynczej, rodzaj nijaki"
    F24 = "Czas przeszły, 1 osoba liczby mnogiej, rodzaj męskoosobowy"
    F25 = "Czas przeszły, 2 osoba liczby mnogiej, rodzaj męskoosobowy"
    F26 = "Czas przeszły, 3 osoba liczby mnogiej, rodzaj męskoosobowy"
    F27 = "Czas przeszły, 1 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    F28 = "Czas przeszły, 2 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    F29 = "Czas przeszły, 3 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    F30 = "Tryb przypuszczający, 1 osoba liczby pojedynczej, rodzaj męski"
    F31 = "Tryb przypuszczający, 2 osoba liczby pojedynczej, rodzaj męski"
    F32 = "Tryb przypuszczający, 3 osoba liczby pojedynczej, rodzaj męski"
    F33 = "Tryb przypuszczający, 1 osoba liczby pojedynczej, rodzaj żeński"
    F34 = "Tryb przypuszczający, 2 osoba liczby pojedynczej, rodzaj żeński"
    F35 = "Tryb przypuszczający, 3 osoba liczby pojedynczej, rodzaj żeński"
    F36 = "Tryb przypuszczający, 1 osoba liczby pojedynczej, rodzaj nijaki"
    F37 = "Tryb przypuszczający, 2 osoba liczby pojedynczej, rodzaj nijaki"
    F38 = "Tryb przypuszczający, 3 osoba liczby pojedynczej, rodzaj nijaki"
    F39 = "Tryb przypuszczający, 1 osoba liczby mnogiej, rodzaj męskoosobowy"
    F40 = "Tryb przypuszczający, 2 osoba liczby mnogiej, rodzaj męskoosobowy"
    F41 = "Tryb przypuszczający, 3 osoba liczby mnogiej, rodzaj męskoosobowy"
    F42 = "Tryb przypuszczający, 1 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    F43 = "Tryb przypuszczający, 2 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    F44 = "Tryb przypuszczający, 3 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    F45 = "Bezosobnik w czasie przeszłym"
    F46 = "Imiesłów przymiotnikowy bierny"
    F47 = "Imiesłów przysłówkowy uprzedni"


class Przymiotnik(Enum):
    F1 = "Liczba pojedyncza, Mianownik, rodzaj męski osobowy i męski żywotny"
    F2 = "Liczba pojedyncza, Dopełniacz, rodzaj męski osobowy i męski żywotny"
    F3 = "Liczba pojedyncza, Celownik, rodzaj męski osobowy i męski żywotny"
    F4 = "Liczba pojedyncza, Biernik, rodzaj męski osobowy i męski żywotny"
    F5 = "Liczba pojedyncza, Narzędnik, rodzaj męski osobowy i męski żywotny"
    F6 = "Liczba pojedyncza, Miejscownik, rodzaj męski osobowy i męski żywotny"
    F7 = "Liczba pojedyncza, Wołacz, rodzaj męski osobowy i męski żywotny"
    F8 = "Liczba pojedyncza, Mianownik, rodzaj męski nieosobowy"
    F9 = "Liczba pojedyncza, Dopełniacz, rodzaj męski nieosobowy"
    F10 = "Liczba pojedyncza, Celownik, rodzaj męski nieosobowy"
    F11 = "Liczba pojedyncza, Biernik, rodzaj męski nieosobowy"
    F12 = "Liczba pojedyncza, Narzędnik, rodzaj męski nieosobowy"
    F13 = "Liczba pojedyncza, Miejscownik, rodzaj męski nieosobowy"
    F14 = "Liczba pojedyncza, Wołacz, rodzaj męski nieosobowy"
    F15 = "Liczba pojedyncza, Mianownik, rodzaj żeński"
    F16 = "Liczba pojedyncza, Dopełniacz, rodzaj żeński"
    F17 = "Liczba pojedyncza, Celownik, rodzaj żeński"
    F18 = "Liczba pojedyncza, Biernik, rodzaj żeński"
    F19 = "Liczba pojedyncza, Narzędnik, rodzaj żeński"
    F20 = "Liczba pojedyncza, Miejscownik, rodzaj żeński"
    F21 = "Liczba pojedyncza, Wołacz, rodzaj żeński"
    F22 = "Liczba pojedyncza, Mianownik, rodzaj nijaki"
    F23 = "Liczba pojedyncza, Dopełniacz, rodzaj nijaki"
    F24 = "Liczba pojedyncza, Celownik, rodzaj nijaki"
    F25 = "Liczba pojedyncza, Biernik, rodzaj nijaki"
    F26 = "Liczba pojedyncza, Narzędnik, rodzaj nijaki"
    F27 = "Liczba pojedyncza, Miejscownik, rodzaj nijaki"
    F28 = "Liczba pojedyncza, Wołacz, rodzaj nijaki"
    F29 = "Liczba mnoga, Mianownik, rodzaj męskoosobowy"
    F30 = "Liczba mnoga, Dopełniacz, rodzaj męskoosobowy"
    F31 = "Liczba mnoga, Celownik, rodzaj męskoosobowy"
    F32 = "Liczba mnoga, Biernik, rodzaj męskoosobowy"
    F33 = "Liczba mnoga, Narzędnik, rodzaj męskoosobowy"
    F34 = "Liczba mnoga, Miejscownik, rodzaj męskoosobowy"
    F35 = "Liczba mnoga, Wołacz, rodzaj męskoosobowy"
    F36 = "Liczba mnoga, Mianownik, rodzaj niemęskoosobowy"
    F37 = "Liczba mnoga, Dopełniacz, rodzaj niemęskoosobowy"
    F38 = "Liczba mnoga, Celownik, rodzaj niemęskoosobowy"
    F39 = "Liczba mnoga, Biernik, rodzaj niemęskoosobowy"
    F40 = "Liczba mnoga, Narzędnik, rodzaj niemęskoosobowy"
    F41 = "Liczba mnoga, Miejscownik, rodzaj niemęskoosobowy"
    F42 = "Liczba mnoga, Wołacz, rodzaj niemęskoosobowy"
    F43 = "brak"
    F44 = "brak"


class Liczebnik(Enum):
    F1 = "Liczba pojedyncza, Mianownik, rodzaj męski osobowy"
    F2 = "Liczba pojedyncza, Dopełniacz, rodzaj męski osobowy"
    F3 = "Liczba pojedyncza, Celownik, rodzaj męski osobowy"
    F4 = "Liczba pojedyncza, Biernik, rodzaj męski osobowy"
    F5 = "Liczba pojedyncza, Narzędnik, rodzaj męski osobowy"
    F6 = "Liczba pojedyncza, Miejscownik, rodzaj męski osobowy"
    F7 = "Liczba pojedyncza, Wołacz, rodzaj męski osobowy"
    F8 = "Liczba pojedyncza, Mianownik, rodzaj męski żywotny"
    F9 = "Liczba pojedyncza, Dopełniacz, rodzaj męski żywotny"
    F10 = "Liczba pojedyncza, Celownik, rodzaj męski żywotny"
    F11 = "Liczba pojedyncza, Biernik, rodzaj męski żywotny"
    F12 = "Liczba pojedyncza, Narzędnik, rodzaj męski żywotny"
    F13 = "Liczba pojedyncza, Miejscownik, rodzaj męski żywotny"
    F14 = "Liczba pojedyncza, Wołacz, rodzaj męski żywotny"
    F15 = "Liczba pojedyncza, Mianownik, rodzaj męski nieosobowy"
    F16 = "Liczba pojedyncza, Dopełniacz, rodzaj męski nieosobowy"
    F17 = "Liczba pojedyncza, Celownik, rodzaj męski nieosobowy"
    F18 = "Liczba pojedyncza, Biernik, rodzaj męski nieosobowy"
    F19 = "Liczba pojedyncza, Narzędnik, rodzaj męski nieosobowy"
    F20 = "Liczba pojedyncza, Miejscownik, rodzaj męski nieosobowy"
    F21 = "Liczba pojedyncza, Wołacz, rodzaj męski nieosobowy"
    F22 = "Liczba pojedyncza, Mianownik, rodzaj żeński"
    F23 = "Liczba pojedyncza, Dopełniacz, rodzaj żeński"
    F24 = "Liczba pojedyncza, Celownik, rodzaj żeński"
    F25 = "Liczba pojedyncza, Biernik, rodzaj żeński"
    F26 = "Liczba pojedyncza, Narzędnik, rodzaj żeński"
    F27 = "Liczba pojedyncza, Miejscownik, rodzaj żeński"
    F28 = "Liczba pojedyncza, Wołacz, rodzaj żeński"
    F29 = "Liczba pojedyncza, Mianownik, rodzaj nijaki"
    F30 = "Liczba pojedyncza, Dopełniacz, rodzaj nijaki"
    F31 = "Liczba pojedyncza, Celownik, rodzaj nijaki"
    F32 = "Liczba pojedyncza, Biernik, rodzaj nijaki"
    F33 = "Liczba pojedyncza, Narzędnik, rodzaj nijaki"
    F34 = "Liczba pojedyncza, Miejscownik, rodzaj nijaki"
    F35 = "Liczba pojedyncza, Wołacz, rodzaj nijaki"
    F36 = "Liczba mnoga, Mianownik, rodzaj męskoosobowy"
    F37 = "Liczba mnoga, Dopełniacz, rodzaj męskoosobowy"
    F38 = "Liczba mnoga, Celownik, rodzaj męskoosobowy"
    F39 = "Liczba mnoga, Biernik, rodzaj męskoosobowy"
    F40 = "Liczba mnoga, Narzędnik, rodzaj męskoosobowy"
    F41 = "Liczba mnoga, Miejscownik, rodzaj męskoosobowy"
    F42 = "Liczba mnoga, Wołacz, rodzaj męskoosobowy"
    F43 = "Liczba mnoga, Mianownik, rodzaj niemęskoosobowy"
    F44 = "Liczba mnoga, Dopełniacz, rodzaj niemęskoosobowy"
    F45 = "Liczba mnoga, Celownik, rodzaj niemęskoosobowy"
    F46 = "Liczba mnoga, Biernik, rodzaj niemęskoosobowy"
    F47 = "Liczba mnoga, Narzędnik, rodzaj niemęskoosobowy"
    F48 = "Liczba mnoga, Miejscownik, rodzaj niemęskoosobowy"
    F49 = "Liczba mnoga, Wołacz, rodzaj niemęskoosobowy"


class Zaimek(Enum):
    F1 = "Liczba pojedyncza, Mianownik"
    F2 = "Liczba pojedyncza, Dopełniacz"
    F3 = "Liczba pojedyncza, Celownik"
    F4 = "Liczba pojedyncza, Biernik"
    F5 = "Liczba pojedyncza, Narzędnik"
    F6 = "Liczba pojedyncza, Miejscownik"
    F7 = "Liczba pojedyncza, Wołacz"
    F8 = "Liczba mnoga, Mianownik"
    F9 = "Liczba mnoga, Dopełniacz"
    F10 = "Liczba mnoga, Celownik"
    F11 = "Liczba mnoga, Biernik"
    F12 = "Liczba mnoga, Narzędnik"
    F13 = "Liczba mnoga, Miejscownik"
    F14 = "Liczba mnoga, Wołacz"


class Przyslowek(Enum):
    F1 = "Stopień równy"
    F2 = "Stopień wyższy"
    F3 = "Stopień najwyższy"