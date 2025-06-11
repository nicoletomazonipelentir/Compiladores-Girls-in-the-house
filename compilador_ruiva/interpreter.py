class RuivaInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {
            'DISK DUNNY': self._handle_print,
            'OLHA SO AQUI': self._handle_input
        }
        self.type_keywords = {
            'Duny FR': {'type': str, 'default': ''},
            'Shaft M1': {'type': int, 'default': 0},
            'Alex M2': {'type': int, 'default': 0},
            'Todd M3': {'type': int, 'default': 0},
            'Honey T': {'type': float, 'default': 0.0},
            'Priscilao TD': {'type': float, 'default': 0.0},
            'Julie FRANGO BF': {'type': int, 'default': 0}
        }

    def interpret(self, code):
        lines = [line.strip() for line in code.split('\n') 
                if line.strip() and not line.strip().startswith('//')]
        
        for line in lines:
            try:
                self._execute_line(line)
            except Exception as e:
                print(f"❌ Erro na linha '{line}': {str(e)}")

    def _execute_line(self, line):
        # Remove ponto e vírgula no final
        line = line.rstrip(';')
        
        # Verifica declaração de variável
        for type_kw in self.type_keywords:
            if line.startswith(type_kw):
                self._handle_declaration(line)
                return
        
        # Verifica comandos/funções
        for cmd in self.functions:
            if cmd in line:
                self._handle_function(line)
                return
        
        # Verifica expressão uuuuh
        if line.strip() == 'uuuuh':
            print("🎉 UUUUH! (expressão de entusiasmo reconhecida)")
            return
        
        # Verifica atribuição
        if '=' in line:
            self._handle_assignment(line)
            return
        
        print(f"⚠️ Comando não reconhecido: {line}")

    def _handle_declaration(self, line):
        # Extrai tipo
        type_kw = next(k for k in self.type_keywords if line.startswith(k))
        remaining = line[len(type_kw):].strip()
        
        # Separa nome e possível valor
        if '=' in remaining:
            var_name, expr = [p.strip() for p in remaining.split('=', 1)]
        else:
            var_name = remaining
            expr = None
        
        # Calcula valor se houver expressão
        if expr:
            try:
                value = eval(expr, {}, self.variables)
                # Converte para o tipo correto
                value = self.type_keywords[type_kw]['type'](value)
            except:
                value = self.type_keywords[type_kw]['default']
        else:
            value = self.type_keywords[type_kw]['default']
        
        self.variables[var_name] = value

    def _handle_function(self, line):
        for func_name, func in self.functions.items():
            if func_name in line:
                # Extrai argumentos
                args_str = line[line.find('(')+1:line.find(')')]
                func(args_str)
                return

    def _handle_print(self, args):
        try:
            if args.startswith('"') and args.endswith('"'):
                print(args[1:-1])
            else:
                print(eval(args, {}, self.variables))
        except Exception as e:
            print(f"Erro ao imprimir: {str(e)}")

    def _handle_input(self, args):
        parts = [p.strip().strip('"') for p in args.split(',')]
        prompt = parts[0]
        var_name = parts[1].replace('&', '')
        
        user_input = input(prompt + " ")
        
        # Tenta converter para o tipo da variável se já existir
        if var_name in self.variables:
            var_type = type(self.variables[var_name])
            try:
                self.variables[var_name] = var_type(user_input)
            except ValueError:
                print(f"Erro: Valor inválido para o tipo da variável {var_name}")
        else:
            # Se variável não declarada, cria como string
            self.variables[var_name] = user_input

    def _handle_assignment(self, line):
        var_name, expr = [p.strip() for p in line.split('=', 1)]
        
        if var_name not in self.variables:
            print(f"Erro: Variável {var_name} não declarada!")
            return
        
        try:
            value = eval(expr, {}, self.variables)
            # Converte para o tipo original da variável
            self.variables[var_name] = type(self.variables[var_name])(value)
        except Exception as e:
            print(f"Erro na atribuição: {str(e)}")