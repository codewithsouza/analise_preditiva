# ≡ƒôï Resumo do Projeto - An├ílise Preditiva de Vendas

## ≡ƒÄ» Vis├úo Geral

Projeto completo de an├ílise e previs├úo de vendas utilizando tr├¬s fontes de dados diferentes:
- E-commerce (transa├º├╡es detalhadas)
- Retail/Warehouse (dados agregados mensais)
- Vendas hist├│ricas (m├║ltiplos CSVs mensais)

## ≡ƒôè Datasets

| Dataset | Arquivo | Per├¡odo | Tipo | Status |
|---------|---------|---------|------|--------|
| E-commerce | `Updated_sales.csv` | - | Transacional | ΓÅ│ Pendente |
| Retail/Warehouse | `Retail and wherehouse Sale.csv` | 2020 | Agregado | ΓÅ│ Pendente |
| Vendas Hist├│ricas | `Sales_Data/*.csv` | 2019 | Transacional | ΓÅ│ Pendente |

## ≡ƒùé∩╕Å Estrutura Criada

```
Γ£à Diret├│rios de dados (raw, processed, external)
Γ£à Estrutura de notebooks (explora├º├úo, limpeza, features, modelagem)
Γ£à M├│dulos Python organizados (data, features, models, visualization)
Γ£à Configura├º├╡es (requirements.txt, config.yaml, setup.py)
Γ£à Documenta├º├úo (README, QUICK_START, STRUCTURE)
Γ£à Templates e exemplos
```

## ≡ƒô¥ Arquivos Criados

### Documenta├º├úo
- Γ£à `README.md` - Documenta├º├úo principal do projeto
- Γ£à `QUICK_START.md` - Guia r├ípido para come├ºar
- Γ£à `STRUCTURE.md` - Explica├º├úo detalhada da estrutura
- Γ£à `CONTRIBUTING.md` - Guia de contribui├º├úo
- Γ£à `CHANGELOG.md` - Hist├│rico de mudan├ºas

### Configura├º├úo
- Γ£à `requirements.txt` - Depend├¬ncias Python
- Γ£à `setup.py` - Configura├º├úo do pacote
- Γ£à `config/config.yaml` - Configura├º├╡es do projeto
- Γ£à `Makefile` - Comandos ├║teis
- Γ£à `.gitignore` - Arquivos ignorados pelo Git
- Γ£à `LICENSE` - Licen├ºa MIT

### C├│digo
- Γ£à `src/data/load_ecommerce.py` - Carregador de e-commerce
- Γ£à `src/data/load_retail.py` - Carregador de retail
- Γ£à `src/data/load_sales_data.py` - Carregador de sales data
- Γ£à `src/features/build_features.py` - Feature engineering
- Γ£à `src/__init__.py` - Inicializa├º├úo dos m├│dulos
- Γ£à M├│dulos: data, features, models, visualization

### Notebooks
- Γ£à `notebooks/01_exploracao/ecommerce_eda.ipynb` - Template de explora├º├úo
- Γ£à READMEs em cada pasta de notebooks

### Outros
- Γ£à READMEs em todos os diret├│rios principais
- Γ£à `.gitkeep` em pastas de dados
- Γ£à Estrutura completa de testes

## ≡ƒÜÇ Pr├│ximos Passos

### Fase 1: Prepara├º├úo de Dados ΓÅ│
- [ ] Colocar arquivos CSV em `data/raw/`
- [ ] Implementar scripts de carregamento
- [ ] Executar limpeza de dados
- [ ] Validar qualidade dos dados

### Fase 2: Explora├º├úo ≡ƒôè
- [ ] An├ílise explorat├│ria de cada dataset
- [ ] Identificar padr├╡es e tend├¬ncias
- [ ] Documentar insights principais
- [ ] Criar visualiza├º├╡es iniciais

### Fase 3: Feature Engineering ΓÜÖ∩╕Å
- [ ] Implementar features temporais
- [ ] Implementar features geogr├íficas
- [ ] Criar features agregadas
- [ ] Selecionar features relevantes

### Fase 4: Modelagem ≡ƒñû
- [ ] Desenvolver modelos baseline
- [ ] Implementar modelos de s├⌐ries temporais
- [ ] Treinar modelos de ML
- [ ] Avaliar e comparar modelos

### Fase 5: Deployment ≡ƒÜÇ
- [ ] Criar dashboard interativo
- [ ] Automatizar pipeline
- [ ] Documentar resultados
- [ ] Preparar apresenta├º├úo

## ≡ƒôª Depend├¬ncias Principais

```
pandas>=2.0.0          # Manipula├º├úo de dados
numpy>=1.24.0          # Computa├º├úo num├⌐rica
matplotlib>=3.7.0      # Visualiza├º├úo
seaborn>=0.12.0        # Visualiza├º├úo estat├¡stica
scikit-learn>=1.3.0    # Machine Learning
prophet>=1.1.0         # S├⌐ries temporais
jupyter>=1.0.0         # Notebooks
```

## ≡ƒÄô Conceitos e T├⌐cnicas

### An├ílise Explorat├│ria
- Estat├¡sticas descritivas
- An├ílise de distribui├º├╡es
- Identifica├º├úo de outliers
- An├ílise de correla├º├╡es
- Visualiza├º├╡es

### Feature Engineering
- Features temporais (m├¬s, hora, dia da semana)
- Features geogr├íficas (cidade, estado, regi├úo)
- Features agregadas (soma, m├⌐dia, contagem)
- Encoding de vari├íveis categ├│ricas

### Modelagem
- Modelos baseline (m├⌐dia, ├║ltimo valor)
- S├⌐ries temporais (ARIMA, Prophet, SARIMA)
- Machine Learning (Random Forest, XGBoost)
- Ensemble methods

### Avalia├º├úo
- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- MAPE (Mean Absolute Percentage Error)
- R┬▓ Score

## ≡ƒÆí Dicas Importantes

1. **Sempre trabalhe em branch separado**
   ```bash
   git checkout -b feature/minha-analise
   ```

2. **Limpe outputs de notebooks antes de commitar**
   ```bash
   # Cell > All Output > Clear
   ```

3. **Use caminhos relativos**
   ```python
   from pathlib import Path
   data_path = Path("../../data/raw/arquivo.csv")
   ```

4. **Documente suas descobertas**
   - Crie arquivos .md em `reports/insights/`
   - Salve gr├íficos em `reports/figures/`

5. **Teste seu c├│digo**
   ```bash
   pytest tests/ -v
   ```

## ≡ƒôº Contato e Suporte

- Issues: Use o sistema de issues do GitHub
- Documenta├º├úo: Veja READMEs em cada pasta
- D├║vidas: Consulte QUICK_START.md

## ΓÜû∩╕Å Licen├ºa

MIT License - Veja arquivo LICENSE para detalhes

---

**Status do Projeto:** ≡ƒƒí Em Desenvolvimento  
**├Ültima Atualiza├º├úo:** 06/10/2025  
**Vers├úo:** 0.1.0

