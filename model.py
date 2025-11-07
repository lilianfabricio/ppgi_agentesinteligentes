"""Classificador mockado para demonstração de galáxias"""
import numpy as np


class MockClassifier:
    """
    Classificador mockado simples (para demonstração sem treinar CNN)
    Usa heurísticas nas imagens para simular classificação
    """

    def __init__(self):
        self.classes = ['spiral', 'elliptical']

    def predict(self, image_array):
        """
        Prediz classe baseado em características simples da imagem

        Args:
            image_array: Array numpy de imagem [H, W]

        Returns:
            (classe, confiança)
        """
        # Calcular variância e entropia como features simples
        variance = np.var(image_array)
        mean_brightness = np.mean(image_array)

        # Heurística: espirais têm mais variância (braços), elípticas são mais suaves
        if variance > 0.015:
            pred_class = 'spiral'
            confidence = min(0.92, 0.65 + variance * 10)
        else:
            pred_class = 'elliptical'
            confidence = min(0.92, 0.65 + (0.015 - variance) * 10)

        # Ajustar pela intensidade
        if mean_brightness < 0.3:
            confidence *= 0.85  # Baixa confiança em imagens muito escuras

        return pred_class, round(confidence, 2)

    def get_features(self, image_array):
        """Extrai features da imagem para análise"""
        return {
            'variance': round(np.var(image_array), 4),
            'mean_brightness': round(np.mean(image_array), 4),
            'max_intensity': round(np.max(image_array), 4)
        }
