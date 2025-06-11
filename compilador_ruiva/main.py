from lexer import lexer
from parser import Parser
from interpreter import Interpreter
import sys

def run_ruiva(source_file):
    with open(source_file, 'r') as f:
        code = f.read()
    
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    interpreter.execute(ast)

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Uso: python main.py arquivo.ruiva")
            print(f"Recebido {len(sys.argv)-1} argumento(s): {sys.argv[1:]}")
        else:
            if not os.path.exists(sys.argv[1]):
                print(f"Erro: Arquivo '{sys.argv[1]}' não encontrado!")
            else:
                print(f"Processando arquivo: {sys.argv[1]}")
                run_ruiva(sys.argv[1])
    except Exception as e:
        print(f"Erro inesperado: {e}")