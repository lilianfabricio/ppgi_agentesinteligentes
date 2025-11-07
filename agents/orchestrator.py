"""Orchestrator: Coordena comunicação entre agentes usando Autogen"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agent_a import PreprocessorAgent
from agents.agent_b import ClassifierAgent


class GalaxyClassificationOrchestrator:
    """
    Orquestra a comunicação entre Agente A (Preprocessor) e Agente B (Classifier)
    Implementa padrão de comunicação multi-agente
    """

    def __init__(self):
        self.agent_a = PreprocessorAgent()
        self.agent_b = ClassifierAgent()
        self.conversation_log = []
        self.max_iterations = 3

    def log_message(self, sender, receiver, message):
        """Registra mensagem na conversa"""
        self.conversation_log.append({
            'from': sender,
            'to': receiver,
            'message': message
        })

    def classify_galaxy(self, image_path):
        """
        Pipeline completo de classificação com comunicação entre agentes

        Args:
            image_path: Caminho da imagem

        Returns:
            Dict com resultado e log de conversação
        """
        print(f"\n🚀 Iniciando classificação: {image_path}")
        print("="*60)

        # ETAPA 1: Agente A analisa qualidade
        print("\n[AGENTE A - PREPROCESSOR] Analisando qualidade da imagem...")
        quality_report = self.agent_a.analyze_quality(image_path)

        self.log_message(
            "AgentA_Preprocessor",
            "System",
            f"Análise de qualidade: {quality_report['quality']} "
            f"(brilho={quality_report['brightness']:.2f}, "
            f"contraste={quality_report['contrast']:.2f})"
        )

        print(f"   Qualidade: {quality_report['quality']}")
        print(f"   Issues: {quality_report['issues'] if quality_report['issues'] else 'Nenhum'}")

        # ETAPA 2: Pré-processar se necessário
        preprocessed = False
        if quality_report['recommendation'] == 'preprocess':
            print("\n[AGENTE A] Aplicando pré-processamento...")
            preprocess_result = self.agent_a.preprocess()
            preprocessed = True

            self.log_message(
                "AgentA_Preprocessor",
                "AgentB_Classifier",
                f"Imagem pré-processada. Melhoria aplicada: "
                f"{preprocess_result['original']['brightness']:.2f} -> "
                f"{preprocess_result['new']['brightness']:.2f}"
            )

            print(f"   Brilho: {preprocess_result['original']['brightness']:.2f} -> "
                  f"{preprocess_result['new']['brightness']:.2f}")
            print(f"   Contraste: {preprocess_result['original']['contrast']:.2f} -> "
                  f"{preprocess_result['new']['contrast']:.2f}")

        # ETAPA 3: Agente A comunica com Agente B
        message_to_b = self.agent_a.get_message_for_classifier(preprocessed)
        self.log_message("AgentA_Preprocessor", "AgentB_Classifier", message_to_b)

        print(f"\n[AGENTE A -> AGENTE B]")
        print(f"   {message_to_b}")

        # ETAPA 4: Agente B classifica
        print(f"\n[AGENTE B - CLASSIFIER] Classificando galáxia...")
        processed_image = self.agent_a.get_processed_image()
        result = self.agent_b.classify(processed_image)

        self.log_message(
            "AgentB_Classifier",
            "System",
            f"Classificação: {result['class']} (confiança={result['confidence']:.2f})"
        )

        print(f"   Predição: {result['class']}")
        print(f"   Confiança: {result['confidence']:.2f}")

        # ETAPA 5: Se baixa confiança, Agente B pode pedir reprocessamento
        iteration = 1
        while result['needs_reprocessing'] and iteration < self.max_iterations:
            print(f"\n[AGENTE B -> AGENTE A] Solicitando reprocessamento (iteração {iteration})...")

            message_to_a = self.agent_b.get_message_for_preprocessor(result)
            self.log_message("AgentB_Classifier", "AgentA_Preprocessor", message_to_a)

            print(f"   {message_to_a}")

            # Agente A reprocessa com ajustes mais agressivos
            print("\n[AGENTE A] Reprocessando com ajustes mais agressivos...")
            self.agent_a.preprocess()
            processed_image = self.agent_a.get_processed_image()

            # Agente B tenta novamente
            print(f"\n[AGENTE B] Reclassificando...")
            result = self.agent_b.classify(processed_image)
            print(f"   Nova confiança: {result['confidence']:.2f}")

            iteration += 1

        # ETAPA 6: Resultado final
        final_message = self.agent_b.get_final_result(result)
        self.log_message("AgentB_Classifier", "User", final_message)

        print(final_message)

        return {
            'success': True,
            'classification': result['class'],
            'confidence': result['confidence'],
            'preprocessed': preprocessed,
            'iterations': iteration,
            'conversation_log': self.conversation_log
        }

    def get_conversation_summary(self):
        """Retorna sumário da conversação entre agentes"""
        summary = "\n" + "="*60 + "\n"
        summary += "LOG DE CONVERSAÇÃO ENTRE AGENTES\n"
        summary += "="*60 + "\n"

        for i, msg in enumerate(self.conversation_log, 1):
            summary += f"\n[{i}] {msg['from']} -> {msg['to']}\n"
            summary += f"    {msg['message']}\n"

        return summary
