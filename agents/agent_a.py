"""Agente A: Pré-processador de Imagens"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import analyze_image_quality, preprocess_image, load_image
import json


class PreprocessorAgent:
    """
    Agente responsável por analisar qualidade e pré-processar imagens de galáxias
    """

    def __init__(self):
        self.name = "PreprocessorAgent"
        self.image_tensor = None
        self.quality_report = None

    def analyze_quality(self, image_path):
        """
        Analisa qualidade da imagem

        Args:
            image_path: Caminho da imagem

        Returns:
            Dict com relatório de qualidade
        """
        self.image_tensor = load_image(image_path)
        self.quality_report = analyze_image_quality(self.image_tensor)

        return {
            'status': 'analyzed',
            'image_path': image_path,
            'quality': self.quality_report['quality'],
            'brightness': self.quality_report['brightness'],
            'contrast': self.quality_report['contrast'],
            'issues': self.quality_report['issues'],
            'recommendation': 'preprocess' if self.quality_report['needs_preprocessing'] else 'proceed'
        }

    def preprocess(self):
        """
        Aplica pré-processamento na imagem

        Returns:
            Dict com status do processamento
        """
        if self.image_tensor is None:
            return {'status': 'error', 'message': 'No image loaded'}

        original_brightness = self.quality_report['brightness']
        original_contrast = self.quality_report['contrast']

        # Aplicar pré-processamento
        self.image_tensor = preprocess_image(self.image_tensor)

        # Reanalisar qualidade
        new_quality = analyze_image_quality(self.image_tensor)

        return {
            'status': 'preprocessed',
            'original': {
                'brightness': original_brightness,
                'contrast': original_contrast
            },
            'new': {
                'brightness': new_quality['brightness'],
                'contrast': new_quality['contrast']
            },
            'improvement': new_quality['quality']
        }

    def get_processed_image(self):
        """Retorna imagem processada"""
        return self.image_tensor

    def get_message_for_classifier(self, preprocessed=False):
        """
        Cria mensagem para enviar ao Classificador via Autogen

        Args:
            preprocessed: Se a imagem foi pré-processada

        Returns:
            String com mensagem formatada
        """
        if preprocessed:
            return (
                f"Imagem pré-processada e pronta para classificação.\n"
                f"Qualidade: {self.quality_report['quality']}\n"
                f"Brilho ajustado, contraste melhorado.\n"
                f"Por favor, classifique esta galáxia."
            )
        else:
            return (
                f"Imagem analisada - qualidade boa, sem necessidade de pré-processamento.\n"
                f"Brilho: {self.quality_report['brightness']:.2f}, "
                f"Contraste: {self.quality_report['contrast']:.2f}\n"
                f"Por favor, classifique esta galáxia."
            )
