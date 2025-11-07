"""Script para gerar dataset sintético de galáxias"""
import numpy as np
from PIL import Image
import os

def generate_spiral_galaxy(size=128, seed=None):
    """Gera imagem sintética de galáxia espiral"""
    if seed is not None:
        np.random.seed(seed)

    img = np.zeros((size, size))
    center = size // 2

    # Criar braços espirais
    theta = np.linspace(0, 4 * np.pi, 1000)
    for arm in range(2):
        offset = arm * np.pi
        r = theta * 5
        x = center + (r * np.cos(theta + offset)).astype(int)
        y = center + (r * np.sin(theta + offset)).astype(int)

        valid = (x >= 0) & (x < size) & (y >= 0) & (y < size)
        x, y = x[valid], y[valid]

        for i in range(len(x)):
            if 0 <= x[i] < size and 0 <= y[i] < size:
                img[y[i], x[i]] = 200 + np.random.randint(-50, 50)

    # Adicionar núcleo brilhante
    y, x = np.ogrid[:size, :size]
    dist = np.sqrt((x - center)**2 + (y - center)**2)
    img += 100 * np.exp(-dist**2 / 200)

    # Adicionar ruído
    img += np.random.normal(0, 10, (size, size))

    return np.clip(img, 0, 255).astype(np.uint8)


def generate_elliptical_galaxy(size=128, seed=None):
    """Gera imagem sintética de galáxia elíptica"""
    if seed is not None:
        np.random.seed(seed)

    img = np.zeros((size, size))
    center = size // 2

    # Criar forma elíptica suave
    y, x = np.ogrid[:size, :size]
    ellipse_a = 30 + np.random.randint(-5, 5)
    ellipse_b = 20 + np.random.randint(-5, 5)

    dist_ellipse = ((x - center)**2 / ellipse_a**2 + (y - center)**2 / ellipse_b**2)
    img = 200 * np.exp(-dist_ellipse * 2)

    # Adicionar gradiente suave
    img += 50 * np.exp(-dist_ellipse * 0.5)

    # Adicionar ruído
    img += np.random.normal(0, 10, (size, size))

    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    """Gera dataset de 20 imagens (10 spiral, 10 elliptical)"""
    output_dir = "data/samples"
    os.makedirs(output_dir, exist_ok=True)

    # Gerar galáxias espirais
    print("Gerando galáxias espirais...")
    for i in range(10):
        img_array = generate_spiral_galaxy(seed=i)
        img = Image.fromarray(img_array, mode='L')
        img.save(f"{output_dir}/spiral_{i:02d}.png")

    # Gerar galáxias elípticas
    print("Gerando galáxias elípticas...")
    for i in range(10):
        img_array = generate_elliptical_galaxy(seed=i+100)
        img = Image.fromarray(img_array, mode='L')
        img.save(f"{output_dir}/elliptical_{i:02d}.png")

    print(f"✓ Dataset criado: 20 imagens em {output_dir}/")


if __name__ == "__main__":
    main()
