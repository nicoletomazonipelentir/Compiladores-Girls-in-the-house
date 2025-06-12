import re

class TiaRuivaCompiler:
    def __init__(self):
        self.variables = {}
        self.type_map = {
            'Duny': str,    # char
            'Shaft': int,   # short
            'Alex': int,    # int
            'Todd': int,    # long
            'Honey': float, # float
            'Priscilao': float, # double
            'Julie': int    # unsigned
        }
        self.FLOW_CONTINUE = "DOMENICA;"
        self.FLOW_BREAK = "EU TENHO MAIS O QUE FAZER;"
        self.flow_control = None
        self.global_vars = {}
        self.context_stack = [{'vars': {}, 'functions': {}}]
        self.output = []
    
    def reset(self):
        self.variables = {}
        
        # Variáveis globais
        self.global_vars = {}
        
        # Pilha de contexto para funções (armazena variáveis locais)
        self.context_stack = [{'vars': {}, 'functions': {}}]
        
        # Saída do programa
        self.output = []
        
        # Controle de fluxo
        self.flow_control = None

    def current_context(self):
        return self.context_stack[-1]

    def compile_and_run(self, code):
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('//')]

        if not lines:
            raise RuntimeError("Código vazio")

        # Verificar abertura e fechamento
        if lines[0] != 'Open the door and have fun':
            raise RuntimeError("O código deve começar com 'Open the door and have fun'")
        if lines[-1] != 'uuuuh':
            raise RuntimeError("O código deve terminar com 'uuuuh'")

        # Remover a primeira e última linhas
        lines = lines[1:-1]

        i = 0
        while i < len(lines):
            line = lines[i]
            try:
                if line.startswith('KENDRA FOXTI'):
                    i = self.process_for_loop(lines, i)
                elif line.startswith('Anteriormente nessa porra'):
                    i = self.process_while(lines, i)
                else:
                    self.execute_line(line)
                    i += 1
            except Exception as e:
                raise RuntimeError(f"Erro na linha {i+2}: {line}\n{str(e)}")

    def get_block(self, lines, start_idx):
        block = []
        i = start_idx
        while i < len(lines):
            if lines[i].strip() == 'uuuuh':
                return block, i
            block.append(lines[i])
            i += 1
        raise RuntimeError("Bloco não terminado com 'uuuuh'")
    
    
    def execute_block(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Detecta if
            if line.startswith('A Katia já foi uma grande mulher'):
                print(f"Executando estrutura condicional a partir da linha {i}")
                i = self.process_if_else(lines, i)
                continue
            # Detecta prints
            elif line.startswith("DISK DUNNY"):
                self.process_print(line)
            # Detecta declaração de variáveis
            elif any(line.startswith(t + " ") for t in self.type_map):
                self.process_variable_declaration(line)
            # Detecta atribuição simples
            elif "=" in line:
                self.process_assignment(line)
            # Detecta while
            elif line.startswith("Anteriormente nessa porra"):
                i = self.process_while(lines, i)
                continue

            i += 1

    def execute_line(self, line):
        line = line.strip()
        
        # Verifica break/continue
        if line == self.FLOW_CONTINUE:
            self.flow_control = 'continue'
            return
        elif line == self.FLOW_BREAK:
            self.flow_control = 'break'
            return
        
        # Ignora linhas de fechamento de bloco
        if line == 'uuuuh':
            return

        # Trata incrementos/decrementos pós-fixados
        if re.match(r'^\w+\+\+;?$', line):
            var = line.replace('+', '').replace(';', '')
            self.execute_line(f"{var} = {var} + 1")
            return
        elif re.match(r'^\w+--;?$', line):
            var = line.replace('-', '').replace(';', '')
            self.execute_line(f"{var} = {var} - 1")
            return

        # 1. Declaração de variáveis
        if any(line.startswith(tipo + ' ') for tipo in self.type_map):
            self.process_variable_declaration(line)
            return
            
        # 2. Prints
        elif line.startswith('DISK DUNNY'):
            self.process_print(line)
            return
        # Adicione este caso para input
        elif line.startswith('OLHA SO AQUI'):
            self.process_input(line)
            return
        
        # 3. Atribuições
        elif '=' in line and not line.startswith(('A Katia', 'Anteriormente', 'Caralhetee', 'Ja fui')):
            self.process_assignment(line)
            return
            
        # 4. Condicionais
        elif line.startswith('A Katia já foi uma grande mulher'):
            self.process_conditional([line], 0)
            return
        elif line.startswith('Caralhetee'):
            return
        elif line.startswith('Ja fui uma grande mulher'):
            return
            
        # 5. Loops
        elif line.startswith('Anteriormente nessa porra'):
            self.process_while([line], 0)
            return
        elif line.startswith('KENDRA FOXTI'):
            self.process_for_loop([line], 0)
            return
            
        # 6. Controle de fluxo
        elif line == 'DOMENICA;':
            self.flow_control = 'continue'
            return
        elif line == 'EU TENHO MAIS O QUE FAZER;':
            self.flow_control = 'break'
            return
            
        # 7. Funções
        elif line.startswith('PENSÃO DA TIA RUIVA RECEBE'):
            self.process_function_declaration(line)
            return
        elif 'PENSÃO DA TIA RUIVA ENTREGA' in line:
            self.process_function_call(line)
            return
        elif line.startswith('RETORNA ESSA MERDA'):
            self.process_return(line)
            return
            
        # 8. Linha vazia/comentário
        elif not line or line.startswith('//'):
            return
            
        # 9. Comando não reconhecido
        else:
            raise SyntaxError(f"Comando não reconhecido: {line}")

    def process_input(self, line):
        try:
            # Extrai o tipo e variável (ex: "Todd?("%d", &X)")
            parts = line.split('?', 1)
            var_type = parts[0].split()[-1]  # Pega "Todd"
            var_part = parts[1].split('&')[-1].rstrip(');').strip()  # Pega "X"
            
            # Simula a entrada do usuário
            user_input = input(f"Digite um valor para {var_part}: ")
            
            # Converte para o tipo correto
            if var_type in self.type_map:
                self.variables[var_part] = self.type_map[var_type](user_input)
            else:
                raise ValueError(f"Tipo desconhecido: {var_type}")
                
        except Exception as e:
            raise RuntimeError(f"Erro no input: {str(e)}")

    def get_value(self, var):
        var = var.strip()
        if var in self.variables:
            return self.variables[var]
        try:
            return int(var)
        except ValueError:
            try:
                return float(var)
            except ValueError:
                raise Exception(f"Variável ou valor inválido: {var}")

    def process_for_loop(self, lines, start_idx):
        try:
            line = lines[start_idx]
            match = re.match(r'KENDRA FOXTI\s*\((.*?)\s*;\s*(.*?)\s*;\s*(.*?)\)', line)
            if not match:
                raise SyntaxError("Sintaxe inválida do for loop")
                
            init, condition, increment = match.groups()
            
            # Executa inicialização
            self.execute_line(init)
            
            # Se a variável da condição não existe, inicialize com zero
            var_cond = condition.split()[0]
            if var_cond not in self.variables:
                self.variables[var_cond] = 0
            
            block, end_idx = self.get_block(lines, start_idx + 1)
            
            while True:
                # Avalia a condição
                if not self.evaluate_expression(condition):
                    break
                
                # Executa o bloco do loop
                self.execute_block(block)
                
                # Executa o incremento
                inc_line = increment.strip()
                if inc_line.endswith('++'):
                    var = inc_line[:-2]
                    self.variables[var] += 1
                elif inc_line.endswith('--'):
                    var = inc_line[:-2]
                    self.variables[var] -= 1
                else:
                    self.execute_line(inc_line)
            
            while self.evaluate_expression(condition):
                for inner_line in block:
                    self.flow_control = None
                    self.execute_line(inner_line)
                    
                    if self.flow_control == 'break':
                        return end_idx + 1
                    elif self.flow_control == 'continue':
                        break
                
                if self.flow_control != 'continue':
                    self.execute_line(increment)
                
                self.flow_control = None
            
            return end_idx + 1
        except Exception as e:
            raise RuntimeError(f"Erro no for loop: {str(e)}")

    def process_if_else(self, lines, start_idx):
        i = start_idx
        blocks = []
        line = lines[i].strip()
        match_if = re.match(r'A Katia já foi uma grande mulher\s*\((.*)\)', line)
        if not match_if:
            raise SyntaxError(f"Condicional if inválida: {line}")
        cond = match_if.group(1)
        i += 1

        body = []
        while i < len(lines):
            l = lines[i].strip()
            if l in ('uuuuh', 'uuuuh;'):
                break
            if l.startswith('Caralhetee') or l.startswith('Ja fui uma grande mulher'):
                break
            body.append(lines[i])
            i += 1

        blocks.append(('if', cond, body))

        while i < len(lines):
            l = lines[i].strip()
            if l in ('uuuuh', 'uuuuh;'):
                break
            elif l.startswith('Caralhetee'):
                match_elif = re.match(r'Caralhetee\s*\((.*)\)', l)
                if not match_elif:
                    raise SyntaxError(f"Condicional elif inválida: {l}")
                cond_elif = match_elif.group(1)
                i += 1
                body = []
                while i < len(lines):
                    l2 = lines[i].strip()
                    if l2 in ('uuuuh', 'uuuuh;') or l2.startswith('Caralhetee') or l2.startswith('Ja fui uma grande mulher'):
                        break
                    body.append(lines[i])
                    i += 1
                blocks.append(('elif', cond_elif, body))
            elif l.startswith('Ja fui uma grande mulher'):
                i += 1
                body = []
                while i < len(lines):
                    l2 = lines[i].strip()
                    if l2 in ('uuuuh', 'uuuuh;'):
                        break
                    body.append(lines[i])
                    i += 1
                blocks.append(('else', None, body))
            else:
                break

        while i < len(lines) and lines[i].strip() not in ('uuuuh', 'uuuuh;'):
            i += 1
        i += 1

        for tipo, condicao, corpo in blocks:
            if tipo in ('if', 'elif'):
                val = self.evaluate_expression(condicao)
                if val:
                    self.execute_block(corpo)
                    break
            else:
                self.execute_block(corpo)
                break

        return i

    def process_conditional(self, lines, i):
        condition_line = lines[i]

        if "A Katia já foi uma grande mulher" in condition_line:
            condition = condition_line.split("(", 1)[1].rstrip(")")
            if self.evaluate_expression(condition):
                i += 1
                while i < len(lines) and not lines[i].startswith("Mas dizem que ela mudou") and not lines[i].startswith("Mentira dela"):
                    self.execute_line(lines[i])
                    i += 1
                while i < len(lines) and (lines[i].startswith("Mas dizem que ela mudou") or lines[i].startswith("Mentira dela")):
                    i += 1
                return i
            else:
                i += 1
                while i < len(lines) and not lines[i].startswith("Mas dizem que ela mudou") and not lines[i].startswith("Mentira dela"):
                    i += 1

                if i < len(lines) and lines[i].startswith("Mas dizem que ela mudou"):
                    condition = lines[i].split("(", 1)[1].rstrip(")")
                    if self.evaluate_expression(condition):
                        i += 1
                        while i < len(lines) and not lines[i].startswith("Mentira dela"):
                            self.execute_line(lines[i])
                            i += 1
                        return i
                    else:
                        while i < len(lines) and not lines[i].startswith("Mentira dela"):
                            i += 1

                if i < len(lines) and lines[i].startswith("Mentira dela"):
                    i += 1
                    while i < len(lines) and not lines[i].startswith("A Katia já foi uma grande mulher"):
                        self.execute_line(lines[i])
                        i += 1

        return i

    def skip_to_next_conditional(self, lines, start_idx):
        i = start_idx
        while i < len(lines):
            if lines[i].strip() in ('uuuuh', 'Caralhetee', 'Ja fui uma grande mulher'):
                return i
            i += 1
        return i
    
    def process_block(self, lines, start_idx):
        i = start_idx
        while i < len(lines):
            line = lines[i].strip()
            if line in ('uuuuh', 'Caralhetee', 'Ja fui uma grande mulher'):
                return i
            self.execute_line(line)
            i += 1
        return i

    def skip_block(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and not lines[i].strip() in ("uuuuh", "uuuuh;"):
            i += 1
        return i + 1
    
    def get_next_block(self):
        block = []
        while True:
            line = self.get_next_line()
            if line is None:
                raise SyntaxError("Bloco não terminado com 'uuuuh'")
            if line.strip() == 'uuuuh':
                break
            block.append(line)
        return block
    
    def get_next_line(self):
        if hasattr(self, 'current_line_index'):
            self.current_line_index += 1
            if self.current_line_index < len(self.lines):
                return self.lines[self.current_line_index]
        return None
    
    def process_assignment(self, line):
        parts = line.split('=', 1)
        var = parts[0].strip()
        value_expr = parts[1].strip().rstrip(';')
        
        value = self.evaluate_expression(value_expr)
        
        self.current_context()['vars'][var] = value

    def process_increment(self, line):
        if line.startswith("INCREMENTA"):
            var = line.split()[1]
            if var in self.variables:
                self.variables[var] += 1
            else:
                raise Exception(f"Variável '{var}' não definida para incremento")

    def process_while(self, lines, start_idx):
        try:
            line = lines[start_idx]
            condition = line[line.find('(')+1:line.rfind(')')].strip()
            
            # Pega o bloco do while
            block_lines = []
            i = start_idx + 1
            while i < len(lines) and lines[i].strip() != 'uuuuh':
                block_lines.append(lines[i])
                i += 1
            
            # Executa o loop
            while self.evaluate_expression(condition):
                for inner_line in block_lines:
                    self.flow_control = None
                    self.execute_line(inner_line)
                    
                    if self.flow_control == 'break':
                        return i + 1  # Sai do while
                    elif self.flow_control == 'continue':
                        break  # Pula para próxima iteração
                
                if self.flow_control == 'break':
                    break
            
            return i + 1
        except Exception as e:
            raise RuntimeError(f"Erro no while: {str(e)}")

    def process_variable_declaration(self, line):
        try:
            match = re.match(r'(\w+)\s+(\w+)\s*(?:=\s*(.*?)\s*)?;?$', line)
            if not match:
                raise SyntaxError(f"Declaração inválida: {line}")
            
            tipo, nome, valor = match.groups()
            
            if tipo not in self.type_map:
                raise SyntaxError(f"Tipo desconhecido: {tipo}")
            
            if valor is None or valor.strip() == '':
                valor_avaliado = 0 if self.type_map[tipo] == int else 0.0 if self.type_map[tipo] == float else ''
            else:
                valor = valor.rstrip(';').strip()
                valor_avaliado = self.evaluate_expression(valor)
            
            self.current_context()['vars'][nome] = self.type_map[tipo](valor_avaliado)
            
        except Exception as e:
            raise RuntimeError(f"Erro na declaração de variável '{nome}': {str(e)}")

    def process_print(self, line):
        try:
            match = re.match(r'DISK DUNNY\((.+)\);?', line)
            if not match:
                raise ValueError(f"Sintaxe inválida no print: {line}")
            
            content = match.group(1).strip()
            
            if content.startswith('"') and content.endswith('"'):
                print(content[1:-1])
            else:
                try:
                    value = self.evaluate_expression(content)
                    print(str(value))
                except Exception as e:
                    raise ValueError(f"Erro ao avaliar expressão '{content}': {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Erro no processamento do print: {str(e)}")

    def process_function_declaration(self, lines, start_idx):
        decl_line = lines[start_idx]
        match = re.match(r'PENSÃO DA TIA RUIVA RECEBE (\w+)\(([^)]*)\)', decl_line)
        if not match:
            raise SyntaxError(f"Declaração de função inválida: {decl_line}")
            
        func_name = match.group(1)
        params = [p.strip() for p in match.group(2).split(',') if p.strip()]
        
        param_list = []
        for p in params:
            type_name = p.split()
            if len(type_name) != 2:
                raise SyntaxError(f"Parâmetro de função inválido: {p}")
            param_list.append(type_name[1])
        
        body = []
        i = start_idx + 1
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            body.append(lines[i])
            i += 1
        
        self.current_context()['functions'][func_name] = {
            'params': param_list,
            'body': body
        }
        
        return i + 1

    def process_function_call(self, line):
        match = re.match(r'(\w+\s+\w+\s*=\s*)?PENSÃO DA TIA RUIVA ENTREGA (\w+)\(([^)]*)\);', line)
        if not match:
            raise SyntaxError(f"Chamada de função inválida: {line}")
            
        func_name = match.group(2)
        args = [self.evaluate_expression(a.strip()) for a in match.group(3).split(',') if a.strip()]
        
        func_def = None
        for context in reversed(self.context_stack):
            if func_name in context['functions']:
                func_def = context['functions'][func_name]
                break
        
        if not func_def:
            raise NameError(f"Função não definida: {func_name}")
            
        if len(args) != len(func_def['params']):
            raise TypeError(f"Número incorreto de argumentos para {func_name}")
        
        new_context = {
            'vars': dict(zip(func_def['params'], args)),
            'functions': {}
        }
        
        self.context_stack.append(new_context)
        
        result = None
        body_code = '\n'.join(func_def['body'])
        try:
            self.compile_and_run(body_code)
        except Exception as e:
            self.context_stack.pop()
            raise e
        
        if hasattr(self, 'last_return'):
            result = self.last_return
            delattr(self, 'last_return')
        
        self.context_stack.pop()
        
        if match.group(1):
            var_decl = match.group(1).strip()
            if '=' in var_decl:
                var_name = var_decl.split('=')[0].strip().split()[-1]
                self.global_vars[var_name] = result
        
        return result

    def process_return(self, line):
        expr = re.match(r'RETORNA ESSA MERDA (.*?);', line).group(1)
        result = self.evaluate_expression(expr)
        self.last_return = result
        return result

    def evaluate_expression(self, expr):
        try:
            expr = expr.strip().rstrip(';')
            
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]
                
            if expr in self.current_context()['vars']:
                return self.current_context()['vars'][expr]
                
            local_vars = self.current_context()['vars'].copy()
            return eval(expr, {}, local_vars)
            
        except Exception as e:
            raise RuntimeError(f"Erro ao avaliar expressão '{expr}': {str(e)}")

    def get_output(self):
        return '\n'.join(self.output)
    
    def show_variables(self):
        print("\nVariáveis declaradas:")
        for nome, valor in self.current_context()['vars'].items():
            print(f"{nome} = {valor} (tipo: {type(valor).__name__})")

def run_ruiva_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    
    compiler = TiaRuivaCompiler()
    try:
        compiler.compile_and_run(code)
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python tia_ruiva_compiler.py hello.ruiva")
        sys.exit(1)
    
    run_ruiva_file(sys.argv[1])