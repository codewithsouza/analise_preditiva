"""
Script r├ípido para converter arquivos Parquet em Excel/CSV.
Execute: python convert_to_excel.py
"""

import pandas as pd
from pathlib import Path

print("="*70)
print("CONVERTENDO PARQUET PARA EXCEL/CSV")
print("="*70)

processed_dir = Path("data/processed")

# Lista de arquivos parquet
parquet_files = [
    "ecommerce_clean.parquet",
    "ecommerce_daily_ts.parquet",
    "ecommerce_monthly_ts.parquet"
]

for parquet_file in parquet_files:
    parquet_path = processed_dir / parquet_file
    
    if not parquet_path.exists():
        print(f"\n[AVISO] {parquet_file} nao encontrado, pulando...")
        continue
    
    print(f"\nConvertendo {parquet_file}...")
    
    # Ler parquet
    df = pd.read_parquet(parquet_path)
    print(f"   Linhas: {df.shape[0]:,} | Colunas: {df.shape[1]}")
    
    # Nome base sem extens├úo
    base_name = parquet_file.replace(".parquet", "")
    
    # Salvar em Excel
    excel_path = processed_dir / f"{base_name}.xlsx"
    df.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"   [OK] Excel: {excel_path}")
    
    # Salvar em CSV
    csv_path = processed_dir / f"{base_name}.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"   [OK] CSV: {csv_path}")

print("\n" + "="*70)
print("[SUCESSO] CONVERSAO CONCLUIDA!")
print("="*70)
print("\nArquivos Excel e CSV estao em: data/processed/")
print("\nVoce pode abrir os arquivos .xlsx ou .csv diretamente no Excel.")
print("\nPara gerar tambem as previsoes (predictions_rf.csv, etc):")
print("   Execute: python run_modeling.py")

