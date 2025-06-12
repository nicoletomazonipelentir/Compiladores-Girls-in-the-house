import re

class TiaRuivaCompiler:
    def __init__(self):
        # Mapeamento de tipos
        self.type_map = {
            'Duny': str,    # char
            'Shaft': int,   # short
            'Alex': int,     # int
            'Todd': int,     # long
            'Honey': float, # float
            'Priscilao': float, # double
            'Julie': int     # unsigned
        }
        
        # Variáveis declaradas
        self.variables = {}
        
        # Funções definidas
        self.functions = {}
        
        # Pilha de contexto (para if/else/while)
        self.context_stack = []
        
        # Saída do programa
        self.output = []

    def compile_and_run(self, code):
        lines = code.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith('//'):
                i += 1
                continue
                
            try:
                # Processar declaração de função
                if 'PENSÃO DA TIA RUIVA RECEBE' in line:
                    i = self.process_function_declaration(lines, i)
                    
                # Processar declaração de variáveis
                elif any(type_word in line for type_word in self.type_map):
                    self.process_variable_declaration(line)
                    
                # Processar prints
                elif line.startswith('DISK DUNNY'):
                    self.process_print(line)
                    
                # Processar if/else if/else
                elif line.startswith('A Katia já foi uma grande mulher') or \
                     line.startswith('Caralhetee') or \
                     line.startswith('Ja fui uma grande mulher'):
                    i = self.process_conditional(lines, i)
                    
                # Processar while
                elif line.startswith('Anteriormente nessa porra'):
                    i = self.process_while(lines, i)
                    
                # Processar for
                elif line.startswith('KENDRA FOXTI'):
                    i = self.process_for(lines, i)
                    
                # Processar chamada de função
                elif 'PENSÃO DA TIA RUIVA ENTREGA' in line:
                    self.process_function_call(line)
                    
                # Processar retorno de função
                elif line.startswith('RETORNA ESSA MERDA'):
                    return self.process_return(line)
                    
                # Processar continue/break
                elif line == 'DOMENICA;':  # continue
                    return 'continue'
                elif line == 'EU TENHO MAIS O QUE FAZER;':  # break
                    return 'break'
                    
                # Processar incremento/decremento
                elif '++' in line or '--' in line:
                    self.process_increment_decrement(line)
                    
                # Processar uuuuh (ignorar)
                elif line == 'uuuuh':
                    pass
                    
                # Processar atribuição simples
                elif '=' in line and not any(kw in line for kw in ['if', 'while', 'for']):
                    self.process_assignment(line)
                    
                i += 1
            except Exception as e:
                raise RuntimeError(f"Erro na linha {i+1}: {str(e)}")
        
        return None

    def process_variable_declaration(self, line):
        # Exemplo: Alex X = 5;
        parts = re.match(r'(\w+)\s+(\w+)\s*=\s*(.*?);', line)
        if not parts:
            raise SyntaxError(f"Declaração de variável inválida: {line}")
            
        var_type = parts.group(1)
        var_name = parts.group(2)
        var_value = self.evaluate_expression(parts.group(3))
        
        if var_type in self.type_map:
            self.variables[var_name] = self.type_map[var_type](var_value)

    def process_print(self, line):
        # Exemplo: DISK DUNNY("Hello"); ou DISK DUNNY(var);
        match = re.match(r'DISK DUNNY\((.*?)\);', line)
        if not match:
            raise SyntaxError(f"Comando print inválido: {line}")
            
        content = match.group(1)
        
        # Se estiver entre aspas, é string literal
        if content.startswith('"') and content.endswith('"'):
            self.output.append(content[1:-1])
        else:
            # É uma variável ou expressão
            value = self.evaluate_expression(content)
            self.output.append(str(value))

    def process_function_declaration(self, lines, start_idx):
        # Exemplo: PENSÃO DA TIA RUIVA RECEBE FAT(Alex n)
        decl_line = lines[start_idx]
        match = re.match(r'PENSÃO DA TIA RUIVA RECEBE (\w+)\(([^)]*)\)', decl_line)
        if not match:
            raise SyntaxError(f"Declaração de função inválida: {decl_line}")
            
        func_name = match.group(1)
        params = [p.strip() for p in match.group(2).split(',') if p.strip()]
        
        # Processar parâmetros (tipo e nome)
        param_list = []
        for p in params:
            type_name = p.split()
            if len(type_name) != 2:
                raise SyntaxError(f"Parâmetro de função inválido: {p}")
            param_list.append(type_name[1])
        
        # Encontrar o corpo da função
        body = []
        i = start_idx + 1
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            body.append(lines[i])
            i += 1
        
        # Armazenar a função
        self.functions[func_name] = {
            'params': param_list,
            'body': body
        }
        
        return i  # Retorna o índice da linha após a função

    def process_function_call(self, line):
        # Exemplo: Alex res = PENSÃO DA TIA RUIVA ENTREGA FAT(num);
        match = re.match(r'(\w+\s+\w+\s*=\s*)?PENSÃO DA TIA RUIVA ENTREGA (\w+)\(([^)]*)\);', line)
        if not match:
            raise SyntaxError(f"Chamada de função inválida: {line}")
            
        func_name = match.group(2)
        args = [self.evaluate_expression(a.strip()) for a in match.group(3).split(',') if a.strip()]
        
        if func_name not in self.functions:
            raise NameError(f"Função não definida: {func_name}")
            
        func = self.functions[func_name]
        
        if len(args) != len(func['params']):
            raise TypeError(f"Número incorreto de argumentos para {func_name}")
        
        # Salvar variáveis atuais
        old_vars = self.variables.copy()
        
        # Criar variáveis locais para os parâmetros
        for param, arg in zip(func['params'], args):
            self.variables[param] = arg
        
        # Executar o corpo da função
        result = None
        body_code = '\n'.join(func['body'])
        self.compile_and_run(body_code)
        
        # Restaurar variáveis
        self.variables = old_vars
        
        # Se a atribuição foi especificada, armazenar o resultado
        if match.group(1):
            var_decl = match.group(1).strip()
            if '=' in var_decl:
                var_name = var_decl.split('=')[0].strip().split()[-1]
                self.variables[var_name] = result
        
        return result

    def process_conditional(self, lines, start_idx):
        # Processa if/else if/else
        current_line = lines[start_idx]
        
        # Determinar o tipo de condicional
        if current_line.startswith('A Katia já foi uma grande mulher'):
            cond_type = 'if'
            condition = re.match(r'A Katia já foi uma grande mulher \((.*)\)', current_line).group(1)
        elif current_line.startswith('Caralhetee'):
            cond_type = 'else if'
            condition = re.match(r'Caralhetee \((.*)\)', current_line).group(1)
        else:  # Ja fui uma grande mulher
            cond_type = 'else'
            condition = None
        
        # Avaliar a condição (se houver)
        cond_result = None
        if condition:
            cond_result = self.evaluate_expression(condition)
        
        # Encontrar o bloco de código
        block = []
        i = start_idx + 1
        while i < len(lines) and not any(lines[i].strip().startswith(s) for s in ['A Katia', 'Caralhetee', 'Ja fui']) and lines[i].strip() != 'uuuuh':
            block.append(lines[i])
            i += 1
        
        # Executar se a condição for verdadeira
        if cond_type == 'if' and cond_result:
            self.compile_and_run('\n'.join(block))
            # Pular qualquer else/else if relacionado
            while i < len(lines) and (lines[i].strip().startswith('Caralhetee') or lines[i].strip().startswith('Ja fui')):
                i += 1
                # Pular o bloco
                while i < len(lines) and lines[i].strip() != 'uuuuh':
                    i += 1
        elif cond_type == 'else if' and cond_result and not self.context_stack[-1].get('executed', False):
            self.compile_and_run('\n'.join(block))
            self.context_stack[-1]['executed'] = True
        elif cond_type == 'else' and not self.context_stack[-1].get('executed', False):
            self.compile_and_run('\n'.join(block))
        
        return i

    def process_while(self, lines, start_idx):
        # Exemplo: Anteriormente nessa porra (X > 2)
        current_line = lines[start_idx]
        condition = re.match(r'Anteriormente nessa porra \((.*)\)', current_line).group(1)
        
        # Encontrar o bloco de código
        block = []
        i = start_idx + 1
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            block.append(lines[i])
            i += 1
        
        # Executar o loop while
        while self.evaluate_expression(condition):
            result = self.compile_and_run('\n'.join(block))
            if result == 'break':
                break
            if result == 'continue':
                continue
        
        return i

    def process_for(self, lines, start_idx):
        # Exemplo: KENDRA FOXTI (i = 1; i <= n; i++)
        current_line = lines[start_idx]
        match = re.match(r'KENDRA FOXTI\s*\(([^;]+);([^;]+);([^)]+)\)', current_line)
        if not match:
            raise SyntaxError(f"Sintaxe de for inválida: {current_line}")
        
        init = match.group(1).strip()
        condition = match.group(2).strip()
        increment = match.group(3).strip()
        
        # Executar a inicialização
        self.process_assignment(init)
        
        # Encontrar o bloco de código
        block = []
        i = start_idx + 1
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            block.append(lines[i])
            i += 1
        
        # Executar o loop for
        while self.evaluate_expression(condition):
            result = self.compile_and_run('\n'.join(block))
            if result == 'break':
                break
            if result == 'continue':
                self.process_assignment(increment)
                continue
            
            # Executar o incremento
            self.process_assignment(increment)
        
        return i

    def process_assignment(self, line):
        # Exemplo: X = 5; ou X--;
        if '=' in line:
            var, expr = line.split('=', 1)
            var = var.strip()
            value = self.evaluate_expression(expr)
            self.variables[var] = value
        elif '++' in line:
            var = line.split('++')[0].strip()
            self.variables[var] += 1
        elif '--' in line:
            var = line.split('--')[0].strip()
            self.variables[var] -= 1

    def process_return(self, line):
        # Exemplo: RETORNA ESSA MERDA 1;
        expr = re.match(r'RETORNA ESSA MERDA (.*?);', line).group(1)
        return self.evaluate_expression(expr)

    def evaluate_expression(self, expr):
        # Avalia uma expressão matemática ou variável
        try:
            # Tenta avaliar como expressão Python (com substituição de variáveis)
            for var in self.variables:
                expr = expr.replace(var, str(self.variables[var]))
            return eval(expr)
        except:
            # Se falhar, pode ser uma string ou variável não encontrada
            if expr in self.variables:
                return self.variables[expr]
            raise ValueError(f"Expressão inválida ou variável não definida: {expr}")

    def get_output(self):
        return '\n'.join(self.output)

def run_ruiva_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    
    compiler = TiaRuivaCompiler()
    compiler.compile_and_run(code)
    print(compiler.get_output())

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python tia_ruiva_compiler.py arquivo.ruiva")
        sys.exit(1)
    
    run_ruiva_file(sys.argv[1])