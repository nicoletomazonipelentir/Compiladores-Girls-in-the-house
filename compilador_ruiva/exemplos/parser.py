class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = None
        self.next_token()
    
    def next_token(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None
    
    def parse(self):
        statements = []
        while self.current_token:
            if self.current_token[0] in ['INT', 'CHAR', 'LONG', 'SHORT']:
                statements.append(self.parse_declaration())
            elif self.current_token[0] == 'FUNCTION_DECL':
                statements.append(self.parse_function())
            elif self.current_token[0] == 'FOR':
                statements.append(self.parse_for())
            elif self.current_token[0] == 'WHILE':
                statements.append(self.parse_while())
            elif self.current_token[1] == 'DISK DUNNY':
                statements.append(self.parse_print())
            elif self.current_token[0] == 'IF':
                statements.append(self.parse_if())
            else:
                self.next_token()
        return statements
   
   
    def parse_function(self):
        self.next_token()  # Pula 'PENSAO DA TIA RUIVA RECEBE'
        self.expect('OPEN_PAREN')
        
        # Parse dos parâmetros
        params = []
        while self.current_token and self.current_token[0] != 'CLOSE_PAREN':
            param_type = self.current_token[1]
            self.next_token()
            param_name = self.current_token[1]
            self.next_token()
            params.append((param_type, param_name))
            if self.current_token and self.current_token[0] == 'COMMA':
                self.next_token()
        
        self.expect('CLOSE_PAREN')
        func_name = self.current_token[1]
        self.next_token()
        
        # Parse do corpo da função
        body = self.parse_block()
        return ('FUNCTION', func_name, params, body)
    
    def parse_declaration(self):
        var_type = self.current_token[1]
        self.next_token()
        var_name = self.current_token[1]
        self.next_token()
        if self.current_token and self.current_token[0] == 'ASSIGN':
            self.next_token()
            value = self.current_token[1]
            self.next_token()
            return ('DECLARE', var_type, var_name, value)
        return ('DECLARE', var_type, var_name)
    
    def parse_for(self):
        self.next_token()  # Pula 'KENDRA FOXTI'
        self.expect('OPEN_PAREN')
        init = self.parse_declaration() if self.current_token[0] in ['INT', 'CHAR', 'LONG'] else None
        self.expect('SEMICOLON')
        condition = self.parse_expression()
        self.expect('SEMICOLON')
        increment = self.parse_expression()
        self.expect('CLOSE_PAREN')
        body = self.parse_block()
        return ('FOR', init, condition, increment, body)
    
    def parse_while(self):
        self.next_token()  # Pula 'Anteriormente nessa porra'
        self.expect('OPEN_PAREN')
        condition = self.parse_expression()
        self.expect('CLOSE_PAREN')
        body = self.parse_block()
        return ('WHILE', condition, body)
    
    def parse_if(self):
        self.next_token()  # Pula 'A Katia já foi uma grande mulher'
        self.expect('OPEN_PAREN')
        condition = self.parse_expression()
        self.expect('CLOSE_PAREN')
        then_branch = self.parse_block()
        else_branch = None
        if self.current_token and self.current_token[1] in ['Caralhetee', 'Ja fui uma grande mulher']:
            self.next_token()
            else_branch = self.parse_block()
        return ('IF', condition, then_branch, else_branch)
    
    def parse_print(self):
        self.next_token()  # Pula 'DISK DUNNY'
        self.expect('OPEN_PAREN')
        value = self.current_token[1]
        self.next_token()
        self.expect('CLOSE_PAREN')
        return ('PRINT', value)
    
    def parse_block(self):
        statements = []
        while self.current_token and self.current_token[1] != 'uuuuh':
            statements.append(self.parse())
        if self.current_token and self.current_token[1] == 'uuuuh':
            self.next_token()
        return statements
    
    def parse_expression(self):
        # Implementação simplificada - na prática seria mais complexa
        left = self.current_token[1]
        self.next_token()
        if self.current_token and self.current_token[0] == 'OPERATOR':
            op = self.current_token[1]
            self.next_token()
            right = self.current_token[1]
            self.next_token()
            return ('BINOP', op, left, right)
        return left
    
    def expect(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.next_token()
        else:
            raise SyntaxError(f"Esperado {token_type}, encontrado {self.current_token}")