# ≡ƒôê Figuras e Gr├íficos

Esta pasta cont├⌐m gr├íficos e visualiza├º├╡es exportadas dos notebooks.

## Organiza├º├úo Sugerida

Organize por tipo de an├ílise:

```
figures/
Γö£ΓöÇΓöÇ eda/
Γöé   Γö£ΓöÇΓöÇ distribuicao_vendas.png
Γöé   Γö£ΓöÇΓöÇ outliers_boxplot.png
Γöé   ΓööΓöÇΓöÇ correlacao_heatmap.png
Γö£ΓöÇΓöÇ temporal/
Γöé   Γö£ΓöÇΓöÇ vendas_mensais_2019_2020.png
Γöé   Γö£ΓöÇΓöÇ sazonalidade.png
Γöé   ΓööΓöÇΓöÇ tendencia.png
Γö£ΓöÇΓöÇ geografico/
Γöé   Γö£ΓöÇΓöÇ vendas_por_estado.png
Γöé   ΓööΓöÇΓöÇ mapa_calor.png
ΓööΓöÇΓöÇ modelos/
    Γö£ΓöÇΓöÇ feature_importance.png
    Γö£ΓöÇΓöÇ previsao_vs_real.png
    ΓööΓöÇΓöÇ residuals.png
```

## Boas Pr├íticas

1. **Nomes descritivos**: Use nomes que expliquem o conte├║do
2. **Alta resolu├º├úo**: Salve com DPI >= 300 para relat├│rios
3. **Formato PNG**: Para apresenta├º├╡es e web
4. **Formato SVG**: Para gr├íficos que precisam escalar
5. **Versionamento**: Adicione data se necess├írio (vendas_2024_10_06.png)

## C├│digo de Exemplo

```python
import matplotlib.pyplot as plt

# Criar gr├ífico
fig, ax = plt.subplots(figsize=(12, 6))
# ... seu c├│digo de plot ...

# Salvar
plt.savefig('reports/figures/meu_grafico.png', 
            dpi=300, 
            bbox_inches='tight')
plt.close()
```

