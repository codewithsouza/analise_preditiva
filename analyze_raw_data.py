"""Analisa os datasets dispon├¡veis em data/raw/"""

import pandas as pd
from pathlib import Path
import sys

# Configurar encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("="*70)
print("ANALISE DOS DATASETS")
print("="*70)

# 1. UPDATED_SALES.CSV
print("\n1. UPDATED_SALES.CSV (E-commerce)")
print("-"*70)
try:
    path1 = Path("data/raw/Updated_sales.csv")
    df1 = pd.read_csv(path1)
    
    print(f"Linhas: {len(df1):,}")
    print(f"Colunas: {len(df1.columns)}")
    print(f"Colunas: {df1.columns.tolist()}")
    print(f"\nPrimeiras 3 linhas:")
    print(df1.head(3).to_string())
    print(f"\nTipos de dados:")
    print(df1.dtypes.to_string())
    print(f"\nValores nulos:")
    print(df1.isnull().sum().to_string())
    
except Exception as e:
    print(f"[ERRO] {e}")

# 2. RETAIL AND WHEREHOUSE SALE.CSV
print("\n\n2. RETAIL AND WHEREHOUSE SALE.CSV")
print("-"*70)
try:
    path2 = Path("data/raw/Retail and wherehouse Sale.csv")
    df2 = pd.read_csv(path2)
    
    print(f"Linhas: {len(df2):,}")
    print(f"Colunas: {len(df2.columns)}")
    print(f"Colunas: {df2.columns.tolist()}")
    print(f"\nPrimeiras 3 linhas:")
    print(df2.head(3).to_string())
    print(f"\nTipos de dados:")
    print(df2.dtypes.to_string())
    print(f"\nValores nulos:")
    print(df2.isnull().sum().to_string())
    
except Exception as e:
    print(f"[ERRO] {e}")

print("\n" + "="*70)
print("CONCLUSAO")
print("="*70)
print("\nVoce tem 2 datasets principais:")
print("  1. Updated_sales.csv - Dataset de e-commerce (transacoes)")
print("  2. Retail and wherehouse Sale.csv - Dataset de varejo/warehouse")
print("\nA pasta Sales_Data/ esta vazia - nao precisa dela!")
print("\nRECOMENDACOES:")
print("  - Comece explorando Updated_sales.csv")
print("  - Use o notebook: notebooks/01_exploracao/ecommerce_eda.ipynb")
print("="*70)

