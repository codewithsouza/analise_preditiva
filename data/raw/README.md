# ≡ƒôª Dados Brutos (Raw Data)

Esta pasta deve conter os arquivos CSV originais. **Nunca modifique arquivos nesta pasta!**

## Arquivos Esperados

### 1. Updated_sales.csv
Dataset de e-commerce com transa├º├╡es individuais.

**Estrutura esperada:**
- Order ID
- Product
- Quantity Ordered
- Price Each
- Order Date
- Purchase Address

### 2. Retail and wherehouse Sale.csv
Dataset de vendas de varejo e warehouse agregadas por m├¬s (ano 2020).

**Estrutura esperada:**
- YEAR
- MONTH
- SUPPLIER
- ITEM CODE
- ITEM DESCRIPTION
- ITEM TYPE
- RETAIL SALES
- RETAIL TRANSFERS
- WAREHOUSE SALES

### 3. Sales_Data/ (pasta)
M├║ltiplos arquivos CSV mensais com transa├º├╡es.

**Arquivos esperados:**
- Sales_April_2019.csv
- Sales_May_2019.csv
- Sales_June_2019.csv
- ... (um arquivo por m├¬s)

**Estrutura de cada arquivo:**
- Order ID
- Product
- Quantity Ordered
- Price Each
- Order Date
- Purchase Address

## ΓÜá∩╕Å Avisos Importantes

1. **N├úo modifique**: Mantenha os arquivos originais intactos
2. **Backup**: Fa├ºa backup dos arquivos originais antes de come├ºar
3. **Gitignore**: Estes arquivos n├úo s├úo versionados (veja .gitignore)
4. **Tamanho**: Arquivos grandes podem demorar para carregar

## ≡ƒôÑ Como Obter os Dados

Se voc├¬ n├úo tem os arquivos ainda:

1. **Updated_sales.csv**: [fonte/link aqui]
2. **Retail and wherehouse Sale.csv**: [fonte/link aqui]
3. **Sales_Data/**: [link para reposit├│rio GitHub]

## Γ£à Valida├º├úo

Para verificar se seus arquivos est├úo corretos:

```python
import pandas as pd
from pathlib import Path

# Verificar Updated_sales.csv
path1 = Path("data/raw/Updated_sales.csv")
assert path1.exists(), "Updated_sales.csv n├úo encontrado!"
df1 = pd.read_csv(path1, nrows=5)
print("Γ£à Updated_sales.csv OK")
print(df1.columns.tolist())

# Verificar Retail and wherehouse Sale.csv
path2 = Path("data/raw/Retail and wherehouse Sale.csv")
assert path2.exists(), "Retail and wherehouse Sale.csv n├úo encontrado!"
df2 = pd.read_csv(path2, nrows=5)
print("Γ£à Retail and wherehouse Sale.csv OK")
print(df2.columns.tolist())

# Verificar Sales_Data/
sales_dir = Path("data/raw/Sales_Data")
assert sales_dir.exists(), "Pasta Sales_Data n├úo encontrada!"
csv_files = list(sales_dir.glob("*.csv"))
print(f"Γ£à {len(csv_files)} arquivos CSV encontrados em Sales_Data/")
```

## ≡ƒöì Informa├º├╡es Adicionais

**Encoding**: Geralmente UTF-8, mas pode ser necess├írio usar latin-1 ou cp1252

**Separador**: V├¡rgula (,)

**Decimal**: Ponto (.)

**Datas**: Formato MM/DD/YY

