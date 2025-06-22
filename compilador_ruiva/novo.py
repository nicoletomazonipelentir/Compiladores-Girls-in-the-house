import re

class TiaRuivaCompiler:
    def __init__(self):
        self.command_map = [
            (r'Open the door and have fun', '# Programa iniciado'),
            (r'KENDRA FOXTI\s*\((.+?)=(.+?);(.+?);(.+?)\+\+\)',
             self._convert_for_loop),
            (r'DISK DUNNY\((.+?)\)', r'print(\1)'),
            (r'uuuuh', r'pass'),
            (r'(\w+)\s+(\w+)\s*=\s*(\d+);', r'\2 = \3'),
            (r'(\w+)\s*=\s*(\d+);', r'\1 = \2')
        ]
    
    def _convert_for_loop(self, match):
        var = match.group(1).strip()
        start = match.group(2).strip()
        end = match.group(3).strip().replace(' ', '')
        return f"for {var} in range({start}, {end}):"
    
    def translate_line(self, line):
        line = line.strip()
        if not line:
            return ''
        
        for pattern, replacement in self.command_map:
            if callable(replacement):
                match = re.fullmatch(pattern, line)
                if match:
                    return replacement(match)
            else:
                if re.fullmatch(pattern, line):
                    return re.sub(pattern, replacement, line)
        
        return line
    
    def compile(self, source_code):
        output = []
        indent = 0
        for line in source_code.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            translated = self.translate_line(line)
            
            # Ajuste de indentação
            if translated.startswith('for '):
                output.append(' ' * indent + translated)
                indent += 4
            elif translated == 'pass':
                output.append(' ' * indent + translated)
            else:
                if indent > 0 and not translated.startswith((' ', '#')):
                    indent = 0
                output.append(' ' * indent + translated)
        
        return '\n'.join(output)

# Exemplo de uso
compiler = TiaRuivaCompiler()
source_code = """Open the door and have fun
Alex M=0;
KENDRA FOXTI (M = 0; M < 5; M++)
    DISK DUNNY(M)
uuuuh
uuuuh"""

compiled_code = compiler.compile(source_code)
print("Código compilado:")
print(compiled_code)

# Salvar e executar
with open('programa.py', 'w') as f:
    f.write(compiled_code)

print("\nExecute com: python programa.py")