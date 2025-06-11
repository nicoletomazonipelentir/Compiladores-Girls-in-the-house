import re

tokens = [
    'TYPE', 'IDENTIFIER', 'NUMBER', 'STRING', 'OPERATOR',
    'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE', 'CLOSE_BRACE',
    'SEMICOLON', 'COMMA', 'ASSIGN', 'KEYWORD'
]

reserved = {
    'Duny': 'CHAR',
    'Shaft': 'SHORT',
    'Alex': 'INT',
    'Todd': 'LONG',
    'KENDRA FOXTI': 'FOR',
    'DOMENICA': 'CONTINUE',
    'EU TENHO MAIS O QUE FAZER': 'BREAK',
    'DISK DUNNY': 'PRINT',
    'OLHA SO AQUI': 'INPUT',
    'RETORNA ESSA MERDA': 'RETURN'
}

def lexer(code):
    token_specs = [
        ('COMMENT', r'//.*'),
        ('STRING', r'\".*?\"'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('ASSIGN', r'='),
        ('OPERATOR', r'[+\-*/%<>!]=?'),
        ('OPEN_PAREN', r'\('),
        ('CLOSE_PAREN', r'\)'),
        ('OPEN_BRACE', r'\{'),
        ('CLOSE_BRACE', r'\}'),
        ('SEMICOLON', r';'),
        ('COMMA', r','),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('WHITESPACE', r'\s+'),
    ]
    
    tokens = []
    pos = 0
    
    while pos < len(code):
        match = None
        for token_type, pattern in token_specs:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE' and token_type != 'COMMENT':
                    if value in reserved:
                        tokens.append((reserved[value], value))
                    else:
                        tokens.append((token_type, value))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f'Caractere inesperado: {code[pos]} na posição {pos}')
    
    return tokens