"""Agente B: Classificador de Galáxias"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import MockClassifier


class ClassifierAgent:
    """
    Agente responsável por classificar galáxias em spiral ou elliptical
    """

    def __init__(self):
        self.name = "ClassifierAgent"
        self.classifier = MockClassifier()
        self.confidence_threshold = 0.75

    def classify(self, image_tensor):
        """
        Classifica a galáxia

        Args:
            image_tensor: Tensor da imagem processada

        Returns:
            Dict com resultado da classificação
        """
        # Obter predição
        pred_class, confidence = self.classifier.predict(image_tensor)

        # Extrair features para análise
        features = self.classifier.get_features(image_tensor)

        # Determinar se precisa reprocessamento
        needs_reprocessing = confidence < self.confidence_threshold

        return {
            'class': pred_class,
            'confidence': confidence,
            'features': features,
            'needs_reprocessing': needs_reprocessing,
            'status': 'low_confidence' if needs_reprocessing else 'success'
        }

    def get_message_for_preprocessor(self, result):
        """
        Cria mensagem para enviar ao Preprocessor se confiança for baixa

        Args:
            result: Resultado da classificação

        Returns:
            String com mensagem formatada
        """
        if result['needs_reprocessing']:
            return (
                f"Classificação com baixa confiança ({result['confidence']:.2f}).\n"
                f"Features detectadas: variância={result['features']['variance']:.4f}\n"
                f"Recomendo reprocessar a imagem com ajuste de contraste mais agressivo."
            )
        else:
            return None

    def get_final_result(self, result):
        """
        Formata resultado final da classificação

        Args:
            result: Resultado da classificação

        Returns:
            String formatada com resultado
        """
        emoji = "🌀" if result['class'] == 'spiral' else "⚪"

        return (
            f"\n{'='*50}\n"
            f"RESULTADO DA CLASSIFICAÇÃO\n"
            f"{'='*50}\n"
            f"{emoji} Tipo: {result['class'].upper()}\n"
            f"📊 Confiança: {result['confidence']*100:.1f}%\n"
            f"📈 Features:\n"
            f"   - Variância: {result['features']['variance']:.4f}\n"
            f"   - Brilho médio: {result['features']['mean_brightness']:.4f}\n"
            f"   - Intensidade máxima: {result['features']['max_intensity']:.4f}\n"
            f"{'='*50}\n"
        )
