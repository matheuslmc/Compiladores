from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = {
        NUMBER, PLUS, MINUS, TIMES, COMMA, SEMICOLON, LBRACKET, RBRACKET, LPAREN, RPAREN, TRANSP
    }

    ignore_newline = r'\n+'
    ignore = ' \t'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    COMMA = r','
    SEMICOLON = r';'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LPAREN = r'\('
    RPAREN = r'\)'
    TRANSP = r't'

    @_(r'-?\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES),
        ('right', TRANSP),
    )

    @_('M')
    def S(self, p):
        return p.M

    @_('S PLUS M',
       'S MINUS M')
    def S(self, p):
        if p[1] == '+':
            return [a + b for a, b in zip(p.S, p.M)]
        elif p[1] == '-':
            return [a - b for a, b in zip(p.S, p.M)]

    @_('matrix')
    def M(self, p):
        return p.matrix

    @_('M TIMES matrix')
    def M(self, p):
        m1 = [[0] * 3 for _ in range(3)]
        m2 = [[0] * 3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                m1[i][j] = p.M[i * 3 + j]
                m2[i][j] = p.matrix[i * 3 + j]

        result = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += m1[i][k] * m2[k][j]

        return [val for sublist in result for val in sublist]

    @_('TRANSP matrix')
    def matrix(self, p):
        return [p.matrix[i + j * 3] for i in range(3) for j in range(3)]

    @_('LPAREN S RPAREN')
    def matrix(self, p):
        return p.S

    @_('LBRACKET row SEMICOLON row SEMICOLON row RBRACKET')
    def matrix(self, p):
        return [p.row0, p.row1, p.row2]

    @_('NUMBER COMMA NUMBER COMMA NUMBER')
    def row(self, p):
        return [p.NUMBER0, p.NUMBER1, p.NUMBER2]

if __name__ == '__main__':
    data = input('Entre com sua Matriz: ')
    lexer = CalcLexer()
    parser = CalcParser()
    result = parser.parse(lexer.tokenize(data))
    print('--- RESULT ---')
    print(result)
