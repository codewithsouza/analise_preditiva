# ≡ƒÜÇ Guia R├ípido de In├¡cio

Este guia ir├í te ajudar a come├ºar com o projeto em poucos minutos.

## ΓÜí Setup R├ípido (5 minutos)

### 1. Preparar Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Instalar depend├¬ncias
pip install -r requirements.txt
```

### 2. Organizar Dados

Coloque seus arquivos CSV na pasta `data/raw/`:

```
data/raw/
Γö£ΓöÇΓöÇ Updated_sales.csv
Γö£ΓöÇΓöÇ Retail and wherehouse Sale.csv
ΓööΓöÇΓöÇ Sales_Data/
    Γö£ΓöÇΓöÇ Sales_April_2019.csv
    Γö£ΓöÇΓöÇ Sales_May_2019.csv
    ΓööΓöÇΓöÇ ... (outros meses)
```

### 3. Come├ºar a Explorar

```bash
# Iniciar Jupyter Notebook
jupyter notebook

# Abrir um dos notebooks de explora├º├úo:
# notebooks/01_exploracao/ecommerce_eda.ipynb
```

## ≡ƒôè Fluxo de Trabalho T├¡pico

### Op├º├úo A: Usar Notebooks (Recomendado para Iniciantes)

1. **Explora├º├úo**: `notebooks/01_exploracao/`
   - Abra os notebooks de EDA
   - Execute c├⌐lula por c├⌐lula
   - Entenda seus dados

2. **Limpeza**: `notebooks/02_limpeza/`
   - Limpe e valide dados
   - Exporte para `data/processed/`

3. **Features**: `notebooks/03_feature_engineering/`
   - Crie features temporais e geogr├íficas
   - Salve dataset final

4. **Modelagem**: `notebooks/04_modelagem/`
   - Treine modelos
   - Avalie resultados

### Op├º├úo B: Usar Scripts Python

```bash
# 1. Carregar e limpar dados
python src/data/load_ecommerce.py
python src/data/load_retail.py
python src/data/load_sales_data.py

# 2. Criar features
python src/features/build_features.py

# 3. Treinar modelo
python src/models/train.py

# 4. Ver resultados
python src/visualization/dashboard.py
```

## ≡ƒöì Exemplo M├¡nimo de Uso

Aqui est├í um exemplo b├ísico para come├ºar:

### Python Script

```python
import pandas as pd
from pathlib import Path

# Carregar dados
df = pd.read_csv("data/raw/Updated_sales.csv", 
                 parse_dates=["Order Date"])

# Ver primeiras linhas
print(df.head())

# Estat├¡sticas b├ísicas
print(df.describe())

# Criar feature de receita
df["Revenue"] = df["Quantity Ordered"] * df["Price Each"]

# Vendas por m├¬s
monthly_sales = df.groupby(df["Order Date"].dt.month)["Revenue"].sum()
print(monthly_sales)

# Salvar processado
df.to_parquet("data/processed/ecommerce_clean.parquet")
```

### Jupyter Notebook

```python
# C├⌐lula 1: Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# C├⌐lula 2: Carregar dados
df = pd.read_csv("data/raw/Updated_sales.csv", 
                 parse_dates=["Order Date"])

# C├⌐lula 3: Explorar
df.info()
df.head()

# C├⌐lula 4: Visualizar
df.groupby(df["Order Date"].dt.month)["Revenue"].sum().plot(kind="bar")
plt.title("Vendas por M├¬s")
plt.show()
```

## ≡ƒÄ» Checklist Primeira Execu├º├úo

- [ ] Ambiente virtual criado e ativado
- [ ] Depend├¬ncias instaladas (`pip install -r requirements.txt`)
- [ ] Arquivos CSV em `data/raw/`
- [ ] Jupyter Notebook funcionando
- [ ] Primeiro notebook de explora├º├úo executado
- [ ] Dados b├ísicos entendidos

## ≡ƒåÿ Problemas Comuns

### Erro de Encoding

```python
# Tente encoding diferente
df = pd.read_csv("arquivo.csv", encoding="latin-1")
# ou
df = pd.read_csv("arquivo.csv", encoding="cp1252")
```

### Jupyter N├úo Encontra M├│dulos

```bash
# Instalar kernel do Jupyter no ambiente virtual
python -m ipykernel install --user --name=analise-preditiva
```

### Mem├│ria Insuficiente

```python
# Ler em chunks
chunks = pd.read_csv("arquivo_grande.csv", chunksize=100000)
df = pd.concat([chunk for chunk in chunks])
```

## ≡ƒôÜ Pr├│ximos Passos

Depois de completar o setup:

1. Γ£à Leia o [README.md](README.md) completo
2. Γ£à Explore [STRUCTURE.md](STRUCTURE.md) para entender organiza├º├úo
3. Γ£à Execute notebooks de explora├º├úo
4. Γ£à Adapte o c├│digo para suas necessidades
5. Γ£à Crie seus pr├│prios notebooks de an├ílise

## ≡ƒÆí Dicas

- **Salve com frequ├¬ncia**: Notebooks podem perder trabalho n├úo salvo
- **Use Ctrl+Enter**: Para executar c├⌐lula sem avan├ºar
- **Use Shift+Enter**: Para executar e avan├ºar para pr├│xima c├⌐lula
- **Reinicie kernel**: Se algo n├úo funcionar (Kernel > Restart)
- **Limpe outputs**: Antes de commitar (Cell > All Output > Clear)

## ≡ƒöù Recursos ├Üteis

- [Documenta├º├úo Pandas](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Scikit-learn Examples](https://scikit-learn.org/stable/auto_examples/)
- [Jupyter Notebook Tips](https://jupyter-notebook.readthedocs.io/)

---

Pronto! Voc├¬ est├í preparado para come├ºar sua an├ílise preditiva! ≡ƒÄë

