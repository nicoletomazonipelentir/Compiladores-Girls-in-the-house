import re

class RuivaInterpreter:
    def __init__(self):
        self.variables = {}
        self.type_map = {
            'Duny': str,
            'Shaft': int,
            'Alex': int,
            'Todd': int
        }
        self.loops = []

    def interpret(self, code):
        lines = self._preprocess(code)
        self._execute(lines)

    def _preprocess(self, code):
        processed = []
        for line in code.split('\n'):
            line = line.split('//')[0].strip()
            if line:
                processed.append(line)
        return processed

    def _execute(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i]
            try:
                if line.startswith('Anteriormente nessa porra'):
                    i = self._handle_while(lines, i)
                elif line.startswith('A Katia já foi uma grande mulher'):
                    i = self._handle_if(lines, i)
                # Continua executando as linhas após o if
                    continue
                elif line.startswith('DISK DUNNY'):
                    self._handle_print(line)
                elif any(line.startswith(t) for t in self.type_map):
                    self._handle_declaration(line)
                elif '=' in line:
                    self._handle_assignment(line)
                elif line == 'EU TENHO MAIS O QUE FAZER':
                    if self.loops:
                        return self.loops[-1]['break']
                elif line == 'uuuuh':
                    pass  # Ignora o fechamento de bloco
                i += 1
            except Exception as e:
                print(f"Erro na linha {i+1}: '{line}' - {str(e)}")
                i += 1

    def _handle_declaration(self, line):
        parts = line.split()
        var_type = parts[0]
        rest = ' '.join(parts[1:]).rstrip(';')
        
        if '=' in rest:
            var_name, expr = rest.split('=', 1)
            var_name = var_name.strip()
            expr = expr.strip()
            self.variables[var_name] = self.type_map[var_type](eval(expr, {}, self.variables))
        else:
            var_name = rest.rstrip(';')
            self.variables[var_name] = self.type_map[var_type]()

    def _handle_assignment(self, line):
        var_name, expr = line.split('=', 1)
        var_name = var_name.strip()
        expr = expr.strip().rstrip(';')
        if var_name in self.variables:
            self.variables[var_name] = eval(expr, {}, self.variables)
        else:
            raise NameError(f"Variável não declarada: {var_name}")

    def _handle_print(self, line):
        content = line[line.find('(')+1:line.find(')')]
        if content.startswith('"') and content.endswith('"'):
            print(content[1:-1])
        else:
            print(eval(content, {}, self.variables))

    def _handle_while(self, lines, start_idx):
        line = lines[start_idx]
        condition = line[line.find('(')+1:line.find(')')]
        
        block = []
        i = start_idx + 1
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            block.append(lines[i])
            i += 1
        
        self.loops.append({'break': i + 1})
        
        while eval(condition, {}, self.variables):
            self._execute(block)
        
        self.loops.pop()
        return i + 1

    def _handle_if(self, lines, start_idx):
        line = lines[start_idx]
        condition = line[line.find('(')+1:line.find(')')]
    
    # Encontra o bloco do if
        block = []
        i = start_idx + 1
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            block.append(lines[i])
            i += 1
    
    # Executa o bloco se a condição for verdadeira
        if eval(condition, {}, self.variables):
            self._execute(block)
    
    # Retorna o índice da linha após o 'uuuuh' para continuar a execução
        return i + 1