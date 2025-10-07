# ≡ƒôè An├ílise Preditiva de Vendas

Projeto de an├ílise e previs├úo de vendas utilizando tr├¬s fontes de dados distintas: e-commerce, varejo/warehouse e vendas hist├│ricas mensais.

## ≡ƒôü Estrutura do Projeto

```
analise-preditiva/
Γö£ΓöÇΓöÇ data/
Γöé   Γö£ΓöÇΓöÇ raw/                    # Dados brutos originais
Γöé   Γö£ΓöÇΓöÇ processed/              # Dados processados e limpos
Γöé   ΓööΓöÇΓöÇ external/               # Dados externos complementares
Γö£ΓöÇΓöÇ notebooks/
Γöé   Γö£ΓöÇΓöÇ 01_exploracao/          # An├ílise explorat├│ria
Γöé   Γö£ΓöÇΓöÇ 02_limpeza/             # Limpeza e prepara├º├úo
Γöé   Γö£ΓöÇΓöÇ 03_feature_engineering/ # Cria├º├úo de features
Γöé   ΓööΓöÇΓöÇ 04_modelagem/           # Modelos preditivos
Γö£ΓöÇΓöÇ src/
Γöé   Γö£ΓöÇΓöÇ data/                   # Scripts de carregamento
Γöé   Γö£ΓöÇΓöÇ features/               # Transforma├º├╡es de dados
Γöé   Γö£ΓöÇΓöÇ models/                 # Modelos e treinamento
Γöé   ΓööΓöÇΓöÇ visualization/          # Visualiza├º├╡es
Γö£ΓöÇΓöÇ reports/
Γöé   Γö£ΓöÇΓöÇ figures/                # Gr├íficos e visualiza├º├╡es
Γöé   ΓööΓöÇΓöÇ insights/               # Documenta├º├úo de descobertas
Γö£ΓöÇΓöÇ tests/                      # Testes automatizados
ΓööΓöÇΓöÇ config/                     # Arquivos de configura├º├úo

```

## ≡ƒôï Datasets

### 1. Updated_sales.csv (E-commerce)
- **Colunas**: Order ID, Product, Quantity Ordered, Price Each, Order Date, Purchase Address
- **Per├¡odo**: Dados transacionais de e-commerce
- **Features Derivadas**: Revenue, Month, Day, Hour, City, State, Zip

### 2. Retail and wherehouse Sale.csv (Varejo/Warehouse 2020)
- **Colunas**: YEAR, MONTH, SUPPLIER, ITEM CODE, ITEM DESCRIPTION, ITEM TYPE, RETAIL SALES, RETAIL TRANSFERS, WAREHOUSE SALES
- **Per├¡odo**: Ano 2020
- **Features Derivadas**: DATE (primeiro dia do m├¬s)

### 3. Sales_Data/ (Vendas Mensais)
- **Formato**: M├║ltiplos arquivos CSV por m├¬s
- **Colunas**: Order ID, Product, Quantity Ordered, Price Each, Order Date, Purchase Address
- **Notas**: Cont├⌐m linhas de cabe├ºalho repetidas que precisam ser removidas

## ≡ƒÜÇ Como Usar

### 1. Prepara├º├úo do Ambiente
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Organizar os Dados
Coloque seus arquivos CSV em:
- `data/raw/Updated_sales.csv`
- `data/raw/Retail and wherehouse Sale.csv`
- `data/raw/Sales_Data/*.csv`

### 3. Executar Pipeline
```bash
# Carregar e limpar dados
python src/data/load_ecommerce.py
python src/data/load_retail.py
python src/data/load_sales_data.py

# Explorar dados
jupyter notebook notebooks/01_exploracao/

# Feature engineering
python src/features/build_features.py

# Modelagem preditiva
jupyter notebook notebooks/04_modelagem/
```

## ≡ƒôè An├ílises Dispon├¡veis

- Γ£à An├ílise explorat├│ria de dados (EDA)
- Γ£à Limpeza e valida├º├úo de dados
- Γ£à Feature engineering temporal e geogr├ífico
- Γ£à An├ílise de tend├¬ncias e sazonalidade
- Γ£à Previs├úo de vendas (time series)
- Γ£à Segmenta├º├úo de produtos
- Γ£à An├ílise de performance por regi├úo

## ≡ƒöº Tecnologias

- Python 3.9+
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Scikit-learn
- Prophet / ARIMA (previs├úo)
- Jupyter Notebook

## ≡ƒôê Pr├│ximos Passos

1. Implementar valida├º├úo de qualidade de dados
2. Criar dashboard interativo
3. Automatizar pipeline de dados
4. Deploy do modelo preditivo

## ≡ƒæÑ Contribui├º├╡es

Projeto em desenvolvimento.

## ≡ƒô¥ Licen├ºa

Uso interno/educacional.

