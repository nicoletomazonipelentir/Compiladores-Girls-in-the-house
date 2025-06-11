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
            if self.current_token[0] in ['INT', 'CHAR', 'LONG']:
                statements.append(self.parse_declaration())
            elif self.current_token[0] == 'FOR':
                statements.append(self.parse_for())
            elif self.current_token[1] == 'DISK DUNNY':
                statements.append(self.parse_print())
            else:
                self.next_token()
        return statements
    
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
        # Implementar lógica para parse do for
        pass
    
    def parse_print(self):
        self.next_token()  # Pula 'DISK DUNNY'
        # Implementar lógica para parse do print
        pass