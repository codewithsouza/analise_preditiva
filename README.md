📊 Análise Preditiva de Vendas

Projeto de análise e previsão de vendas utilizando três fontes de dados distintas: e-commerce, varejo/warehouse e vendas históricas mensais.

🧩 Estrutura do Projeto
analise-preditiva/
│
├── data/
│   ├── raw/                    # Dados brutos originais
│   ├── processed/              # Dados processados e limpos
│   └── external/               # Dados externos complementares
│
├── notebooks/
│   ├── 01_exploracao/          # Análise exploratória
│   ├── 02_limpeza/             # Limpeza e preparação
│   ├── 03_feature_engineering/ # Criação de features
│   └── 04_modelagem/           # Modelos preditivos
│
├── src/
│   ├── data/                   # Scripts de carregamento
│   ├── features/               # Transformações de dados
│   ├── models/                 # Modelos e treinamento
│   └── visualization/          # Visualizações
│
├── reports/
│   ├── figures/                # Gráficos e visualizações
│   └── insights/               # Documentação de descobertas
│
├── tests/                      # Testes automatizados
└── config/                     # Arquivos de configuração

🗂️ Datasets
1. Updated_sales.csv (E-commerce)

Colunas: Order ID, Product, Quantity Ordered, Price Each, Order Date, Purchase Address

Período: Dados transacionais de e-commerce

Features Derivadas: Revenue, Month, Day, Hour, City, State, Zip

2. Retail and Warehouse Sale.csv (Varejo/Warehouse 2020)

Colunas: YEAR, MONTH, SUPPLIER, ITEM CODE, ITEM DESCRIPTION, ITEM TYPE, RETAIL SALES, RETAIL TRANSFERS, WAREHOUSE SALES

Período: Ano 2020

Features Derivadas: DATE (primeiro dia do mês)

3. Sales_Data/ (Vendas Mensais)

Formato: Múltiplos arquivos CSV por mês

Colunas: Order ID, Product, Quantity Ordered, Price Each, Order Date, Purchase Address

Notas: Contém linhas de cabeçalho repetidas que precisam ser removidas

⚙️ Como Usar
1. Preparação do Ambiente
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt

2. Organização dos Dados

Coloque seus arquivos CSV em:

data/raw/Updated_sales.csv
data/raw/Retail and wherehouse Sale.csv
data/raw/Sales_Data/*.csv

3. Execução do Pipeline
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

📈 Análises Disponíveis

✅ Análise exploratória de dados (EDA)

✅ Limpeza e validação de dados

✅ Feature engineering temporal e geográfico

✅ Análise de tendências e sazonalidade

✅ Previsão de vendas (time series)

✅ Segmentação de produtos

✅ Análise de performance por região

🧠 Tecnologias

Python 3.9+

Pandas, NumPy

Matplotlib, Seaborn, Plotly

Scikit-learn

Prophet / ARIMA (previsão)

Jupyter Notebook
