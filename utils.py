"""Funções auxiliares para processamento de imagens"""
from PIL import Image
import numpy as np


def load_image(image_path):
    """
    Carrega imagem e converte para array numpy

    Args:
        image_path: Caminho da imagem

    Returns:
        Array numpy normalizado [H, W]
    """
    img = Image.open(image_path).convert('L')  # Grayscale
    img = img.resize((128, 128))
    img_array = np.array(img) / 255.0  # Normalizar [0, 1]
    return img_array


def analyze_image_quality(image_array):
    """
    Analisa qualidade da imagem

    Args:
        image_array: Array numpy da imagem

    Returns:
        Dict com métricas de qualidade
    """
    brightness = np.mean(image_array)
    contrast = np.std(image_array)

    # Determinar qualidade
    quality_score = 0
    issues = []

    if brightness < 0.2:
        issues.append("muito escura")
    elif brightness > 0.8:
        issues.append("muito clara")
    else:
        quality_score += 1

    if contrast < 0.1:
        issues.append("baixo contraste")
    else:
        quality_score += 1

    quality = "boa" if quality_score == 2 else "aceitável" if quality_score == 1 else "ruim"

    return {
        'quality': quality,
        'brightness': round(brightness, 3),
        'contrast': round(contrast, 3),
        'issues': issues,
        'needs_preprocessing': len(issues) > 0
    }


def preprocess_image(image_array, enhance_contrast=True, adjust_brightness=True):
    """
    Pré-processa imagem para melhorar qualidade

    Args:
        image_array: Array numpy da imagem
        enhance_contrast: Aplicar equalização de contraste
        adjust_brightness: Ajustar brilho

    Returns:
        Array numpy processado
    """
    processed = image_array.copy()

    # Ajustar brilho
    if adjust_brightness:
        mean_brightness = np.mean(processed)
        if mean_brightness < 0.3:
            processed = processed * 1.5  # Clarear
        elif mean_brightness > 0.7:
            processed = processed * 0.7  # Escurecer

    # Melhorar contraste (histogram equalization simplificado)
    if enhance_contrast:
        pmin = np.percentile(processed, 2)
        pmax = np.percentile(processed, 98)
        processed = (processed - pmin) / (pmax - pmin + 1e-8)

    # Garantir range [0, 1]
    processed = np.clip(processed, 0, 1)

    return processed
