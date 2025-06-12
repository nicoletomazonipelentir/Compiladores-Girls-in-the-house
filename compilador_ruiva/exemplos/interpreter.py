import re

class RuivaInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.loops = []
        self.type_map = {
            'Duny FR': str,
            'Shaft M1': int,
            'Alex M2': int,
            'Todd M3': int,
            'Honey T': float,
            'Priscilao TD': float,
            'Julie FRANGO BF': int
        }
        self.control_structures = {
            'A Katia já foi uma grande mulher': self._handle_if,
            'KENDRA FOXTI': self._handle_for,
            'Anteriormente nessa porra': self._handle_while
        }
        self.keywords = {
            'DOMENICA': 'continue',
            'EU TENHO MAIS O QUE FAZER': 'break',
            'RETORNA ESSA MERDA': 'return'
        }

    def interpret(self, code):
        lines = self._preprocess(code)
        self._execute(lines)

    def _preprocess(self, code):
        # Remove comentários e linhas vazias
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
                # Estruturas de controle
                if any(ctrl in line for ctrl in self.control_structures):
                    ctrl = next(ctrl for ctrl in self.control_structures if ctrl in line)
                    i = self.control_structures[ctrl](lines, i)
                    continue
                
                # Palavras-chave
                if any(kw in line for kw in self.keywords):
                    kw = next(kw for kw in self.keywords if kw in line)
                    action = self.keywords[kw]
                    if action == 'continue':
                        if self.loops:
                            i = self.loops[-1]['continue']
                            continue
                    elif action == 'break':
                        if self.loops:
                            i = self.loops[-1]['break']
                            continue
                    elif action == 'return':
                        return
                
                # Declaração de função
                if 'PENSÃO DA TIA RUIVA RECEBE' in line:
                    i = self._handle_function_def(lines, i)
                    continue
                
                # Chamada de função
                if 'PENSÃO DA TIA RUIVA ENTREGA' in line:
                    self._handle_function_call(line)
                    i += 1
                    continue
                
                # Comandos básicos
                self._execute_line(line)
                i += 1
            except Exception as e:
                print(f"Erro na linha {i+1}: '{line}' - {str(e)}")
                i += 1

    def _execute_line(self, line):
        line = line.rstrip(';')
        
        # DISK DUNNY (print)
        if line.startswith('DISK DUNNY('):
            content = line[11:-1]
            if content.startswith('"') and content.endswith('"'):
                print(content[1:-1])
            else:
                try:
                    print(eval(content, {}, self.variables))
                except:
                    print(f"Erro ao avaliar: {content}")
            return
        
        # OLHA SO AQUI (input)
        if line.startswith('OLHA SO AQUI'):
            match = re.match(r'OLHA SO AQUI (\w+)\?\("([^"]+)", &(\w+)\)', line)
            if match:
                var_type, prompt, var_name = match.groups()
                value = input(prompt + " ")
                try:
                    self.variables[var_name] = self.type_map[var_type](value)
                except:
                    print(f"Valor inválido para {var_type}")
            return
        
        # Declaração de variável
        for type_kw in self.type_map:
            if line.startswith(type_kw):
                parts = line[len(type_kw):].strip().split('=')
                var_name = parts[0].strip()
                if len(parts) > 1:
                    try:
                        self.variables[var_name] = eval(parts[1].strip(), {}, self.variables)
                    except:
                        self.variables[var_name] = self.type_map[type_kw]()
                else:
                    self.variables[var_name] = self.type_map[type_kw]()
                return
        
        # Atribuição
        if '=' in line:
            var_name, expr = [p.strip() for p in line.split('=', 1)]
            if var_name in self.variables:
                try:
                    self.variables[var_name] = eval(expr, {}, self.variables)
                except:
                    print(f"Erro na atribuição: {expr}")
            else:
                print(f"Variável não declarada: {var_name}")
            return
        
        # Expressão uuuuh
        if line.strip() == 'uuuuh':
            return
        
        print(f"Comando não reconhecido: {line}")

    def _handle_if(self, lines, start_idx):
        line = lines[start_idx]
        condition = line[line.find('(')+1:line.find(')')]
        
        try:
            if eval(condition, {}, self.variables):
                # Executa bloco verdadeiro
                end_idx = self._find_block_end(lines, start_idx+1)
                self._execute(lines[start_idx+1:end_idx])
                return end_idx
            else:
                # Procura else/elif
                next_line = lines[start_idx+1]
                if 'Ja fui uma grande mulher' in next_line:
                    end_idx = self._find_block_end(lines, start_idx+2)
                    self._execute(lines[start_idx+2:end_idx])
                    return end_idx
                elif 'Caralhetee' in next_line:
                    condition = next_line[next_line.find('(')+1:next_line.find(')')]
                    if eval(condition, {}, self.variables):
                        end_idx = self._find_block_end(lines, start_idx+2)
                        self._execute(lines[start_idx+2:end_idx])
                        return end_idx
        except:
            print(f"Erro na condição: {condition}")
        
        return self._find_block_end(lines, start_idx) + 1

    def _handle_for(self, lines, start_idx):
        line = lines[start_idx]
        parts = line[line.find('(')+1:line.find(')')].split(';')
        init, cond, inc = [p.strip() for p in parts]
        
        self._execute_line(init)
        start_loop = start_idx + 1
        end_loop = self._find_block_end(lines, start_loop)
        
        self.loops.append({
            'continue': start_loop,
            'break': end_loop + 1
        })
        
        while eval(cond, {}, self.variables):
            self._execute(lines[start_loop:end_loop])
            self._execute_line(inc)
        
        self.loops.pop()
        return end_loop + 1

    def _handle_while(self, lines, start_idx):
        line = lines[start_idx]
        condition = line[line.find('(')+1:line.find(')')]
        start_loop = start_idx + 1
        end_loop = self._find_block_end(lines, start_loop)
        
        self.loops.append({
            'continue': start_loop,
            'break': end_loop + 1
        })
        
        while eval(condition, {}, self.variables):
            self._execute(lines[start_loop:end_loop])
        
        self.loops.pop()
        return end_loop + 1

    def _handle_function_def(self, lines, start_idx):
        line = lines[start_idx]
        signature = line.replace('PENSÃO DA TIA RUIVA RECEBE', '').strip()
        func_name = signature.split('(')[0].strip()
        params = [p.strip() for p in signature.split('(')[1].split(')')[0].split(',')]
        
        body = []
        i = start_idx + 1
        while i < len(lines) and 'RETORNA ESSA MERDA' not in lines[i]:
            body.append(lines[i])
            i += 1
        
        if i < len(lines):
            body.append(lines[i])
        
        self.functions[func_name] = {
            'params': params,
            'body': body
        }
        
        return i + 1

    def _handle_function_call(self, line):
        call = line.replace('PENSÃO DA TIA RUIVA ENTREGA', '').strip()
        func_name = call.split('(')[0].strip()
        args = [a.strip() for a in call.split('(')[1].split(')')[0].split(',')]
        
        if func_name not in self.functions:
            print(f"Função não definida: {func_name}")
            return
        
        func = self.functions[func_name]
        local_vars = {}
        
        for param, arg in zip(func['params'], args):
            try:
                local_vars[param] = eval(arg, {}, self.variables)
            except:
                local_vars[param] = arg
        
        old_vars = self.variables
        self.variables = {**old_vars, **local_vars}
        
        result = None
        for line in func['body']:
            if 'RETORNA ESSA MERDA' in line:
                expr = line.replace('RETORNA ESSA MERDA', '').strip()
                try:
                    result = eval(expr, {}, self.variables)
                except:
                    pass
                break
            self._execute_line(line)
        
        self.variables = old_vars
        return result

    def _find_block_end(self, lines, start_idx):
        depth = 1
        i = start_idx
        while i < len(lines):
            if 'uuuuh' in lines[i]:
                depth -= 1
                if depth == 0:
                    return i
            elif any(ctrl in lines[i] for ctrl in self.control_structures):
                depth += 1
            i += 1
        return len(lines)