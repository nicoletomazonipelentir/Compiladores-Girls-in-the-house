import sys
import os
from interpreter import RuivaInterpreter

def compile_ruiva(source_file):
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"🔧 Compilando {source_file}...\n")
        
        interpreter = RuivaInterpreter()
        interpreter.interpret(code)
        
        print("\n✅ Execução concluída!")
        print("\nVariáveis definidas:")
        for var, val in interpreter.variables.items():
            print(f"{var} = {val}")
            
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.ruiva")
    else:
        if not os.path.exists(sys.argv[1]):
            print(f"Arquivo {sys.argv[1]} não encontrado!")
        else:
            compile_ruiva(sys.argv[1])