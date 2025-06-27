import re

def traduzir_linguagem(codigo):
    linhas = codigo.splitlines()
    saida = []
    indent = 0

    def add_linha(linha):
        saida.append("    " * indent + linha)

    for linha in linhas:
        linha = linha.strip()
        
        if not linha or linha.startswith("//"):
            continue

        # Tipos de dados
        if re.match(r"(Duny|Shaft|Alex|Todd|Honey|Priscilao|Julie) ", linha):
            linha = re.sub(r"^(?:Duny|Shaft|Alex|Todd|Honey|Priscilao|Julie)\s+(\w+)\s*=\s*(.*);", r"\1 = \2", linha)
            add_linha(linha)
            continue

        if linha.startswith("DISK DUNNY"):
            match_formatado = re.search(r'DISK DUNNY\("(.+?)",\s*(\w+)\);', linha)
            if match_formatado:
                texto = match_formatado.group(1)
                var = match_formatado.group(2)
                # Substitui %d pela variável
                texto_python = texto.replace('%d', f'{{{var}}}')  # Usando f-string
                add_linha(f'print(f"{texto_python}")')
                continue
            
            # Caso simples
            match_simples = re.search(r'DISK DUNNY\("(.+?)"\);', linha)
            if match_simples:
                add_linha(f'print("{match_simples.group(1)}")')
                continue
            match_simples = re.search(r'DISK DUNNY\("(.+?)"\);', linha)
            
            if match_simples:
                add_linha(f'print({match_simples.group(1)})')
                continue

        # Entrada de dados
        if linha.startswith("OLHA SO AQUI"):
            var = re.search(r'OLHA SO AQUI (\w+)\?\("%d", &(\w+)\)', linha)
            if var:
                add_linha(f'{var.group(2)} = int(input())')
            continue

        # If simples
        if linha.startswith("A Katia já foi uma grande mulher"):
            cond = re.search(r'\((.+)\)', linha)
            if cond:
                add_linha(f"if {cond.group(1)}:")
                indent += 1
            continue

        # Elif
        if linha.startswith("Caralhetee"):
            cond = re.search(r'\((.+)\)', linha)
            if cond:
                add_linha(f"elif {cond.group(1)}:")
                indent += 1  # Aumenta somente depois de adicionar a linha
            continue

        # Else
        if linha == "Já fui uma grande mulher":
            add_linha("else:")
            indent += 1  # Aumenta depois de adicionar a linha
            continue


        # Fim de bloco (uuuuh)
        if linha == "uuuuh":
            indent = max(indent - 1, 0)
            continue

        # For loop
        if linha.startswith("KENDRA FOXTI"):
            match = re.search(r'\((\w+) = (\d+); \w+ < (\d+); \w+\+\+\)', linha)
            if match:
                var, start, end = match.groups()
                add_linha(f"for {var} in range({start}, {end}):")
                indent += 1
            continue

        # While
        if linha.startswith("Anteriormente nessa porra"):
            cond = re.search(r'\((.+)\)', linha)
            if cond:
                add_linha(f"while {cond.group(1)}:")
                indent += 1
            continue

        # Declaração de função
        if linha.startswith("PENSAO DA TIA RUIVA RECEBE"):
            match = re.search(r'(\w+)\((.*)\)', linha)
            if match:
                nome_func = match.group(1)
                args = match.group(2).replace("Alex", "").replace("Todd", "").replace(" ", "")
                add_linha(f"def {nome_func}({args}):")
                indent += 1
            continue

        # Return
        if linha.startswith("RETORNA ESSA MERDA"):
            retorno = linha.replace("RETORNA ESSA MERDA", "return")
            add_linha(retorno)
            continue

        # break e continue
        if linha == "DOMENICA;":
            add_linha("continue")
            continue

        if linha == "EU TENHO MAIS O QUE FAZER;":
            add_linha("break")
            continue

        # Decremento (X--)
        if re.match(r"^\w+\-\-;$", linha):
            var = linha.replace("--;", "")
            add_linha(f"{var} -= 1")
            continue

        # Código direto / prints básicos
        if re.match(r"^Ja fui uma grande mulher$", linha):
            add_linha('print("Ja fui uma grande mulher")')
            continue
        elif re.match(r"^uuuuh$", linha):
            add_linha('print("uuuuh")')
            continue

        # Fallback
        add_linha(f"# NÃO RECONHECIDO: {linha}")

    return "\n".join(saida)

# 2. Código da linguagem fictícia
codigo_custom = """
Alex IDADE=0;
DISK DUNNY("Escreva sua idade:");
OLHA SO AQUI Alex?("%d", &IDADE);

// Verificar se pode beber
A Katia já foi uma grande mulher (IDADE >= 18)
    DISK DUNNY("Pode tomar uma gelada!");
    uuuuh
Caralhetee (IDADE <18)
    DISK DUNNY("Ainda não pode, pivete!");
    uuuuh
Já fui uma grande mulher
    DISK DUNNY("Idade inválida!");
    uuuuh
"""

# 3. Executar
codigo_python = traduzir_linguagem(codigo_custom)
print("==== Código Traduzido ====\n")
print(codigo_python)
print("\n==== Saída do Programa ====\n")
exec(codigo_python)
