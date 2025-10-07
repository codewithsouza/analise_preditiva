# ≡ƒº¬ Testes

Esta pasta cont├⌐m testes automatizados para o projeto.

## Estrutura

- `test_data_loading.py` - Testa carregamento de dados
- `test_feature_engineering.py` - Testa cria├º├úo de features
- `test_models.py` - Testa funcionamento dos modelos
- `test_utils.py` - Testa fun├º├╡es utilit├írias

## Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Testes espec├¡ficos
pytest tests/test_data_loading.py
```

## O que testar

- Γ£à Leitura correta de CSVs
- Γ£à Tipos de dados corretos
- Γ£à Tratamento de valores faltantes
- Γ£à Cria├º├úo de features
- Γ£à Consist├¬ncia de pipelines
- Γ£à Formato de sa├¡da dos modelos

