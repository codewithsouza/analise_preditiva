# ≡ƒñ¥ Guia de Contribui├º├úo

Obrigado por considerar contribuir para este projeto!

## Como Contribuir

### 1. Configurar Ambiente de Desenvolvimento

```bash
# Clone o reposit├│rio
git clone [url-do-repo]
cd analise-preditiva

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale depend├¬ncias de desenvolvimento
pip install -r requirements.txt
pip install -e ".[dev]"
```

### 2. Criar Branch para sua Feature

```bash
git checkout -b feature/nome-da-sua-feature
# ou
git checkout -b fix/nome-do-bug
```

### 3. Fazer suas Mudan├ºas

- Escreva c├│digo limpo e documentado
- Adicione testes se aplic├ível
- Siga as conven├º├╡es de c├│digo do projeto
- Atualize documenta├º├úo se necess├írio

### 4. Testar suas Mudan├ºas

```bash
# Executar testes
pytest tests/

# Verificar formata├º├úo
black src/ tests/ --check

# Verificar linting
flake8 src/ tests/
```

### 5. Commitar suas Mudan├ºas

```bash
git add .
git commit -m "Adiciona: descri├º├úo clara da mudan├ºa"
```

**Formato de commits:**
- `Adiciona: ` para novas features
- `Corrige: ` para bug fixes
- `Atualiza: ` para mudan├ºas em c├│digo existente
- `Remove: ` para remo├º├úo de c├│digo
- `Documenta: ` para mudan├ºas em documenta├º├úo

### 6. Push e Pull Request

```bash
git push origin feature/nome-da-sua-feature
```

Depois crie um Pull Request no GitHub com:
- Descri├º├úo clara das mudan├ºas
- Refer├¬ncias a issues relacionadas
- Screenshots se aplic├ível

## Conven├º├╡es de C├│digo

### Python

- **PEP 8**: Siga o guia de estilo Python
- **Type hints**: Use quando poss├¡vel
- **Docstrings**: Documente fun├º├╡es e classes
- **Imports**: Organize como stdlib, third-party, local

```python
"""
Docstring descrevendo o m├│dulo.
"""

import os  # stdlib
from pathlib import Path

import pandas as pd  # third-party
import numpy as np

from src.utils import helper  # local


def my_function(param: str) -> int:
    """
    Breve descri├º├úo da fun├º├úo.
    
    Args:
        param: Descri├º├úo do par├ómetro
        
    Returns:
        Descri├º├úo do retorno
    """
    pass
```

### Notebooks

- **Limpe outputs** antes de commitar
- **Organize em se├º├╡es** com markdown
- **Documente decis├╡es** importantes
- **N├úo hardcode paths** - use Path() e vari├íveis

## Estrutura de Testes

```python
# tests/test_data_loading.py

import pytest
from src.data.load_ecommerce import load_ecommerce_data


def test_load_ecommerce_returns_dataframe():
    """Testa se fun├º├úo retorna DataFrame."""
    df = load_ecommerce_data()
    assert isinstance(df, pd.DataFrame)


def test_load_ecommerce_has_expected_columns():
    """Testa se colunas esperadas est├úo presentes."""
    df = load_ecommerce_data()
    expected_cols = ["Order ID", "Product", "Revenue"]
    assert all(col in df.columns for col in expected_cols)
```

## Reportar Bugs

Use o sistema de issues do GitHub e inclua:

1. **Descri├º├úo clara** do bug
2. **Passos para reproduzir**
3. **Comportamento esperado**
4. **Comportamento atual**
5. **Ambiente** (OS, Python version, etc.)
6. **Screenshots** se relevante

## Sugerir Features

Use o sistema de issues com tag `enhancement`:

1. **Descri├º├úo** da feature
2. **Motiva├º├úo** - por que ├⌐ ├║til
3. **Alternativas** consideradas
4. **Exemplos** de uso

## C├│digo de Conduta

- Seja respeitoso e construtivo
- Aceite cr├¡ticas construtivas
- Foque no melhor para o projeto
- Demonstre empatia com outros contribuidores

## D├║vidas?

Abra uma issue com tag `question` ou entre em contato.

---

Obrigado por contribuir! ≡ƒÄë

