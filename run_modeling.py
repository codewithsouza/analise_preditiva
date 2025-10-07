"""
Script para executar modelagem preditiva do e-commerce.
Execute: python run_modeling.py

Requisitos:
- Execute primeiro: python run_analysis.py (para gerar dados processados)
- Instale: pip install scikit-learn statsmodels prophet
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
import time
warnings.filterwarnings("ignore")

# Sklearn
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Statsmodels
from statsmodels.tsa.statespace.sarimax import SARIMAX
import itertools

print("="*70)
print("MODELAGEM PREDITIVA - E-COMMERCE")
print("="*70)

# ===== VERIFICAR DADOS PROCESSADOS =====
processed_path = Path("data/processed/ecommerce_clean.parquet")
if not processed_path.exists():
    print("\n[ERRO] Dados processados nao encontrados!")
    print("Execute primeiro: python run_analysis.py")
    exit(1)

print("\n[OK] Dados processados encontrados")

# ===== CARREGAR DADOS =====
print("\n1. Carregando dados processados...")
df = pd.read_parquet(processed_path)

# Renomear para consist├¬ncia
df = df.rename(columns={
    "Order Date": "OrderDate",
    "Quantity Ordered": "Quantity",
    "Price Each": "Price"
})

print(f"[OK] Dataset: {df.shape[0]:,} linhas")

# ===================================================================
# PARTE 1: REGRESS├âO (Random Forest)
# ===================================================================
print("\n" + "="*70)
print("PARTE 1: REGRESS├âO (Random Forest)")
print("="*70)

# ===== AGREGA├ç├âO =====
print("\n2. Agregando dados por m├¬s ├ù produto ├ù cidade...")
agg = (df
       .assign(YearMonth=df["OrderDate"].dt.to_period("M").dt.to_timestamp())
       .groupby(["YearMonth", "Product", "City", "State"], as_index=False)
       .agg(
           Quantity=("Quantity", "sum"),
           Revenue=("Revenue", "sum"),
           AvgPrice=("Price", "mean")
       )
)

agg["YM_year"] = agg["YearMonth"].dt.year
agg["YM_month"] = agg["YearMonth"].dt.month

print(f"[OK] Dataset agregado: {agg.shape[0]:,} combinacoes")

# ===== SPLIT TEMPORAL =====
print("\n3. Split temporal (80% treino / 20% teste)...")
cutoff = agg["YearMonth"].quantile(0.8)
train = agg[agg["YearMonth"] < cutoff].copy()
test = agg[agg["YearMonth"] >= cutoff].copy()

features_cols = ["Product", "City", "State", "YM_year", "YM_month", "AvgPrice"]
target = "Revenue"

X_train = train[features_cols]
y_train = train[target]
X_test = test[features_cols]
y_test = test[target]

print(f"[OK] Treino: {train.shape[0]:,} | Teste: {test.shape[0]:,}")

# ===== PIPELINE E TREINAMENTO =====
print("\n4. Treinando Random Forest...")
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["Product", "City", "State"]),
    ("num", "passthrough", ["YM_year", "YM_month", "AvgPrice"])
])

rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=0
)

pipe = Pipeline([
    ("prep", preprocessor),
    ("model", rf)
])

start = time.time()
pipe.fit(X_train, y_train)
elapsed = time.time() - start

print(f"[OK] Modelo treinado em {elapsed:.2f} segundos")

# ===== AVALIA├ç├âO =====
print("\n5. Avaliando modelo...")
pred_test = pipe.predict(X_test)

mae_test = mean_absolute_error(y_test, pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, pred_test))
r2_test = r2_score(y_test, pred_test)
mape_test = np.mean(np.abs((y_test - pred_test) / y_test)) * 100

print("\n" + "="*70)
print("RESULTADOS - Random Forest")
print("="*70)
print(f"MAE:  ${mae_test:,.2f}")
print(f"RMSE: ${rmse_test:,.2f}")
print(f"R┬▓:   {r2_test:.3f}")
print(f"MAPE: {mape_test:.2f}%")
print("="*70)

# ===== PREVIS├âO FUTURA (3 MESES) =====
print("\n6. Gerando previs├╡es futuras (3 meses)...")
last_date = agg["YearMonth"].max()
future_months = pd.period_range(last_date + pd.DateOffset(months=1), periods=3, freq="M").to_timestamp()

grid = (agg[["Product", "City", "State"]].drop_duplicates()
        .assign(key=1)
        .merge(pd.DataFrame({"YearMonth": future_months, "key": [1]*len(future_months)}), on="key")
        .drop("key", axis=1))

grid["YM_year"] = grid["YearMonth"].dt.year
grid["YM_month"] = grid["YearMonth"].dt.month

last_price = agg.groupby(["Product", "City", "State"])["AvgPrice"].last()
grid = grid.merge(last_price.rename("AvgPrice"), on=["Product", "City", "State"], how="left")

future_pred = pipe.predict(grid[features_cols])
grid["PredRevenue"] = future_pred

print(f"[OK] {grid.shape[0]:,} previsoes geradas")

# Top previs├╡es por m├¬s
print("\nTOP 5 PREVIS├òES POR M├èS:")
for month in future_months:
    month_data = grid[grid["YearMonth"] == month].nlargest(5, "PredRevenue")
    total = month_data["PredRevenue"].sum()
    print(f"\n{month.strftime('%Y-%m')} (Total previsto: ${total:,.2f}):")
    for i, row in enumerate(month_data.itertuples(), 1):
        print(f"  {i}. {row.Product[:30]:30s} | {row.City[:15]:15s} | ${row.PredRevenue:>10,.2f}")

# ===================================================================
# PARTE 2: S├ëRIES TEMPORAIS (SARIMA)
# ===================================================================
print("\n" + "="*70)
print("PARTE 2: S├ëRIES TEMPORAIS (SARIMA)")
print("="*70)

# ===== PREPARAR S├ëRIE MENSAL =====
print("\n7. Preparando s├⌐rie temporal mensal...")
monthly = (df.assign(YearMonth=df["OrderDate"].dt.to_period("M").dt.to_timestamp())
             .groupby("YearMonth", as_index=True)["Revenue"].sum()
             .sort_index())

cutoff_ts = monthly.index[int(len(monthly) * 0.8)]
y_train_ts = monthly[monthly.index < cutoff_ts]
y_test_ts = monthly[monthly.index >= cutoff_ts]

print(f"[OK] Serie: {len(monthly)} meses | Treino: {len(y_train_ts)} | Teste: {len(y_test_ts)}")

# ===== BUSCAR MELHOR SARIMA =====
print("\n8. Buscando melhor modelo SARIMA (pode demorar 1-2 min)...")
p = d = q = range(0, 2)
pdq = list(itertools.product(p, [1], q))
seasonal_pdq = [(0, 1, 0, 12)]

best = None
best_aic = float("inf")

for order in pdq:
    for sorder in seasonal_pdq:
        try:
            model = SARIMAX(y_train_ts, 
                          order=order, 
                          seasonal_order=sorder,
                          enforce_stationarity=False,
                          enforce_invertibility=False)
            result = model.fit(disp=False, maxiter=200)
            
            if result.aic < best_aic:
                best_aic = result.aic
                best = (order, sorder)
        except:
            continue

print(f"[OK] Melhor: {best[0]} x {best[1]} | AIC={best_aic:.2f}")

# ===== TREINAR E AVALIAR =====
print("\n9. Treinando modelo final...")
model_sarima = SARIMAX(y_train_ts,
                      order=best[0],
                      seasonal_order=best[1],
                      enforce_stationarity=False,
                      enforce_invertibility=False)
result_sarima = model_sarima.fit(disp=False, maxiter=200)

pred_sarima_test = result_sarima.get_forecast(steps=len(y_test_ts)).predicted_mean

mae_sarima = mean_absolute_error(y_test_ts, pred_sarima_test)
rmse_sarima = np.sqrt(mean_squared_error(y_test_ts, pred_sarima_test))
mape_sarima = np.mean(np.abs((y_test_ts - pred_sarima_test) / y_test_ts)) * 100

print("\n" + "="*70)
print("RESULTADOS - SARIMA")
print("="*70)
print(f"MAE:  ${mae_sarima:,.2f}")
print(f"RMSE: ${rmse_sarima:,.2f}")
print(f"MAPE: {mape_sarima:.2f}%")
print("="*70)

# ===== PREVIS├âO FUTURA (6 MESES) =====
print("\n10. Gerando previs├╡es SARIMA (6 meses futuros)...")
model_full = SARIMAX(monthly,
                    order=best[0],
                    seasonal_order=best[1],
                    enforce_stationarity=False,
                    enforce_invertibility=False)
result_full = model_full.fit(disp=False, maxiter=200)

n_future = 6
forecast = result_full.get_forecast(steps=n_future)
pred_future = forecast.predicted_mean
conf_int = forecast.conf_int(alpha=0.2)

# Criar datas futuras manualmente
last_date = monthly.index[-1]
future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=n_future, freq='MS')

print("\nPREVIS├âO SARIMA - PR├ôXIMOS 6 MESES:")
print("="*70)
for i, (date, value) in enumerate(zip(future_dates, pred_future.values)):
    lower = conf_int.iloc[i, 0]
    upper = conf_int.iloc[i, 1]
    print(f"{date.strftime('%Y-%m')}: ${value:>12,.2f}  (IC: ${lower:>12,.2f} - ${upper:>12,.2f})")

# ===================================================================
# PROPHET (OPCIONAL)
# ===================================================================
print("\n" + "="*70)
print("PARTE 3: PROPHET (OPCIONAL)")
print("="*70)

try:
    from prophet import Prophet
    
    print("\n11. Treinando Prophet...")
    df_prophet = monthly.reset_index().rename(columns={"YearMonth": "ds", "Revenue": "y"})
    
    model_prophet = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )
    model_prophet.fit(df_prophet)
    
    future_prophet = model_prophet.make_future_dataframe(periods=6, freq='MS')
    forecast_prophet = model_prophet.predict(future_prophet)
    
    print("\nPREVIS├âO PROPHET - PR├ôXIMOS 6 MESES:")
    print("="*70)
    future_only = forecast_prophet.tail(6)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    for _, row in future_only.iterrows():
        print(f"{row['ds'].strftime('%Y-%m')}: ${row['yhat']:>12,.2f}  " + 
              f"(IC: ${row['yhat_lower']:>12,.2f} - ${row['yhat_upper']:>12,.2f})")
    
    print("[OK] Prophet executado com sucesso")
    
except ImportError:
    print("\nΓÜá∩╕Å  Prophet n├úo instalado (opcional)")
    print("   Para instalar: pip install prophet")

# ===================================================================
# COMPARA├ç├âO FINAL
# ===================================================================
print("\n" + "="*70)
print("COMPARA├ç├âO DE MODELOS")
print("="*70)
print(f"\n{'Modelo':<25} {'MAE':>15} {'RMSE':>15} {'MAPE':>10}")
print("-"*70)
print(f"{'Random Forest':<25} ${mae_test:>14,.2f} ${rmse_test:>14,.2f} {mape_test:>9.2f}%")
print(f"{'SARIMA':<25} ${mae_sarima:>14,.2f} ${rmse_sarima:>14,.2f} {mape_sarima:>9.2f}%")

# ===================================================================
# SALVAR RESULTADOS
# ===================================================================
print("\n" + "="*70)
print("SALVANDO RESULTADOS")
print("="*70)

# Salvar previs├╡es Random Forest
output_rf = Path("data/processed/predictions_rf.csv")
grid.to_csv(output_rf, index=False)
print(f"[OK] {output_rf}")

# Salvar previs├╡es SARIMA
output_sarima = pd.DataFrame({
    "Month": future_dates,
    "Prediction": pred_future.values,
    "Lower_CI": conf_int.iloc[:, 0].values,
    "Upper_CI": conf_int.iloc[:, 1].values
})
output_sarima_path = Path("data/processed/predictions_sarima.csv")
output_sarima.to_csv(output_sarima_path, index=False)
print(f"[OK] {output_sarima_path}")

# Salvar m├⌐tricas
metrics = pd.DataFrame({
    "Model": ["Random Forest", "SARIMA"],
    "MAE": [mae_test, mae_sarima],
    "RMSE": [rmse_test, rmse_sarima],
    "MAPE": [mape_test, mape_sarima]
})
metrics_path = Path("data/processed/model_metrics.csv")
metrics.to_csv(metrics_path, index=False)
print(f"[OK] {metrics_path}")

print("\n" + "="*70)
print("[SUCESSO] MODELAGEM CONCLUIDA COM SUCESSO!")
print("="*70)
print("\nArquivos gerados:")
print(f"  - {output_rf}")
print(f"  - {output_sarima_path}")
print(f"  - {metrics_path}")
print("\nPara visualizar os notebooks com gr├íficos detalhados:")
print("  - notebooks/01_exploracao/ecommerce_eda.ipynb")
print("  - notebooks/04_modelagem/ecommerce_predictive_models.ipynb")

