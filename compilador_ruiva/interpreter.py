class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
    
    def execute(self, ast):
        for node in ast:
            if node[0] == 'DECLARE':
                self.handle_declaration(node)
            elif node[0] == 'PRINT':
                self.handle_print(node)
            # Adicione outros comandos aqui
    
    def handle_declaration(self, node):
        var_name = node[2]
        if len(node) == 4:  # Com valor
            value = self.evaluate_expression(node[3])
            self.variables[var_name] = value
    
    def handle_print(self, node):
        message = node[1].strip('"')
        print(message)
    
    def evaluate_expression(self, expr):
        # Implemente avaliação de expressões matemáticas aqui
        return expr  # Versão simplificada