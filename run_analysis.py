"""
Script para executar an├ílise explorat├│ria do e-commerce.
Execute: python run_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# Configura├º├╡es
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

print("="*70)
print("AN├üLISE EXPLORAT├ôRIA - E-COMMERCE")
print("="*70)

# ===== CARREGAMENTO =====
print("\n1. Carregando dados...")

# Verificar se existe pasta Sales_Data com m├║ltiplos arquivos
sales_data_dir = Path("data/raw/Sales_Data")
all_dfs = []

if sales_data_dir.exists():
    print("\n   Carregando todos os arquivos de Sales_Data...")
    sales_files = list(sales_data_dir.glob("Sales_*.csv"))
    
    if sales_files:
        for file in sorted(sales_files):
            print(f"   - {file.name}")
            df_temp = pd.read_csv(
                file,
                dtype=str,
                encoding="utf-8",
                na_values=["", "NA", "NaN", "null"]
            )
            all_dfs.append(df_temp)
        
        # Combinar todos os arquivos
        df_ecom = pd.concat(all_dfs, ignore_index=True)
        print(f"\n   Total de {len(sales_files)} arquivos combinados")
    else:
        # Se n├úo houver arquivos, usar Updated_sales.csv
        print("   Nenhum arquivo Sales_*.csv encontrado, usando Updated_sales.csv")
        df_ecom = pd.read_csv(
            Path("data/raw/Updated_sales.csv"),
            dtype=str,
            encoding="utf-8",
            na_values=["", "NA", "NaN", "null"]
        )
else:
    # Se pasta n├úo existir, usar Updated_sales.csv
    print("   Pasta Sales_Data n├úo encontrada, usando Updated_sales.csv")
    df_ecom = pd.read_csv(
        Path("data/raw/Updated_sales.csv"),
        dtype=str,
        encoding="utf-8",
        na_values=["", "NA", "NaN", "null"]
    )

print(f"\n   Linhas brutas: {df_ecom.shape[0]:,}")

# Remover linhas de cabe├ºalho duplicadas (quando "Quantity Ordered" == "Quantity Ordered")
if "Quantity Ordered" in df_ecom.columns:
    mask_header = df_ecom["Quantity Ordered"] == "Quantity Ordered"
    num_bad = mask_header.sum()
    df_ecom = df_ecom[~mask_header].copy()
    print(f"   Linhas de cabe├ºalho duplicadas removidas: {num_bad}")

# Agora converter para tipos corretos
df_ecom["Order ID"] = pd.to_numeric(df_ecom["Order ID"], errors="coerce").astype("Int64")
df_ecom["Quantity Ordered"] = pd.to_numeric(df_ecom["Quantity Ordered"], errors="coerce").astype("Int64")
df_ecom["Price Each"] = pd.to_numeric(df_ecom["Price Each"], errors="coerce").astype("float64")
df_ecom["Order Date"] = pd.to_datetime(df_ecom["Order Date"], errors="coerce")
df_ecom["Product"] = df_ecom["Product"].astype("string")
df_ecom["Purchase Address"] = df_ecom["Purchase Address"].astype("string")

print(f"[OK] Dataset carregado: {df_ecom.shape[0]:,} linhas x {df_ecom.shape[1]} colunas")

# ===== LIMPEZA =====
print("\n2. Limpando dados...")
print(f"   Linhas com valores nulos: {df_ecom.isnull().any(axis=1).sum()}")
df_ecom_clean = df_ecom.dropna()
print(f"[OK] Dataset limpo: {df_ecom_clean.shape[0]:,} linhas")

# ===== FEATURE ENGINEERING =====
print("\n3. Criando features...")
df_ecom_clean["Revenue"] = df_ecom_clean["Quantity Ordered"] * df_ecom_clean["Price Each"]
df_ecom_clean["Month"] = df_ecom_clean["Order Date"].dt.month
df_ecom_clean["Day"] = df_ecom_clean["Order Date"].dt.day
df_ecom_clean["Hour"] = df_ecom_clean["Order Date"].dt.hour
df_ecom_clean["DayOfWeek"] = df_ecom_clean["Order Date"].dt.dayofweek

# Extrair cidade/estado/cep
parts = df_ecom_clean["Purchase Address"].str.split(",", expand=True)
df_ecom_clean["City"] = parts[1].str.strip()
state_zip = parts[2].str.strip().str.split(" ", n=1, expand=True)
df_ecom_clean["State"] = state_zip[0]
df_ecom_clean["Zip"] = state_zip[1]

print("[OK] Features criadas: Revenue, Month, Hour, City, State, Zip")

# ===== ESTAT├ìSTICAS =====
print("\n4. Estat├¡sticas Descritivas:")
print("="*70)
print(f"Receita Total: ${df_ecom_clean['Revenue'].sum():,.2f}")
print(f"Ticket M├⌐dio: ${df_ecom_clean['Revenue'].mean():,.2f}")
print(f"N├║mero de Pedidos: {df_ecom_clean['Order ID'].nunique():,}")
print(f"Produtos ├Ünicos: {df_ecom_clean['Product'].nunique()}")
print(f"Cidades: {df_ecom_clean['City'].nunique()}")

# ===== TOP PRODUTOS =====
print("\n5. Top 10 Produtos por Receita:")
print("="*70)
top_products = df_ecom_clean.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(10)
for i, (prod, rev) in enumerate(top_products.items(), 1):
    print(f"{i:2}. {prod:40s} ${rev:>12,.2f}")

# ===== VENDAS POR M├èS =====
print("\n6. Vendas por M├¬s:")
print("="*70)
monthly_sales = df_ecom_clean.groupby("Month").agg({
    "Revenue": "sum",
    "Order ID": "count"
})
monthly_sales.columns = ["Receita", "Pedidos"]
print(monthly_sales)

# ===== VENDAS POR CIDADE =====
print("\n7. Top 5 Cidades por Receita:")
print("="*70)
city_sales = df_ecom_clean.groupby("City")["Revenue"].sum().sort_values(ascending=False).head(5)
for i, (city, rev) in enumerate(city_sales.items(), 1):
    print(f"{i}. {city:20s} ${rev:>12,.2f}")

# ===== PREPARAR S├ëRIES TEMPORAIS =====
print("\n8. Preparando dados para modelagem...")
ts_daily = df_ecom_clean.groupby(df_ecom_clean["Order Date"].dt.date).agg({
    "Revenue": "sum",
    "Order ID": "count",
    "Quantity Ordered": "sum"
}).reset_index()
ts_daily.columns = ["Date", "Revenue", "Orders", "Quantity"]
ts_daily["Date"] = pd.to_datetime(ts_daily["Date"])

ts_monthly = df_ecom_clean.groupby(df_ecom_clean["Order Date"].dt.to_period("M")).agg({
    "Revenue": "sum",
    "Order ID": "count",
    "Quantity Ordered": "sum"
}).reset_index()
ts_monthly.columns = ["Month", "Revenue", "Orders", "Quantity"]
ts_monthly["Month"] = ts_monthly["Month"].dt.to_timestamp()

# ===== EXPORTAR =====
print("\n9. Exportando dados processados...")
output_path_clean = Path("data/processed/ecommerce_clean.parquet")
output_path_daily = Path("data/processed/ecommerce_daily_ts.parquet")
output_path_monthly = Path("data/processed/ecommerce_monthly_ts.parquet")

output_path_clean.parent.mkdir(parents=True, exist_ok=True)

# Salvar em Parquet (mais eficiente)
df_ecom_clean.to_parquet(output_path_clean, index=False)
ts_daily.to_parquet(output_path_daily, index=False)
ts_monthly.to_parquet(output_path_monthly, index=False)

print(f"[OK] {output_path_clean}")
print(f"[OK] {output_path_daily}")
print(f"[OK] {output_path_monthly}")

# Salvar em Excel/CSV (para abrir no Excel)
print("\n   Exportando tamb├⌐m em formatos Excel...")
excel_path_clean = Path("data/processed/ecommerce_clean.xlsx")
csv_path_clean = Path("data/processed/ecommerce_clean.csv")
csv_path_monthly = Path("data/processed/ecommerce_monthly_ts.csv")

df_ecom_clean.to_excel(excel_path_clean, index=False, engine='openpyxl')
df_ecom_clean.to_csv(csv_path_clean, index=False, encoding='utf-8-sig')
ts_monthly.to_csv(csv_path_monthly, index=False, encoding='utf-8-sig')

print(f"[OK] {excel_path_clean}")
print(f"[OK] {csv_path_clean}")
print(f"[OK] {csv_path_monthly}")

# ===== GR├üFICOS (OPCIONAL) =====
print("\n10. Gerando gr├íficos...")

# Vendas mensais
fig, ax = plt.subplots(figsize=(12, 6))
monthly_sales["Receita"].plot(kind="bar", ax=ax, color="steelblue", alpha=0.7)
ax.set_title("Receita Total por M├¬s", fontsize=14, fontweight="bold")
ax.set_xlabel("M├¬s")
ax.set_ylabel("Receita ($)")
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig("reports/figures/vendas_mensais.png", dpi=150, bbox_inches='tight')
print("[OK] Salvo: reports/figures/vendas_mensais.png")
plt.close()

# Top produtos
fig, ax = plt.subplots(figsize=(12, 8))
top_products.plot(kind="barh", ax=ax, color="coral")
ax.set_title("Top 10 Produtos por Receita", fontsize=14, fontweight="bold")
ax.set_xlabel("Receita ($)")
ax.invert_yaxis()
plt.tight_layout()
plt.savefig("reports/figures/top_produtos.png", dpi=150, bbox_inches='tight')
print("[OK] Salvo: reports/figures/top_produtos.png")
plt.close()

# Evolu├º├úo temporal
fig, ax = plt.subplots(figsize=(16, 6))
daily_rev = df_ecom_clean.groupby(df_ecom_clean["Order Date"].dt.date)["Revenue"].sum()
ax.plot(daily_rev.index, daily_rev.values, linewidth=1.5, color="darkblue", alpha=0.7)
ax.set_title("Evolu├º├úo Di├íria da Receita", fontsize=14, fontweight="bold")
ax.set_xlabel("Data")
ax.set_ylabel("Receita ($)")
plt.xticks(rotation=45)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("reports/figures/evolucao_receita.png", dpi=150, bbox_inches='tight')
print("[OK] Salvo: reports/figures/evolucao_receita.png")
plt.close()

print("\n" + "="*70)
print("[SUCESSO] ANALISE CONCLUIDA COM SUCESSO!")
print("="*70)
print("\nPr├│ximo passo: python run_modeling.py")

