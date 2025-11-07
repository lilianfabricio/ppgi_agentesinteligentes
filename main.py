"""Sistema de Classificação de Galáxias com Agentes Multi-Agent"""
import os
import argparse
from agents.orchestrator import GalaxyClassificationOrchestrator


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Classificador de Galáxias Multi-Agente')
    parser.add_argument('--image', type=str, help='Caminho da imagem a classificar')
    parser.add_argument('--demo', action='store_true', help='Executar demonstração com imagens de exemplo')
    parser.add_argument('--show-log', action='store_true', help='Mostrar log completo de conversação')

    args = parser.parse_args()

    # Criar orchestrator
    orchestrator = GalaxyClassificationOrchestrator()

    if args.demo:
        # Demonstração com imagens do dataset
        print("\n" + "="*60)
        print("DEMO: Classificação de Galáxias Multi-Agente")
        print("="*60)

        demo_images = [
            'data/samples/spiral_00.png',
            'data/samples/elliptical_00.png',
            'data/samples/spiral_05.png'
        ]

        for img_path in demo_images:
            if os.path.exists(img_path):
                result = orchestrator.classify_galaxy(img_path)

                if args.show_log:
                    print(orchestrator.get_conversation_summary())

                print("\n" + "-"*60 + "\n")
                # Reset log para próxima imagem
                orchestrator.conversation_log = []
            else:
                print(f"⚠️  Imagem não encontrada: {img_path}")

    elif args.image:
        # Classificar imagem específica
        if not os.path.exists(args.image):
            print(f"❌ Erro: Imagem não encontrada: {args.image}")
            return

        result = orchestrator.classify_galaxy(args.image)

        if args.show_log:
            print(orchestrator.get_conversation_summary())

    else:
        # Modo interativo
        print("\n" + "="*60)
        print("Sistema de Classificação de Galáxias Multi-Agente")
        print("="*60)
        print("\nOpções disponíveis:")
        print("1. Classificar imagem spiral de exemplo")
        print("2. Classificar imagem elliptical de exemplo")
        print("3. Classificar imagem customizada")
        print("4. Sair")

        while True:
            choice = input("\nEscolha uma opção (1-4): ").strip()

            if choice == '1':
                img_path = 'data/samples/spiral_00.png'
                if os.path.exists(img_path):
                    result = orchestrator.classify_galaxy(img_path)
                    print(orchestrator.get_conversation_summary())
                    orchestrator.conversation_log = []
                else:
                    print("❌ Imagem de exemplo não encontrada!")

            elif choice == '2':
                img_path = 'data/samples/elliptical_00.png'
                if os.path.exists(img_path):
                    result = orchestrator.classify_galaxy(img_path)
                    print(orchestrator.get_conversation_summary())
                    orchestrator.conversation_log = []
                else:
                    print("❌ Imagem de exemplo não encontrada!")

            elif choice == '3':
                img_path = input("Digite o caminho da imagem: ").strip()
                if os.path.exists(img_path):
                    result = orchestrator.classify_galaxy(img_path)
                    print(orchestrator.get_conversation_summary())
                    orchestrator.conversation_log = []
                else:
                    print(f"❌ Erro: Imagem não encontrada: {img_path}")

            elif choice == '4':
                print("\n👋 Encerrando sistema...")
                break

            else:
                print("❌ Opção inválida! Escolha 1-4.")


if __name__ == "__main__":
    main()
