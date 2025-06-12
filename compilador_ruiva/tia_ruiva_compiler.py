import re

class TiaRuivaCompiler:
    def __init__(self):
        self.variables = {}
        self.reset()
        
    def reset(self):
        self.variables = {}
        # Mapeamento de tipos
        self.type_map = {
            'Duny': str,    # char
            'Shaft': int,   # short
            'Alex': int,    # int
            'Todd': int,    # long
            'Honey': float, # float
            'Priscilao': float, # double
            'Julie': int    # unsigned
        }
        
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
                else:
                    self.execute_line(line)
                    i += 1
            except Exception as e:
                raise RuntimeError(f"Erro na linha {i+2}: {line}\n{str(e)}")

    def get_block(self, lines, start_idx):
        #"""Captura um bloco de código até encontrar 'uuuuh'"""
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
            if line.startswith("A Katia já foi uma grande mulher"):
                i = self.process_if_else(lines, i)
                continue  # já atualizou i, continuar do próximo
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
            # Pode adicionar mais reconhecimentos aqui...

            i += 1

    def execute_line(self, line):
        line = line.strip()

        # Se for incremento pós-fixado do tipo "M++"
        if re.match(r'^\w+\+\+$', line):
            var = line[:-2]  # tira os dois últimos caracteres '++'
            # transforma em atribuição normal: M = M + 1
            line = f"{var} = {var} + 1"

        # Agora executa normalmente (chame seu process_assignment ou o que for)
        if '=' in line:
            self.process_assignment(line)
            if re.match(r'^\w+\+\+;?$', line):
                var = line.replace('+', '').replace(';', '')
                self.execute_line(f"{var} = {var} + 1")
                return
            elif re.match(r'^\w+--;?$', line):
                var = line.replace('-', '').replace(';', '')
                self.execute_line(f"{var} = {var} - 1")
                return
            # 1. Detecta declaração de variáveis (deve vir primeiro)
            if any(line.startswith(tipo + ' ') for tipo in self.type_map):
                self.process_variable_declaration(line)
                return
                
            # 2. Detecta prints
            elif line.startswith('DISK DUNNY'):
                self.process_print(line)
                return
            
            elif line.startswith('KENDRA FOXTI'):
                    self.process_print(line)
                    return
            # 3. Detecta atribuições (ex: X = 10;)
            elif '=' in line and not line.startswith(('A Katia', 'Anteriormente')):
                self.process_assignment(line)
                return
                
            # 4. Detecta condicionais (if)
            elif line.startswith('A Katia já foi uma grande mulher'):
                self.process_if(line)
                return
                
            # 5. Detecta loops (while)
            elif line.startswith('Anteriormente nessa porra'):
                self.process_while(line)
                return
                
            # 6. Detecta continue/break
            elif line == 'DOMENICA;':
                self.flow_control = 'continue'
                return
            elif line == 'EU TENHO MAIS O QUE FAZER;':
                self.flow_control = 'break'
                return
                
            # 7. Detecta declaração de função
            elif line.startswith('PENSÃO DA TIA RUIVA RECEBE'):
                self.process_function_declaration(line)
                return
                
            # 8. Detecta chamada de função
            elif 'PENSÃO DA TIA RUIVA ENTREGA' in line:
                self.process_function_call(line)
                return
                
            # 9. Detecta return
            elif line.startswith('RETORNA ESSA MERDA'):
                self.process_return(line)
                return
                
            # 10. Linha vazia ou comentário (já filtrado anteriormente)
            elif not line or line.startswith('//'):
                return
                
            # 11. Comando não reconhecido
            else:
                raise SyntaxError(f"Comando não reconhecido: {line}")


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
            # Assumindo que a condição é no formato 'VAR < valor'
            var_cond = condition.split()[0]
            if var_cond not in self.variables:
                self.variables[var_cond] = 0
            
            block, end_idx = self.get_block(lines, start_idx + 1)
            
            while True:
                if not self.evaluate_expression(condition):
                    break
                
                self.execute_block(block)
                
                # Tratar incremento do tipo M++
                inc_line = increment.strip()
                if re.match(r'^\w+\+\+$', inc_line):
                    var_inc = inc_line[:-2]
                    inc_line = f"{var_inc} = {var_inc} + 1"
                self.execute_line(inc_line)
            
            return end_idx
        except Exception as e:
            raise RuntimeError(f"Erro no for loop: {str(e)}")




    def process_if_else(self, lines, start_idx):
        line = lines[start_idx].strip()
        print(f"process_if_else: processando linha {start_idx}: {line}")
        match = re.match(r'A Katia já foi uma grande mulher\s*\((.*)\)', line)
        if not match:
            raise SyntaxError(f"Condicional if inválida: {line}")
        condition = match.group(1)
        cond_value = self.evaluate_expression(condition)
        print(f"process_if_else: condição '{condition}' avaliada como {cond_value}")

        body = []
        i = start_idx + 1
        while i < len(lines):
            if lines[i].strip() in ('uuuuh;', 'uuuuh'):
                print(f"process_if_else: fim do bloco encontrado na linha {i}: {lines[i].strip()}")
                break
            body.append(lines[i])
            i += 1

        if cond_value:
            print(f"process_if_else: executando bloco com {len(body)} linhas")
            self.execute_block(body)
        else:
            print("process_if_else: condição falsa, bloco ignorado")

        print(f"process_if_else: retornando próxima linha {i + 1}")
        return i + 1

    def process_conditional(self, lines, start_idx):
        i = start_idx
        executed_block = False

        while i < len(lines):
            line = lines[i].strip()

            # if
            if line.startswith('A Katia já foi uma grande mulher'):
                if executed_block:
                    # já executou algum bloco antes, pular esse
                    i = self.skip_block(lines, i+1)
                else:
                    i = self.process_if_else(lines, i)
                    executed_block = True

            # else if
            elif line.startswith('Caralhetee'):
                if executed_block:
                    i = self.skip_block(lines, i+1)
                else:
                    i = self.process_else_if(lines, i)
                    executed_block = True

            # else
            elif line.startswith('Ja fui uma grande mulher'):
                if executed_block:
                    # pula bloco else
                    i = self.skip_block(lines, i+1)
                else:
                    i = self.process_else(lines, i)
                    executed_block = True

            else:
                # Se não for nenhuma das condicionais, para o loop
                break

        return i

    def skip_block(self, lines, start_idx):
        i = start_idx
        while i < len(lines):
            if lines[i].strip() in ('uuuuh;', 'uuuuh'):
                return i + 1
            i += 1
        return i

    def get_next_block(self):
        block = []
        while True:
            line = self.get_next_line()  # Você precisará implementar isso
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
        if '=' not in line:
            raise Exception("Atribuição mal formada")

        var, value = line.split('=', 1)  # melhor garantir só uma divisão
        var = var.strip()
        value = value.strip()

        if '+' in value:
            left, right = value.split('+')
            left = left.strip()
            right = int(right.strip())
            if left == var:
                self.variables[var] += right
            else:
                raise Exception("Expressão inválida na atribuição")
        else:
            try:
                self.variables[var] = int(value)
            except ValueError:
                self.variables[var] = value





    def process_increment(self, line):
        if line.startswith("INCREMENTA"):
            var = line.split()[1]
            if var in self.variables:
                self.variables[var] += 1
            else:
                raise Exception(f"Variável '{var}' não definida para incremento")




    
    def process_while(self, lines, i):
        line = lines[i]
        condition_start = line.find('(') + 1
        condition_end = line.rfind(')')
        condition = line[condition_start:condition_end].strip()

        block_lines = []
        i += 1

        # Coletar o bloco do while
        while i < len(lines) and lines[i] != 'uuuuh;':
            block_lines.append(lines[i])
            i += 1

        # Ignorar o 'uuuuh;'
        i += 1

        # Executar enquanto a condição for verdadeira
        while self.evaluate_expression(condition):
            for inner_line in block_lines:
                # Permitir break e continue personalizados
                self.flow_control = None
                self.execute_line(inner_line)

                if self.flow_control == 'break':
                    return i  # sai do while
                elif self.flow_control == 'continue':
                    break  # volta para o while sem terminar o bloco

        return i  # retorna a próxima linha após o bloco


    def process_variable_declaration(self, line):
        try:
            # Padrão para: "Tipo nome = valor" (ponto e vírgula opcional)
            match = re.match(r'(\w+)\s+(\w+)\s*(?:=\s*(.*?)\s*)?;?$', line)
            if not match:
                raise SyntaxError(f"Declaração inválida: {line}")
            
            tipo, nome, valor = match.groups()
            
            if tipo not in self.type_map:
                raise SyntaxError(f"Tipo desconhecido: {tipo}")
            
            # Se não tiver valor, inicializa com padrão
            if valor is None or valor.strip() == '':
                valor_avaliado = 0 if self.type_map[tipo] == int else 0.0 if self.type_map[tipo] == float else ''
            else:
                # Remove qualquer ponto e vírgula residual antes de avaliar
                valor = valor.rstrip(';').strip()
                valor_avaliado = self.evaluate_expression(valor)
            
            # Converte para o tipo correto
            self.current_context()['vars'][nome] = self.type_map[tipo](valor_avaliado)
            
        except Exception as e:
            raise RuntimeError(f"Erro na declaração de variável '{nome}': {str(e)}")

    def process_print(self, line):
        try:
            match = re.match(r'DISK DUNNY\((.+)\);?', line)
            if not match:
                raise ValueError(f"Sintaxe inválida no print: {line}")
            
            content = match.group(1).strip()
            
            # Se for string literal
            if content.startswith('"') and content.endswith('"'):
                print(content[1:-1])  # Remove as aspas
            else:
                # Se for variável ou expressão
                try:
                    value = self.evaluate_expression(content)
                    print(str(value))
                except Exception as e:
                    raise ValueError(f"Erro ao avaliar expressão '{content}': {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Erro no processamento do print: {str(e)}")

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
        
        # Armazenar a função no contexto atual
        self.current_context()['functions'][func_name] = {
            'params': param_list,
            'body': body
        }
        
        return i + 1  # Retorna o índice da linha após o uuuuh

    def process_function_call(self, line):
        # Exemplo: Alex res = PENSÃO DA TIA RUIVA ENTREGA FAT(num);
        match = re.match(r'(\w+\s+\w+\s*=\s*)?PENSÃO DA TIA RUIVA ENTREGA (\w+)\(([^)]*)\);', line)
        if not match:
            raise SyntaxError(f"Chamada de função inválida: {line}")
            
        func_name = match.group(2)
        args = [self.evaluate_expression(a.strip()) for a in match.group(3).split(',') if a.strip()]
        
        # Procurar a função na hierarquia de contextos
        func_def = None
        for context in reversed(self.context_stack):
            if func_name in context['functions']:
                func_def = context['functions'][func_name]
                break
        
        if not func_def:
            raise NameError(f"Função não definida: {func_name}")
            
        if len(args) != len(func_def['params']):
            raise TypeError(f"Número incorreto de argumentos para {func_name}")
        
        # Criar novo contexto para a função
        new_context = {
            'vars': dict(zip(func_def['params'], args)),
            'functions': {}
        }
        
        self.context_stack.append(new_context)
        
        # Executar o corpo da função
        result = None
        body_code = '\n'.join(func_def['body'])
        try:
            self.compile_and_run(body_code)
        except Exception as e:
            self.context_stack.pop()
            raise e
        
        # Se houve retorno explícito, pegar o valor
        if hasattr(self, 'last_return'):
            result = self.last_return
            delattr(self, 'last_return')
        
        # Remover o contexto da função
        self.context_stack.pop()
        
        # Se a atribuição foi especificada, armazenar o resultado
        if match.group(1):
            var_decl = match.group(1).strip()
            if '=' in var_decl:
                var_name = var_decl.split('=')[0].strip().split()[-1]
                self.global_vars[var_name] = result
        
        return result

    def process_return(self, line):
        # Exemplo: RETORNA ESSA MERDA 1;
        expr = re.match(r'RETORNA ESSA MERDA (.*?);', line).group(1)
        result = self.evaluate_expression(expr)
        self.last_return = result
        return result

    def evaluate_expression(self, expr):
        local_vars = self.variables.copy()
        try:
            return eval(expr, {}, local_vars)
        except Exception as e:
            raise RuntimeError(f"Erro ao avaliar expressão '{expr}': {e}")
        
        expr = expr.strip().rstrip(';')

        # Verifica se é uma string entre aspas
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        # Procura variáveis nos contextos
        for context in reversed(self.context_stack):
            if expr in context['vars']:
                return context['vars'][expr]

        # Tenta avaliar como expressão usando variáveis do contexto atual
        try:
            # Monta dicionário com todas as variáveis acessíveis
            local_vars = {}
            for context in self.context_stack:
                local_vars.update(context['vars'])
            local_vars.update(self.global_vars)

            return eval(expr, {}, local_vars)
        except Exception as e:
            raise ValueError(f"Não foi possível avaliar a expressão '{expr}': {str(e)}")


    def get_output(self):
        return '\n'.join(self.output)
    
    def show_variables(self):
        print("\nVariáveis declaradas:")
        for nome, valor in self.current_context()['vars'].items():
            print(f"{nome} = {valor} (tipo: {type(valor).__name__})")

# Adicione esta função no nível raiz do arquivo (sem indentação)
def run_ruiva_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    
    compiler = TiaRuivaCompiler()
    try:
        compiler.compile_and_run(code)
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

# O bloco main deve vir depois de todas as definições
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python tia_ruiva_compiler.py hello.ruiva")
        sys.exit(1)
    
    run_ruiva_file(sys.argv[1])

