# ≡ƒôï Guia de Estrutura do Projeto

Este documento explica a organiza├º├úo e finalidade de cada pasta e arquivo no projeto.

## ≡ƒùé∩╕Å Estrutura de Diret├│rios

### `/data`
Cont├⌐m todos os dados do projeto organizados em subpastas:

- **`/raw`**: Dados brutos originais (n├úo devem ser modificados)
  - `Updated_sales.csv` - Dataset de e-commerce
  - `Retail and wherehouse Sale.csv` - Dataset de varejo/warehouse
  - `/Sales_Data/` - Pasta com m├║ltiplos CSVs mensais

- **`/processed`**: Dados limpos e processados prontos para an├ílise
  - Arquivos .parquet para melhor performance
  - Dados validados e sem duplicatas

- **`/external`**: Dados externos complementares (feriados, dados econ├┤micos, etc.)

### `/notebooks`
Notebooks Jupyter organizados por fase do projeto:

- **`/01_exploracao`**: An├ílise explorat├│ria inicial dos dados
- **`/02_limpeza`**: Limpeza e valida├º├úo de dados
- **`/03_feature_engineering`**: Cria├º├úo de features
- **`/04_modelagem`**: Modelos preditivos e avalia├º├úo

### `/src`
C├│digo fonte reutiliz├ível organizado em m├│dulos:

- **`/data`**: Scripts para carregar e preparar dados
  - `load_ecommerce.py`
  - `load_retail.py`
  - `load_sales_data.py`
  - `data_validator.py`

- **`/features`**: Scripts para feature engineering
  - `build_features.py`
  - `temporal_features.py`
  - `geographic_features.py`

- **`/models`**: Implementa├º├╡es de modelos preditivos
  - `baseline.py`
  - `time_series_models.py`
  - `ml_models.py`

- **`/visualization`**: Fun├º├╡es para criar visualiza├º├╡es
  - `eda_plots.py`
  - `time_series_plots.py`
  - `dashboard.py`

### `/reports`
Sa├¡das e resultados das an├ílises:

- **`/figures`**: Gr├íficos e visualiza├º├╡es exportadas
- **`/insights`**: Documentos com descobertas e insights

### `/tests`
Testes automatizados para garantir qualidade do c├│digo:

- `test_data_loading.py`
- `test_feature_engineering.py`
- `test_models.py`

### `/config`
Arquivos de configura├º├úo:

- `config.yaml` - Configura├º├╡es principais do projeto

## ≡ƒôä Arquivos na Raiz

- **`README.md`**: Documenta├º├úo principal do projeto
- **`requirements.txt`**: Depend├¬ncias Python
- **`.gitignore`**: Arquivos ignorados pelo Git
- **`.env.example`**: Exemplo de vari├íveis de ambiente
- **`STRUCTURE.md`**: Este arquivo (guia de estrutura)

## ≡ƒÜÇ Workflow Recomendado

### 1. Prepara├º├úo Inicial
```bash
# 1. Clonar/configurar reposit├│rio
# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar depend├¬ncias
pip install -r requirements.txt

# 4. Colocar CSVs em data/raw/
```

### 2. Explora├º├úo
```bash
# Explorar dados em notebooks/01_exploracao/
jupyter notebook notebooks/01_exploracao/ecommerce_eda.ipynb
```

### 3. Limpeza
```bash
# Limpar dados em notebooks/02_limpeza/
# Ou executar scripts:
python src/data/load_ecommerce.py
python src/data/load_retail.py
python src/data/load_sales_data.py
```

### 4. Feature Engineering
```bash
# Criar features em notebooks/03_feature_engineering/
# Ou executar script:
python src/features/build_features.py
```

### 5. Modelagem
```bash
# Desenvolver modelos em notebooks/04_modelagem/
jupyter notebook notebooks/04_modelagem/time_series_forecast.ipynb
```

### 6. Testes
```bash
# Executar testes
pytest tests/
```

## ≡ƒÄ» Boas Pr├íticas

1. **Nunca editar dados em `/data/raw`** - sempre trabalhe com c├│pias em `/data/processed`

2. **Notebooks numerados** - facilita entender a ordem de execu├º├úo

3. **C├│digo reutiliz├ível em `/src`** - notebooks devem importar fun├º├╡es de `/src`

4. **Commitar notebooks limpos** - limpe outputs antes de commitar

5. **Usar `.gitignore`** - n├úo versionar dados grandes ou arquivos tempor├írios

6. **Documentar decis├╡es** - anote descobertas em `/reports/insights`

7. **Configura├º├╡es em arquivo** - use `config/config.yaml` em vez de hardcode

8. **Versionamento de modelos** - salve modelos treinados com timestamp

## ≡ƒôè Fluxo de Dados

```
Raw Data (CSV)
    Γåô
[Limpeza & Valida├º├úo] ΓåÆ src/data/
    Γåô
Processed Data (Parquet)
    Γåô
[Feature Engineering] ΓåÆ src/features/
    Γåô
Features Dataset
    Γåô
[Modelagem] ΓåÆ src/models/
    Γåô
Modelo Treinado + Previs├╡es
    Γåô
[Visualiza├º├úo] ΓåÆ src/visualization/
    Γåô
Reports & Dashboards
```

## ≡ƒöº Personaliza├º├úo

Esta estrutura ├⌐ um template. Sinta-se livre para:

- Adicionar novas pastas conforme necess├írio
- Criar subm├│dulos em `/src` para organizar melhor
- Adicionar novos notebooks para an├ílises espec├¡ficas
- Expandir `/config` com m├║ltiplos arquivos de configura├º├úo

## ≡ƒôÜ Pr├│ximos Passos

1. [ ] Colocar arquivos CSV em `data/raw/`
2. [ ] Executar notebooks de explora├º├úo
3. [ ] Implementar scripts de limpeza
4. [ ] Desenvolver pipeline de features
5. [ ] Treinar modelos baseline
6. [ ] Criar visualiza├º├╡es
7. [ ] Documentar insights

