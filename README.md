# Sistema de Classificação de Galáxias Multi-Agente

Sistema simples de classificação de galáxias usando arquitetura multi-agente para disciplina de mestrado.

## Visão Geral

Sistema demonstra comunicação e colaboração entre agentes autônomos para classificar galáxias em **spiral** ou **elliptical**.

### Agentes

- **Agente A (Preprocessor)**: Analisa qualidade da imagem e aplica pré-processamento
- **Agente B (Classifier)**: Classifica galáxias usando CNN mockada
- **Orchestrator**: Coordena comunicação entre agentes

### Fluxo de Trabalho

```
Usuário → Imagem
    ↓
[Agente A] Analisa qualidade
    ↓
[Agente A] Pré-processa (se necessário)
    ↓
[Agente A → Agente B] "Imagem pronta para classificação"
    ↓
[Agente B] Classifica galáxia
    ↓
[Agente B] Confiança baixa? → [Agente B → Agente A] "Reprocessar"
    ↓
Resultado Final + Log de Conversação
```

## Estrutura do Projeto

```
galaxy-classifier/
├── data/
│   └── samples/           # 20 imagens sintéticas (10 spiral, 10 elliptical)
├── agents/
│   ├── agent_a.py         # Agente Preprocessor
│   ├── agent_b.py         # Agente Classifier
│   └── orchestrator.py    # Coordenador Autogen
├── model.py               # CNN mockada
├── utils.py               # Funções auxiliares
├── main.py                # Interface principal
├── generate_dataset.py    # Gera dataset sintético
├── requirements.txt       # Dependências
└── README.md
```

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Gerar dataset sintético (se necessário)
python generate_dataset.py
```

## Uso

### Modo Demo (Recomendado)

```bash
python main.py --demo --show-log
```

Classifica 3 imagens de exemplo e mostra log completo de conversação entre agentes.

### Modo Interativo

```bash
python main.py
```

Menu interativo para escolher imagens.

### Classificar Imagem Específica

```bash
python main.py --image data/samples/spiral_00.png --show-log
```

## Exemplo de Saída

```
🚀 Iniciando classificação: data/samples/spiral_00.png
============================================================

[AGENTE A - PREPROCESSOR] Analisando qualidade da imagem...
   Qualidade: boa
   Issues: Nenhum

[AGENTE A -> AGENTE B]
   Imagem analisada - qualidade boa, sem necessidade de pré-processamento.
   Brilho: 0.32, Contraste: 0.45
   Por favor, classifique esta galáxia.

[AGENTE B - CLASSIFIER] Classificando galáxia...
   Predição: spiral
   Confiança: 0.87

==================================================
RESULTADO DA CLASSIFICAÇÃO
==================================================
🌀 Tipo: SPIRAL
📊 Confiança: 87.0%
📈 Features:
   - Variância: 0.0234
   - Brilho médio: 0.3156
   - Intensidade máxima: 0.9823
==================================================
```

## Características

-  Comunicação entre agentes via Orchestrator
-  Pré-processamento adaptativo
-  Feedback loop (baixa confiança → reprocessamento)
-  Log completo de conversação
-  Dataset sintético (20 imagens)

## Tecnologias

- Python 3.8+
- PyTorch (CNN)
- PIL (Processamento de imagens)
- NumPy (Operações numéricas)
