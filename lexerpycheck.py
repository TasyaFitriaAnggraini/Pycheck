from sly import Lexer


class lexerpycheck(Lexer):
    # Token yang akan digunakan
    tokens = {
        VAR,
        ANGKA,
        EQEQ,
        JIKA,
        CETAK,
        KECUALI,
        MAKA,
        LAKUKAN,
        UNTUK,
        LD,
        KD,
        LDSD,
        KDSD,
        TIDAKSAMA,
        MOD,
        FUNGSI,
        STRING,
        SAMPAI,
        TABARRAY,
        LBRACKET,
        RBRACKET,
    }

    literals = {"=", "+", "-", "/", "*", "{", "}", "(", ")", "[", "]", "."}

    # Baris yang akan diabaikan
    ignore = " \t"

    # Regular expression rules untuk tokens
    EQEQ = r"=="
    LDSD = r">="
    KDSD = r"<="
    LD = r">"
    KD = r"<"
    TIDAKSAMA = r"!="
    MOD = r"\%"


    @_(r"\d+")
    def ANGKA(self, t):
        t.value = int(t.value)
        return t

    # Special keywords
    # VAR['jika']     = JIKA
    # VAR['lain']     = LAIN
    # VAR['maka']     = MAKA
    # VAR['lakukan']  = LAKUKAN
    # VAR['untuk']    = UNTUK
    # VAR['func']     = FUNC
    # VAR['cetak']    = CETAK
    # VAR['hingga']   = HINGGA

    JIKA = r"jika"
    KECUALI = r"kecuali"
    MAKA = r"maka"
    LAKUKAN = r"lakukan"
    UNTUK = r"untuk"
    FUNGSI = r"fungsi"
    CETAK = r"cetak"
    SAMPAI = r"sampai"
    TABARRAY = r"tabarray"

    VAR = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STRING = r"\".*?\""

    # Abaikan komentar
    ignore_comment = r"\\.*"

    # Line numbers
    @_(r"\n+")
    def newline(self, t):
        self.lineno += t.value.count("\n")

    # Menghitung kolom
    def find_column(text, token):
        last_cr = text.rfind("\n", 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column

    def __init__(self):
        self.nesting_level = 0

    @_(r"\%")
    def mod(self, t):
        t.type = "%"
        return t

    @_(r"\{")
    def bracel(self, t):
        t.type = "{"
        self.nesting_level += 1
        return t

    @_(r"\}")
    def bracer(self, t):
        t.type = "}"
        self.nesting_level -= 1
        return t

    @_(r"\[")
    def lbracket(self, t):
        t.type = "]"
        self.nesting_level -= 1
        return t

    @_(r"\]")
    def rbracket(self, t):
        t.type = "]"
        self.nesting_level -= 1
        return t

    def error(self, t):
        if t.type == "LBRACKET":
            print(f"Baris {self.lineno}: Token '[' tidak valid")
        elif t.type == "RBRACKET":
            print(f"Baris {self.lineno}: Token ']' tidak valid")

        print("Baris %d: Karakter tidak ada %r" % (self.lineno, t.value[0]))
        self.index += 1


if __name__ == "__main__":
    lexer = lexerpycheck()
    env = {}
    while True:
        try:
            text = input("pyCheck > ")
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
