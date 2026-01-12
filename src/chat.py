import sys
import os
from src.search import search_prompt

def main():
    print("Digite 3 para encerrar.")
    
    while True:
        try:
            query = input("\nFaça sua pergunta: ")
            if query.lower().strip() in ["3"]:
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            
            if not query.strip():
                continue
            
            print("Buscando resposta...")
            response = search_prompt(query)
            print(f"\nRESPOSTA: {response}")
            
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()