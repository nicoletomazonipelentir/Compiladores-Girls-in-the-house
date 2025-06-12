import sys
from interpreter import RuivaInterpreter

def run_ruiva(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"🔧 Interpretando {filename}...\n")
        interpreter = RuivaInterpreter()
        interpreter.interpret(code)
        
        print("\n✅ Execução concluída!")
        print("\nVariáveis finais:")
        for var, val in interpreter.variables.items():
            print(f"{var} = {val}")
            
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado!")
    except Exception as e:
        print(f"Erro fatal: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.ruiva")
    else:
        run_ruiva(sys.argv[1])