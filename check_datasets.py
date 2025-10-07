"""
Script para verificar se Updated_sales.csv ├⌐ consolida├º├úo de Sales_Data/
ou se s├úo datasets diferentes.
"""

import pandas as pd
from pathlib import Path
import sys

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("VERIFICANDO DATASETS...\n")

# Caminhos
updated_path = Path("data/raw/Updated_sales.csv")
sales_data_dir = Path("data/raw/Sales_Data")

# 1. Verificar se os arquivos existem
print("Verificando arquivos...")
if updated_path.exists():
    print(f"  [OK] Updated_sales.csv encontrado")
else:
    print(f"  [X] Updated_sales.csv NAO encontrado em {updated_path}")

if sales_data_dir.exists():
    csv_files = list(sales_data_dir.glob("*.csv"))
    print(f"  [OK] Sales_Data/ encontrado com {len(csv_files)} arquivos CSV")
    if csv_files:
        print(f"     Exemplos: {', '.join([f.name for f in csv_files[:3]])}")
else:
    print(f"  [X] Sales_Data/ NAO encontrado em {sales_data_dir}")

print("\n" + "="*70)

# 2. Se ambos existem, comparar
if updated_path.exists() and sales_data_dir.exists() and csv_files:
    print("\nCOMPARANDO DATASETS...\n")
    
    # Ler Updated_sales.csv
    try:
        df_updated = pd.read_csv(updated_path, nrows=5)
        print(f"[OK] Updated_sales.csv:")
        print(f"   Colunas: {df_updated.columns.tolist()}")
        print(f"   Total de linhas: {len(pd.read_csv(updated_path))}")
        updated_full = pd.read_csv(updated_path)
    except Exception as e:
        print(f"[ERRO] ao ler Updated_sales.csv: {e}")
        updated_full = None
    
    print("\n" + "-"*70)
    
    # Ler primeiro arquivo de Sales_Data
    try:
        first_file = csv_files[0]
        df_sales = pd.read_csv(first_file, nrows=5)
        print(f"\n[OK] {first_file.name}:")
        print(f"   Colunas: {df_sales.columns.tolist()}")
        
        # Contar total de linhas em todos os arquivos
        total_lines = 0
        for f in csv_files:
            total_lines += len(pd.read_csv(f))
        print(f"   Total de linhas (todos os CSVs): {total_lines}")
        
    except Exception as e:
        print(f"[ERRO] ao ler Sales_Data: {e}")
    
    print("\n" + "="*70)
    print("\nANALISE:\n")
    
    # Comparar colunas
    if df_updated.columns.tolist() == df_sales.columns.tolist():
        print("[OK] As colunas sao IDENTICAS")
    else:
        print("[!] As colunas sao DIFERENTES")
    
    # Comparar n├║mero de linhas
    if updated_full is not None:
        if len(updated_full) == total_lines:
            print("[OK] Numero de linhas e IGUAL - Provavelmente sao os MESMOS dados!")
            print("\nRECOMENDACAO: Use APENAS Updated_sales.csv (ja esta consolidado)")
        elif len(updated_full) > total_lines:
            print(f"[!] Updated_sales.csv tem MAIS linhas ({len(updated_full)} vs {total_lines})")
            print("\nRECOMENDACAO: Use Updated_sales.csv (parece mais completo)")
        else:
            print(f"[!] Sales_Data/ tem MAIS linhas ({total_lines} vs {len(updated_full)})")
            print("\nRECOMENDACAO: Use Sales_Data/ e consolide os arquivos")
    
else:
    print("\n[!] Adicione os arquivos CSV para fazer a comparacao!")
    print("\nColoque:")
    print("  - Updated_sales.csv em data/raw/")
    print("  - Arquivos mensais em data/raw/Sales_Data/")

print("\n" + "="*70)
print("\n[OK] Verificacao concluida!")

