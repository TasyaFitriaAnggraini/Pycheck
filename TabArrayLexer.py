from sly import Lexer

class TabArrayLexer(Lexer):
    tokens = {IDENTIFIER, INTEGER, ARRAY, OF, RECORD, END}

    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    INTEGER = r'\d+'

    ignore = ' \t\n'

    @_(r'\[')
    def lbracket(self, t):
        t.type = 'LBRACKET'
        return t

    @_(r'\]')
    def rbracket(self, t):
        t.type = 'RBRACKET'
        return t

    def error(self, t):
        print(f"Invalid character: {t.value[0]}")
        self.index += 1

if __name__ == "__main__":
    lexer = TabArrayLexer()
    code = '''
    array[1..tabmax] of
    record
    lastvar, lastpar, parsize, varsize: integer;
    end;
    '''
    for token in lexer.tokenize(code):
        print(token)


