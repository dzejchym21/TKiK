class Skaner:
    def __init__(self, wyrazenie):
        self.wyrazenie = wyrazenie
        self.ptr = 0

    def pomin_biale_znaki(self):
        while self.ptr < len(self.wyrazenie) and self.wyrazenie[self.ptr].isspace():
            self.ptr += 1

    def skanuj_liczbe(self, start_pos):
        liczba = ''
        while self.ptr < len(self.wyrazenie) and self.wyrazenie[self.ptr].isdigit():
            liczba += self.wyrazenie[self.ptr]
            self.ptr += 1

        return "INT", liczba, start_pos

    def skanuj_identyfikator(self, start_pos):
        id = ''

        id += self.wyrazenie[start_pos]
        self.ptr += 1

        while self.ptr < len(self.wyrazenie):
            znak = self.wyrazenie[self.ptr]

            if znak.isdigit() or znak.isalpha():
                id += znak
                self.ptr += 1

            else:
                break

        return "ID", id, start_pos

    def pobierz_nastepny_token(self):
        self.pomin_biale_znaki()

        if self.ptr >= len(self.wyrazenie):
            return "EOF", "Koniec", self.ptr

        start_pos = self.ptr
        znak = self.wyrazenie[self.ptr]

        if znak.isdigit():
            return self.skanuj_liczbe(start_pos)
        elif znak.isalpha():
            return self.skanuj_identyfikator(start_pos)

        self.ptr += 1

        if znak == '+': return "PLUS", "+", start_pos
        if znak == '-': return "MINUS", "-", start_pos
        if znak == '(': return "LPAREN", "(", start_pos
        if znak == ')': return "RPAREN", ")", start_pos
        if znak == '/': return "DIV", "/", start_pos
        if znak == '*': return "MUL", "*", start_pos

        return "ERROR", znak, start_pos

tekst = " 2+3*(76+8/3)+ 3*(9-3)"
skaner = Skaner(tekst)

print(f'Skanowanie {tekst}: \n')
while True:
    kod, wartosc, kolumna = skaner.pobierz_nastepny_token()

    if kod == 'EOF':
        break

    if kod == 'ERROR':
        print(f'Blad w kolumnie: {kolumna}, nieoczekiwany znak: {wartosc}')
    else:
        print(f'({kod}, {wartosc}, {kolumna})')