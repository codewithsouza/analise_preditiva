# ≡ƒñû M├│dulo de Modelos

Este m├│dulo cont├⌐m implementa├º├╡es de modelos preditivos.

## Scripts Planejados

- `baseline.py` - Modelos baseline (m├⌐dia, ├║ltimo valor)
- `time_series_models.py` - ARIMA, Prophet, SARIMA
- `ml_models.py` - Random Forest, XGBoost, LightGBM
- `model_trainer.py` - Classe para treinar e validar modelos
- `model_evaluator.py` - M├⌐tricas e compara├º├úo de modelos
- `model_persistence.py` - Salvar e carregar modelos treinados

## Estrutura

Cada modelo deve implementar:
- `fit()` - Treinar o modelo
- `predict()` - Fazer previs├╡es
- `evaluate()` - Calcular m├⌐tricas
- `save()` - Salvar modelo
- `load()` - Carregar modelo

