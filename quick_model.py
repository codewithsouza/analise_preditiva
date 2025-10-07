"""
Script SIMPLIFICADO de modelagem - foca em Random Forest que funciona bem.
Execute: python quick_model.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("="*70)
print("MODELAGEM PREDITIVA SIMPLIFICADA - Random Forest")
print("="*70)

# Carregar dados
processed_path = Path("data/processed/ecommerce_clean.parquet")
if not processed_path.exists():
    print("\n[ERRO] Execute primeiro: python run_analysis.py")
    exit(1)

df = pd.read_parquet(processed_path)
df = df.rename(columns={"Order Date": "OrderDate", "Quantity Ordered": "Quantity", "Price Each": "Price"})

print(f"\n[OK] Dados carregados: {df.shape[0]:,} linhas")

# Agregar
agg = (df
       .assign(YearMonth=df["OrderDate"].dt.to_period("M").dt.to_timestamp())
       .groupby(["YearMonth", "Product", "City", "State"], as_index=False)
       .agg(Revenue=("Revenue", "sum"), AvgPrice=("Price", "mean"))
)
agg["YM_year"] = agg["YearMonth"].dt.year
agg["YM_month"] = agg["YearMonth"].dt.month

# Split
cutoff = agg["YearMonth"].quantile(0.8)
train = agg[agg["YearMonth"] < cutoff].copy()
test = agg[agg["YearMonth"] >= cutoff].copy()

features_cols = ["Product", "City", "State", "YM_year", "YM_month", "AvgPrice"]
X_train, y_train = train[features_cols], train["Revenue"]
X_test, y_test = test[features_cols], test["Revenue"]

print(f"[OK] Treino: {len(train)} | Teste: {len(test)}")

# Treinar modelo
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["Product", "City", "State"]),
    ("num", "passthrough", ["YM_year", "YM_month", "AvgPrice"])
])

rf = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
pipe = Pipeline([("prep", preprocessor), ("model", rf)])

print("\n[TREINANDO...]")
start = time.time()
pipe.fit(X_train, y_train)
print(f"[OK] Treinado em {time.time()-start:.2f}s")

# Avaliar
pred = pipe.predict(X_test)
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)

print("\n" + "="*70)
print("RESULTADOS")
print("="*70)
print(f"MAE:  ${mae:,.2f}")
print(f"RMSE: ${rmse:,.2f}")
print(f"R┬▓:   {r2:.3f}")

# Previs├╡es futuras (3 meses)
last_date = agg["YearMonth"].max()
future_months = pd.period_range(last_date + pd.DateOffset(months=1), periods=3, freq="M").to_timestamp()

grid = (agg[["Product", "City", "State"]].drop_duplicates()
        .assign(key=1)
        .merge(pd.DataFrame({"YearMonth": future_months, "key": [1]*3}), on="key")
        .drop("key", axis=1))

grid["YM_year"] = grid["YearMonth"].dt.year
grid["YM_month"] = grid["YearMonth"].dt.month
last_price = agg.groupby(["Product", "City", "State"])["AvgPrice"].last()
grid = grid.merge(last_price.rename("AvgPrice"), on=["Product", "City", "State"], how="left")

grid["PredRevenue"] = pipe.predict(grid[features_cols])

# Salvar
output = Path("data/processed/predictions_rf.csv")
grid.to_csv(output, index=False)
print(f"\n[OK] Salvo: {output}")

# Top previs├╡es
print("\n" + "="*70)
print("TOP 10 PREVISOES")
print("="*70)
top = grid.nlargest(10, "PredRevenue")
for i, row in enumerate(top.itertuples(), 1):
    print(f"{i:2}. {row.YearMonth.strftime('%Y-%m')} | {row.Product[:25]:25s} | {row.City[:12]:12s} | ${row.PredRevenue:>10,.2f}")

# Total por m├¬s
print("\n" + "="*70)
print("PREVISAO TOTAL POR MES")
print("="*70)
monthly = grid.groupby("YearMonth")["PredRevenue"].sum()
for month, value in monthly.items():
    print(f"{month.strftime('%Y-%m')}: ${value:>12,.2f}")

print("\n" + "="*70)
print("[SUCESSO] Modelo treinado e previsoes salvas!")
print("="*70)
print(f"\nArquivo: {output}")
print("\nPara visualizar: python view_results.py")

