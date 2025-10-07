"""
Script para visualizar resultados da an├ílise de forma clara e organizada.
Execute: python view_results.py
"""

import pandas as pd
from pathlib import Path
import os

def print_section(title):
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70)

def check_file(filepath):
    if Path(filepath).exists():
        size = Path(filepath).stat().st_size
        return f"[OK] {size:,} bytes"
    return "[X] Nao encontrado"

print("="*70)
print("RESULTADOS DA ANALISE PREDITIVA".center(70))
print("="*70)

# ===== ESTRUTURA DE ARQUIVOS =====
print_section("ARQUIVOS GERADOS")

files = {
    "Dados Processados": [
        "data/processed/ecommerce_clean.parquet",
        "data/processed/ecommerce_daily_ts.parquet",
        "data/processed/ecommerce_monthly_ts.parquet",
    ],
    "Previsoes": [
        "data/processed/predictions_rf.csv",
        "data/processed/predictions_sarima.csv",
        "data/processed/model_metrics.csv",
    ],
    "Graficos": [
        "reports/figures/vendas_mensais.png",
        "reports/figures/top_produtos.png",
        "reports/figures/evolucao_receita.png",
    ]
}

for category, file_list in files.items():
    print(f"\n{category}:")
    for f in file_list:
        status = check_file(f)
        print(f"  {status:20s} {f}")

# ===== METRICAS DOS MODELOS =====
metrics_path = Path("data/processed/model_metrics.csv")
if metrics_path.exists():
    print_section("METRICAS DOS MODELOS")
    metrics = pd.read_csv(metrics_path)
    print(metrics.to_string(index=False))

# ===== PREVISOES RANDOM FOREST =====
rf_path = Path("data/processed/predictions_rf.csv")
if rf_path.exists():
    print_section("PREVISOES RANDOM FOREST (Top 10)")
    rf_pred = pd.read_csv(rf_path)
    
    # Top 10 previs├╡es gerais
    top_10 = rf_pred.nlargest(10, "PredRevenue")[["YearMonth", "Product", "City", "State", "PredRevenue"]]
    print("\nMaiores Previsoes de Revenue:")
    for i, row in enumerate(top_10.itertuples(), 1):
        print(f"{i:2}. {row.YearMonth[:7]} | {row.Product[:25]:25s} | {row.City[:15]:15s} | ${row.PredRevenue:>10,.2f}")
    
    # Total por m├¬s
    monthly_total = rf_pred.groupby("YearMonth")["PredRevenue"].sum().sort_index()
    print("\nPrevisao Total por Mes:")
    for month, value in monthly_total.items():
        print(f"  {month[:7]}: ${value:>12,.2f}")

# ===== PREVISOES SARIMA =====
sarima_path = Path("data/processed/predictions_sarima.csv")
if sarima_path.exists():
    print_section("PREVISOES SARIMA (Proximos 6 Meses)")
    sarima_pred = pd.read_csv(sarima_path)
    
    print(f"\n{'Mes':<10} {'Previsao':>15} {'IC Inferior':>15} {'IC Superior':>15}")
    print("-"*60)
    for _, row in sarima_pred.iterrows():
        month = pd.to_datetime(row['Month']).strftime('%Y-%m')
        print(f"{month:<10} ${row['Prediction']:>14,.2f} ${row['Lower_CI']:>14,.2f} ${row['Upper_CI']:>14,.2f}")

# ===== LOCALIZACAO DOS ARQUIVOS =====
print_section("ONDE ESTAO OS ARQUIVOS?")
print(f"\nDiretorio do projeto: {Path.cwd()}")
print(f"\nPara abrir no explorer:")
print(f"  Windows: explorer {Path.cwd()}")
print(f"  OU clique com botao direito em qualquer arquivo no VS Code/Cursor")

print("\nEstrutura completa:")
print("""
analise preditiva/
  data/
    raw/                        (seus CSVs originais)
      Updated_sales.csv
    processed/                  (dados processados)
      ecommerce_clean.parquet
      predictions_rf.csv        <-- PREVISOES RANDOM FOREST
      predictions_sarima.csv    <-- PREVISOES SARIMA
  reports/
    figures/                    (graficos PNG)
      vendas_mensais.png
      top_produtos.png
      evolucao_receita.png
  notebooks/                    (para explorar interativamente)
    01_exploracao/
      ecommerce_eda.ipynb
    04_modelagem/
      ecommerce_predictive_models.ipynb
""")

# ===== PROXIMOS PASSOS =====
print_section("PROXIMOS PASSOS")
print("""
1. VER GRAFICOS:
   - Abra: reports/figures/
   - Visualize os PNGs gerados

2. VER PREVISOES DETALHADAS:
   - Abra: data/processed/predictions_rf.csv (Excel/LibreOffice)
   - Abra: data/processed/predictions_sarima.csv

3. ANALISE INTERATIVA (notebooks):
   - Execute: jupyter notebook
   - Abra: notebooks/01_exploracao/ecommerce_eda.ipynb
   - Abra: notebooks/04_modelagem/ecommerce_predictive_models.ipynb

4. ABRIR PASTA NO EXPLORER:
   - Windows: explorer .
   - Mac: open .
   - Linux: xdg-open .
""")

print("\n" + "="*70)
print("Analise completa! Arquivos disponiveis para visualizacao.".center(70))
print("="*70)

