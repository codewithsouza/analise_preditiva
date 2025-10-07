"""
Script master para executar toda a pipeline de an├ílise.
Execute: python run_all.py

Este script executa:
1. An├ílise explorat├│ria (run_analysis.py)
2. Modelagem preditiva (run_modeling.py)
"""

import subprocess
import sys
from pathlib import Path

print("="*70)
print("PIPELINE COMPLETA DE AN├üLISE PREDITIVA")
print("="*70)

# Verificar se o arquivo de dados existe
data_file = Path("data/raw/Updated_sales.csv")
if not data_file.exists():
    print("\n[ERRO] Arquivo Updated_sales.csv nao encontrado!")
    print(f"   Esperado em: {data_file.absolute()}")
    print("\nColoque o arquivo CSV em data/raw/ e tente novamente.")
    sys.exit(1)

print("\n[OK] Arquivo de dados encontrado")

# ===== ETAPA 1: AN├üLISE EXPLORAT├ôRIA =====
print("\n" + "="*70)
print("ETAPA 1: AN├üLISE EXPLORAT├ôRIA")
print("="*70)

try:
    result = subprocess.run([sys.executable, "run_analysis.py"], 
                          check=True, 
                          capture_output=False)
    print("\n[SUCESSO] Analise exploratoria concluida!")
except subprocess.CalledProcessError as e:
    print(f"\n[ERRO] Erro na analise exploratoria: {e}")
    sys.exit(1)

# ===== ETAPA 2: MODELAGEM PREDITIVA =====
print("\n" + "="*70)
print("ETAPA 2: MODELAGEM PREDITIVA")
print("="*70)

try:
    result = subprocess.run([sys.executable, "run_modeling.py"], 
                          check=True, 
                          capture_output=False)
    print("\n[SUCESSO] Modelagem preditiva concluida!")
except subprocess.CalledProcessError as e:
    print(f"\n[ERRO] Erro na modelagem: {e}")
    sys.exit(1)

# ===== RESUMO FINAL =====
print("\n" + "="*70)
print("[SUCESSO] PIPELINE COMPLETA EXECUTADA COM SUCESSO!")
print("="*70)

print("\nArquivos gerados:")
print("   data/processed/")
print("   Γö£ΓöÇΓöÇ ecommerce_clean.parquet")
print("   Γö£ΓöÇΓöÇ ecommerce_clean.xlsx (para Excel)")
print("   Γö£ΓöÇΓöÇ ecommerce_clean.csv")
print("   Γö£ΓöÇΓöÇ ecommerce_daily_ts.parquet")
print("   Γö£ΓöÇΓöÇ ecommerce_monthly_ts.parquet")
print("   Γö£ΓöÇΓöÇ ecommerce_monthly_ts.csv")
print("   Γö£ΓöÇΓöÇ predictions_rf.csv")
print("   Γö£ΓöÇΓöÇ predictions_sarima.csv")
print("   ΓööΓöÇΓöÇ model_metrics.csv")
print("\n   reports/figures/")
print("   Γö£ΓöÇΓöÇ vendas_mensais.png")
print("   Γö£ΓöÇΓöÇ top_produtos.png")
print("   ΓööΓöÇΓöÇ evolucao_receita.png")

print("\nPara visualizar analises detalhadas com graficos:")
print("   jupyter notebook notebooks/01_exploracao/ecommerce_eda.ipynb")
print("   jupyter notebook notebooks/04_modelagem/ecommerce_predictive_models.ipynb")

print("\n" + "="*70)

