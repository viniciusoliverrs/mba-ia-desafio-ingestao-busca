import sys
import os
from src.ingest import ingest_pdf
from src.chat import main as start_chat

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        print("""
        === MENU PRINCIPAL ===
        1. Ingestão de Documentos (Ingest)
        2. Iniciar Chat (Search)
        3. Sair
        =====================
        """)
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == "1":
            print("\nIniciando ingestão...")
            try:
                ingest_pdf()
            except Exception as e:
                print(f"Erro na ingestão: {e}")
            input("\nPressione Enter para continuar...")
            
        elif choice == "2":
            print("\nIniciando Chat...")
            try:
                start_chat()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print(f"Erro no chat: {e}")
            
        elif choice == "3":
            sys.exit(0)
            
        else:
            input("""
            Opção inválida!
            Pressione Enter para tentar novamente...
            """)

if __name__ == "__main__":
    main()
