import re

class RuivaInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {} 
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
            line = lines[i].strip()
            if not line:
                i += 1
                continue
                
            try:
                if line.startswith('PENSAO DA TIA RUIVA RECEBE'):
                    i = self._handle_function_declaration(lines, i)
                elif 'PENSAO DA TIA RUIVA ENTREGA' in line:
                    if '=' in line:
                        var_name = line.split('=')[0].strip()
                        result = self._handle_function_call(line)
                        self.variables[var_name] = result
                    else:
                        self._handle_function_call(line)
                    i += 1
                elif line.startswith('Anteriormente nessa porra'):
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


    def _handle_function_declaration(self, lines, start_idx):
        # Extrai a linha de declaração da função
        decl_line = lines[start_idx]
        
        # Extrai a parte entre parênteses
        params_part = decl_line[decl_line.find('(')+1:decl_line.find(')')]
        # Extrai o nome da função (é o primeiro identificador após RECEBE)
        func_name = decl_line.split('RECEBE')[1].split('(')[0].strip()
        
        # Processa os parâmetros
        params = []
        if params_part:
            param_decls = params_part.split(',')
            for param in param_decls:
                param = param.strip()
                # Divide o tipo e nome do parâmetro
                param_parts = param.split()
                if len(param_parts) != 2:
                    raise SyntaxError(f"Declaração de parâmetro inválida: {param}")
                param_type = param_parts[0]
                param_name = param_parts[1]
                params.append((param_type, param_name))
        
        # Extrai o corpo da função
        body = []
        i = start_idx + 1
        while i < len(lines) and lines[i].strip() != 'uuuuh':
            body.append(lines[i].strip())
            i += 1
        
        # Armazena a função
        self.functions[func_name] = {
            'params': params,
            'body': body
        }
        
        return i + 1  # Retorna o índice após o fechamento 'uuuuh'

    def _handle_function_call(self, line):
        # Extrai a parte após ENTREGA
        call_part = line.split('ENTREGA')[1].split(';')[0].strip()
        # O nome da função é tudo antes do '('
        func_name = call_part.split('(')[0].strip()
        # Os argumentos estão dentro dos parênteses
        args_part = call_part[call_part.find('(')+1:call_part.find(')')]
        
        # Processa os argumentos
        args = []
        if args_part:
            for arg in args_part.split(','):
                arg = arg.strip()
                # Remove o tipo se existir (na chamada só usamos os nomes das variáveis)
                if ' ' in arg:
                    arg = arg.split()[1]
                # Avalia o argumento (pode ser variável ou valor literal)
                args.append(eval(arg, {}, self.variables))
        
        # Verifica se a função existe
        if func_name not in self.functions:
            raise NameError(f"Função não definida: {func_name}")
        
        # Prepara o escopo local para a função
        local_vars = {}
        func_info = self.functions[func_name]
        
        # Mapeia os parâmetros para os argumentos
        for (param_type, param_name), arg in zip(func_info['params'], args):
            # Converte o argumento para o tipo do parâmetro
            type_converter = self.type_map.get(param_type, lambda x: x)
            local_vars[param_name] = type_converter(arg)
        
        # Salva variáveis globais e cria novo escopo
        old_vars = self.variables.copy()
        self.variables.update(local_vars)
        
        # Executa o corpo da função
        result = None
        try:
            for line in func_info['body']:
                if line.startswith('RETORNA ESSA MERDA'):
                    return_expr = line.split('RETORNA ESSA MERDA')[1].strip().rstrip(';')
                    result = eval(return_expr, {}, self.variables)
                    break
                self._execute([line])
        finally:
            # Restaura as variáveis globais
            self.variables = old_vars
        
        return result

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