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
        self.global_functions = {}  # Dicionário para armazenar funções
        self.current_function = None  # Nome da função sendo processada
        self.context_stack = [{'vars': {}, 'functions': {}}]  # Pilha de contexto
        
    def compile_and_run(self, code):
        self.lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('//')]
        self.current_line = 0  # Adiciona um contador de linha atual

        if not self.lines:
            raise RuntimeError("Código vazio")

        # Verificar abertura e fechamento
        if self.lines[0] != 'Open the door and have fun':
            raise RuntimeError("O código deve começar com 'Open the door and have fun'")
        if self.lines[-1] != 'uuuuh':
            raise RuntimeError("O código deve terminar com 'uuuuh'")

        # Remover a primeira e última linhas
        self.lines = self.lines[1:-1]

        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            try:
                if line.startswith('KENDRA FOXTI'):
                    i = self.process_for_loop(self.lines, i)
                elif line.startswith('Anteriormente nessa porra'):
                    i = self.process_while(self.lines, i)
                elif line.startswith('A Katia já foi uma grande mulher'):
                    i = self.process_conditional_structure(self.lines, i)
                else:
                    self.execute_line(line)
                    i += 1
            except Exception as e:
                raise RuntimeError(f"Erro na linha {i+2}: {line}\n{str(e)}")
    
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
        #"""Captura um bloco de código até encontrar 'uuuuh'"""
        block = []
        i = start_idx
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            block.append(lines[i])
            i += 1
        return block, i
    
    def process_function_declaration(self, line):
        try:
            # Padrão mais robusto para capturar declaração
            match = re.match(
                r'PENSÃO DA TIA RUIVA RECEBE\s*\(([^)]+)\)', 
                line.strip()
            )
            if not match:
                raise SyntaxError("Sintaxe inválida na declaração de função")
            
            # Extrai tipo_retorno, nome_função e parâmetros
            parts = match.group(1).split(None, 2)
            if len(parts) < 2:
                raise SyntaxError("Declaração de função incompleta")
            
            return_type = parts[0]
            func_name = parts[1]
            params_str = parts[2] if len(parts) > 2 else ""
            
            # Processa parâmetros (formato: "Tipo1 nome1, Tipo2 nome2")
            params = []
            for param in params_str.strip('()').split(','):
                param = param.strip()
                if param:
                    type_and_name = param.split()
                    if len(type_and_name) != 2:
                        raise SyntaxError(f"Formato de parâmetro inválido: {param}")
                    params.append({
                        'type': type_and_name[0],
                        'name': type_and_name[1]  # Armazena apenas o nome (sem tipo)
                    })
            
            # Registra a função
            self.global_functions[func_name] = {
                'return_type': return_type,
                'params': params,
                'body': []
            }
            
        except Exception as e:
            raise RuntimeError(f"Erro na declaração de função: {str(e)}")

    def process_function_call(self, line):
        try:
            # Extrai nome da função e argumentos
            func_part = line.split('PENSÃO DA TIA RUIVA ENTREGA')[1].strip()
            func_name = func_part.split('(')[0].strip()
            args_str = func_part.split('(')[1].split(')')[0]
            args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
            
            if func_name not in self.global_functions:
                raise NameError(f"Função '{func_name}' não definida")
            
            func_def = self.global_functions[func_name]
            
            if len(args) != len(func_def['params']):
                raise TypeError(f"Número incorreto de argumentos para {func_name}")

            # Cria novo escopo
            new_scope = {'vars': {}}
            
            # Mapeia argumentos para parâmetros (usando apenas o nome)
            for param, arg in zip(func_def['params'], args):
                arg_value = self.evaluate_expression(arg)
                new_scope['vars'][param['name']] = arg_value
            
            # Executa no novo escopo
            self.context_stack.append(new_scope)
            result = None
            
            for body_line in func_def['body']:
                if body_line.strip().startswith('RETORNA ESSA MERDA'):
                    return_expr = body_line[18:].split(';')[0].strip()
                    result = self.evaluate_expression(return_expr)
                    break
            
            self.context_stack.pop()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Erro na chamada de função: {str(e)}")
    
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
        if not line or line == 'uuuuh':
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
     # Declaração de função
        if line.startswith('PENSÃO DA TIA RUIVA RECEBE'):
            return self.process_function_declaration(line)
            
        # Chamada de função
        elif 'PENSÃO DA TIA RUIVA ENTREGA' in line:
            return self.process_function_call(line)
        
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
            remaining_lines = self._get_remaining_lines()
            return self.process_conditional_structure([line] + remaining_lines, 0)
           # return
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
            # Padroniza a extração dos componentes do for
            match = re.match(r'KENDRA FOXTI\s*\((.*?)\s*;\s*(.*?)\s*;\s*(.*?)\)', line)
            if not match:
                raise SyntaxError("Sintaxe inválida do for loop")
                
            init, condition, increment = match.groups()
            
            # Executa inicialização
            self.execute_line(init)
            
            # Pega o bloco do for (até encontrar 'uuuuh')
            block_lines = []
            i = start_idx + 1
            while i < len(lines) and lines[i].strip() != 'uuuuh':
                block_lines.append(lines[i])
                i += 1
            
            # Executa o loop
            while True:
                # Verifica condição
                if not self.evaluate_expression(condition):
                    break
                
                # Executa o bloco
                for inner_line in block_lines:
                    self.flow_control = None  # Reseta o controle de fluxo
                    self.execute_line(inner_line)
                    
                    # Verifica se houve break
                    if hasattr(self, 'flow_control') and self.flow_control == 'break':
                        delattr(self, 'flow_control')
                        return i + 1  # Sai do loop completamente
                    
                    # Verifica continue
                    if hasattr(self, 'flow_control') and self.flow_control == 'continue':
                        delattr(self, 'flow_control')
                        break  # Pula para próxima iteração
                
                # Executa incremento
                self.execute_line(increment)
            
            return i + 1  # Retorna a linha após o 'uuuuh'
        
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

    def get_remaining_lines(self):
        #"""Retorna as linhas restantes do bloco atual"""
        # Implemente conforme sua estrutura de código
        return self.lines[self.current_line_index+1:]
        
    def process_conditional(self, lines, start_idx):
        i = start_idx
        executed = False
        
        # Processa IF
        if i < len(lines) and lines[i].startswith('A Katia já foi uma grande mulher'):
            condition = lines[i][lines[i].find('(')+1:lines[i].rfind(')')].strip()
            if self.evaluate_expression(condition):
                executed = True
                i = self._execute_block(lines, i+1)
            else:
                i = self._skip_block(lines, i+1)
        
        # Processa ELIF (Caralhetee)
        while i < len(lines) and lines[i].startswith('Caralhetee'):
            if not executed:
                condition = lines[i][lines[i].find('(')+1:lines[i].rfind(')')].strip()
                if self.evaluate_expression(condition):
                    executed = True
                    i = self._execute_block(lines, i+1)
                else:
                    i = self._skip_block(lines, i+1)
            else:
                i = self._skip_block(lines, i+1)
        
        # Processa ELSE (Ja fui uma grande mulher)
        if i < len(lines) and lines[i].startswith('Ja fui uma grande mulher'):
            if not executed:
                i = self._execute_block(lines, i+1)
        
        return i + 1 if i < len(lines) and lines[i].strip() == 'uuuuh' else i

    def process_conditional_blocks(self, lines, start_idx):
        i = start_idx
        executed = False
        
        # Padrões regex para cada tipo de condição
        if_pattern = re.compile(r'A Katia já foi uma grande mulher\s*\((.*)\)')
        elif_pattern = re.compile(r'Caralhetee\s*\((.*)\)')
        else_pattern = re.compile(r'Ja fui uma grande mulher')
        
        # Processa IF
        if_match = if_pattern.match(lines[i])
        if if_match:
            condition = if_match.group(1)
            if self.evaluate_expression(condition):
                executed = True
                i = self._execute_conditional_block(lines, i+1)
            else:
                i = self._skip_to_next_conditional(lines, i+1)
        
        # Processa ELIF (pode ter vários)
        while i < len(lines) and elif_pattern.match(lines[i]):
            if not executed:
                elif_match = elif_pattern.match(lines[i])
                condition = elif_match.group(1)
                if self.evaluate_expression(condition):
                    executed = True
                    i = self._execute_conditional_block(lines, i+1)
                else:
                    i = self._skip_to_next_conditional(lines, i+1)
            else:
                i = self._skip_to_next_conditional(lines, i+1)
        
        # Processa ELSE
        if i < len(lines) and else_pattern.match(lines[i]) and not executed:
            i = self._execute_conditional_block(lines, i+1)
        
        return i

    def _execute_block(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            self.execute_line(lines[i])
            i += 1
        return i

    def _skip_block(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            i += 1
        return i
    
    def process_conditional_structure(self, lines, start_idx):
        i = start_idx
        executed = False
        
        # Extrai condição do IF
        if_cond = lines[i][lines[i].find('(')+1:lines[i].rfind(')')].strip()
        
        # Avalia IF
        if self._eval_condition(if_cond):
            executed = True
            i += 1
            # Executa bloco IF
            while i < len(lines) and not self._is_conditional_end(lines[i]):
                self.execute_line(lines[i])
                i += 1
        else:
            i += 1
            # Pula bloco IF
            while i < len(lines) and not self._is_conditional_end(lines[i]):
                i += 1
        
        # Processa ELIFs
        while i < len(lines) and lines[i].strip().startswith('Caralhetee'):
            if not executed:
                elif_cond = lines[i][lines[i].find('(')+1:lines[i].rfind(')')].strip()
                if self._eval_condition(elif_cond):
                    executed = True
                    i += 1
                    # Executa bloco ELIF
                    while i < len(lines) and not self._is_conditional_end(lines[i]):
                        self.execute_line(lines[i])
                        i += 1
                    continue
            i += 1
            # Pula bloco ELIF
            while i < len(lines) and not lines[i].strip().startswith(('Ja fui', 'uuuuh')):
                i += 1
        
        # Processa ELSE
        if not executed and i < len(lines) and lines[i].strip().startswith('Ja fui'):
            i += 1
            while i < len(lines) and lines[i].strip() != 'uuuuh':
                self.execute_line(lines[i])
                i += 1
        
        return i + 1 if i < len(lines) else i

    def _is_conditional_end(self, line):
        return line.strip().startswith(('Caralhetee', 'Ja fui', 'uuuuh'))

    def _eval_condition(self, expr):
        """Avalia condições booleanas de forma segura"""
        expr = expr.strip(';').strip()
        
        # Tabela de operadores
        ops = {
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '>':  lambda x, y: x > y,
            '<':  lambda x, y: x < y
        }
        
        # Verifica operadores
        for op in ops:
            if op in expr:
                left, right = map(str.strip, expr.split(op, 1))
                left_val = self._eval_simple_expr(left)
                right_val = self._eval_simple_expr(right)
                return ops[op](left_val, right_val)
        
        # Avaliação simples
        return bool(self._eval_simple_expr(expr))

    def _eval_simple_expr(self, expr):
        """Avalia expressões simples (variáveis ou literais)"""
        # Verifica variáveis nos escopos
        for ctx in reversed(self.context_stack):
            if expr in ctx.get('vars', {}):
                return ctx['vars'][expr]
        
        # Tenta converter para número
        try:
            return int(expr)
        except ValueError:
            try:
                return float(expr)
            except ValueError:
                raise ValueError(f"Expressão inválida: {expr}")
    
    def _execute_conditional_block(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and not lines[i].startswith(('Caralhetee', 'Ja fui uma grande mulher', 'uuuuh')):
            self.execute_line(lines[i])
            i += 1
        return i

    def _skip_to_next_branch(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and not lines[i].startswith(('Caralhetee', 'Ja fui uma grande mulher', 'uuuuh')):
            i += 1
        return i

    def _skip_to_end_of_conditional(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            i += 1
        return i
      
    def _get_remaining_lines(self):
        if hasattr(self, 'lines') and hasattr(self, 'current_line'):
            return self.lines[self.current_line + 1:]
        return []


    def _skip_to_next_branch(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and not lines[i].startswith(('Caralhetee', 'Ja fui uma grande mulher', 'uuuuh')):
            i += 1
        return i

    def _skip_to_end_of_conditional(self, lines, start_idx):
        i = start_idx
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            i += 1
        return i

    def _skip_entire_conditional_structure(self, lines, start_idx):
        """Pula toda a estrutura condicional restante"""
        i = start_idx
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            i += 1
        return i

    def process_block(self, lines, start_idx):
        i = start_idx
        while i < len(lines):
            line = lines[i].strip()
            if line in ('Caralhetee', 'Ja fui uma grande mulher', 'uuuuh'):
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

    def process_function_declaration(self, line):
        try:
            # Padrão ajustado para capturar melhor a declaração
            match = re.match(
                r'PENSÃO DA TIA RUIVA RECEBE\s*\((\w+)\s+(\w+)\(([^)]*)\)\)',
                line
            )
            if not match:
                raise SyntaxError("Sintaxe inválida para declaração de função")
            
            return_type = match.group(1)
            func_name = match.group(2)
            params_str = match.group(3)
            
            # Processa cada parâmetro
            params = []
            for param in params_str.split(','):
                param = param.strip()
                if param:
                    # Divide tipo e nome (ex: "Alex A" → ["Alex", "A"])
                    parts = param.split()
                    if len(parts) != 2:
                        raise SyntaxError(f"Formato inválido para parâmetro: {param}")
                    params.append((parts[0], parts[1]))  # (tipo, nome)
            
            # Armazena a definição da função
            self.global_functions[func_name] = {
                'return_type': return_type,
                'params': params,
                'body': []
            }
            self.current_function = func_name
            
        except Exception as e:
            raise RuntimeError(f"Erro na declaração de função: {str(e)}")
    
    
    def process_function_body(self, lines, start_idx):
        func_name = self.current_function
        i = start_idx
        
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            line = lines[i].strip()
            self.global_functions[func_name]['body'].append(line)
            i += 1
        
        self.current_function = None
        return i + 1  # Retorna a linha após o 'uuuuh'
        
    def process_function_call(self, line):
        try:
            # Padrão para capturar chamada de função
            match = re.match(r'PENSÃO DA TIA RUIVA ENTREGA\s+(\w+)\(([^)]*)\)', line)
            if not match:
                raise SyntaxError("Sintaxe inválida para chamada de função")
            
            func_name = match.group(1)
            args = [arg.strip() for arg in match.group(2).split(',') if arg.strip()]
            
            # Verifica se função existe
            if func_name not in self.global_functions:
                raise NameError(f"Função '{func_name}' não definida")
            
            func_def = self.global_functions[func_name]
            
            # Verifica número de argumentos
            if len(args) != len(func_def['params']):
                raise TypeError(f"Número incorreto de argumentos para {func_name}")
            
            # Cria novo escopo para a função
            new_scope = {'vars': {}}
            
            # Atribui valores aos parâmetros
            for (param_type, param_name), arg in zip(func_def['params'], args):
                # Avalia o argumento no escopo atual
                arg_value = self.evaluate_expression(arg)
                # Armazena no escopo da função
                new_scope['vars'][param_name] = arg_value
            
            # Empilha o novo escopo
            self.context_stack.append(new_scope)
            
            # Executa o corpo da função
            result = None
            for body_line in func_def['body']:
                # Verifica se é um return
                if body_line.startswith('RETORNA ESSA MERDA'):
                    return_expr = body_line[18:].strip(' ;')
                    result = self.evaluate_expression(return_expr)
                    break
                # Executa outras linhas
                self.execute_line(body_line)
            
            # Desempilha o escopo
            self.context_stack.pop()
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Erro na chamada de função: {str(e)}")
    
        
    def process_return(self, line):
        expr = re.match(r'RETORNA ESSA MERDA (.*?);', line).group(1)
        result = self.evaluate_expression(expr)
        self.last_return = result
        return result

    def evaluate_expression(self, expr):
        expr = expr.strip().rstrip(';')
        
        # Limpeza da expressão
        expr = expr.replace('(', '').replace(')', '').strip()
        
        # Operadores de comparação
        ops = {'>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y}
        
        for op, func in ops.items():
            if op in expr:
                left, right = expr.split(op, 1)
                left_val = self._eval_simple_expression(left.strip())
                right_val = self._eval_simple_expression(right.strip())
                return func(left_val, right_val)
        
        return self._eval_simple_expression(expr)

    def _eval_simple_expression(self, expr):
        # Verifica variáveis
        for context in reversed(self.context_stack):
            if expr in context.get('vars', {}):
                return context['vars'][expr]
        
        # Tenta como número
        try:
            return int(expr)
        except ValueError:
            try:
                return float(expr)
            except ValueError:
                raise ValueError(f"Expressão inválida: {expr}")
            
    def get_output(self):
        return '\n'.join(self.output)
    
    def show_variables(self):
        print("\nVariáveis declaradas:")
        for nome, valor in self.current_context()['vars'].items():
            print(f"{nome} = {valor} (tipo: {type(valor).__name__})")

def run(self, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        self.lines = [line.strip('\n') for line in f.readlines()]
    
    i = 0
    while i < len(self.lines):
        line = self.lines[i].strip()
        # processa a linha
        i += 1


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