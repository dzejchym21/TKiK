import html


class Skaner:
    def __init__(self, wyrazenie):
        self.wyrazenie = wyrazenie
        self.ptr = 0

    def skanuj_liczbe(self, start_pos):
        liczba = ''
        while self.ptr < len(self.wyrazenie) and self.wyrazenie[self.ptr].isdigit():
            liczba += self.wyrazenie[self.ptr]
            self.ptr += 1
        return "INT", liczba

    def skanuj_identyfikator(self, start_pos):
        id_str = ''
        while self.ptr < len(self.wyrazenie) and (self.wyrazenie[self.ptr].isalnum()):
            id_str += self.wyrazenie[self.ptr]
            self.ptr += 1
        return "ID", id_str

    def skanuj_bialy_znak(self):
        znak = self.wyrazenie[self.ptr]
        self.ptr += 1
        return "SPACE", znak

    def pobierz_nastepny_token(self):
        if self.ptr >= len(self.wyrazenie):
            return "EOF", ""

        start_pos = self.ptr
        znak = self.wyrazenie[self.ptr]

        if znak.isspace():
            return self.skanuj_bialy_znak()

        if znak.isdigit():
            return self.skanuj_liczbe(start_pos)

        if znak.isalpha():
            return self.skanuj_identyfikator(start_pos)

        self.ptr += 1

        if znak == ':' and self.ptr < len(self.wyrazenie) and self.wyrazenie[self.ptr] == '=':
            self.ptr += 1
            return "ASSIGN", ":="

        if znak == '+': return "PLUS", "+"
        if znak == '-': return "MINUS", "-"
        if znak == '': return "MUL", ""
        if znak == '/': return "DIV", "/"
        if znak == '(': return "LPAREN", "("
        if znak == ')': return "RPAREN", ")"
        if znak == ';': return "SEMICOLON", ";"
        if znak == '.': return "DOT", "."

        return "ERROR", znak


def koloruj_kod(plik_wejsciowy, plik_wyjsciowy):
    kolory = {
        "INT": "#b5cea8",
        "ID": "#9cdcfe",
        "PLUS": "#d4d4d4",
        "MINUS": "#d4d4d4",
        "MUL": "#d4d4d4",
        "DIV": "#d4d4d4",
        "ASSIGN": "#c586c0",
        "LPAREN": "#ffd700",
        "RPAREN": "#ffd700",
        "SEMICOLON": "#d4d4d4",
        "DOT": "#d4d4d4",
        "ERROR": "#f44747",
        "SPACE": ""
    }

    try:
        with open(plik_wejsciowy, 'r', encoding='utf-8') as f:
            tekst = f.read()
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {plik_wejsciowy}")
        return

    skaner = Skaner(tekst)

    html_content = """
    <html>
    <head>
        <style>
            body { background-color: #1e1e1e; color: #d4d4d4; font-family: 'Consolas', monospace; padding: 20px; }
            .token { font-weight: bold; }
        </style>
    </head>
    <body><pre>"""

    while True:
        typ, wartosc = skaner.pobierz_nastepny_token()
        if typ == "EOF":
            break

        bezpieczna_wartosc = html.escape(wartosc)

        if typ == "SPACE":
            html_content += bezpieczna_wartosc
        else:
            kolor = kolory.get(typ, "#ffffff")
            html_content += f'<span style="color: {kolor}">{bezpieczna_wartosc}</span>'

    html_content += "</pre></body></html>"

    with open(plik_wyjsciowy, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Sukces! Pokolorowany kod zapisano w: {plik_wyjsciowy}")


# --- URUCHOMIENIE ---
# Przygotuj plik 'kod.txt' z dowolną treścią, np. "x := 5 + 10;"
# koloruj_kod('kod.txt', 'wynik.html')

# Test na szybko z tekstem w konsoli:
kod_testowy = "x := 2 + 3 * (76 + 8 / 3);\n y := x - 10."
with open("test.txt", "w") as f: f.write(kod_testowy)
koloruj_kod("test.txt", "indeks.html")