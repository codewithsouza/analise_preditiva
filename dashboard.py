"""
Dashboard Interativo para Visualiza├º├úo de Previs├╡es
Execute: python dashboard.py

Este script cria visualiza├º├╡es interativas com Plotly das an├ílises e previs├╡es.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import webbrowser
import os

print("="*70)
print("DASHBOARD INTERATIVO - AN├üLISE PREDITIVA E-COMMERCE")
print("="*70)

# Verificar arquivos
processed_dir = Path("data/processed")
if not (processed_dir / "ecommerce_clean.parquet").exists():
    print("\n[ERRO] Execute primeiro: python run_analysis.py")
    exit(1)

# ===== CARREGAR DADOS =====
print("\n1. Carregando dados...")
df = pd.read_parquet(processed_dir / "ecommerce_clean.parquet")
df_monthly = pd.read_parquet(processed_dir / "ecommerce_monthly_ts.parquet")

# Verificar se tem previs├╡es
has_predictions = (processed_dir / "predictions_rf.csv").exists()
if has_predictions:
    pred_rf = pd.read_csv(processed_dir / "predictions_rf.csv")
    pred_sarima = pd.read_csv(processed_dir / "predictions_sarima.csv")
    metrics = pd.read_csv(processed_dir / "model_metrics.csv")
    print("[OK] Dados e previs├╡es carregados")
else:
    print("[AVISO] Previs├╡es n├úo encontradas. Execute: python run_modeling.py")
    pred_rf = None
    pred_sarima = None
    metrics = None

# ===== CRIAR DASHBOARD HTML =====
print("\n2. Criando visualiza├º├╡es interativas...")

# Criar figura com subplots
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        '≡ƒôê Evolu├º├úo Mensal da Receita',
        '≡ƒÅå Top 10 Produtos por Receita',
        '≡ƒîå Vendas por Cidade',
        'ΓÅ░ Vendas por Hora do Dia',
        '≡ƒôè Distribui├º├úo de Receita',
        '≡ƒôà Vendas por Dia da Semana'
    ),
    specs=[
        [{"type": "scatter"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "box"}, {"type": "bar"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.15
)

# 1. Evolu├º├úo mensal
monthly_revenue = df.groupby('Month')['Revenue'].sum().sort_index()
fig.add_trace(
    go.Scatter(
        x=monthly_revenue.index,
        y=monthly_revenue.values,
        mode='lines+markers',
        name='Receita Mensal',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10),
        hovertemplate='M├¬s %{x}<br>Receita: $%{y:,.2f}<extra></extra>'
    ),
    row=1, col=1
)

# 2. Top 10 produtos
top_products = df.groupby('Product')['Revenue'].sum().nlargest(10).sort_values()
fig.add_trace(
    go.Bar(
        y=top_products.index,
        x=top_products.values,
        orientation='h',
        name='Top Produtos',
        marker=dict(color='#ff7f0e'),
        hovertemplate='%{y}<br>Receita: $%{x:,.2f}<extra></extra>'
    ),
    row=1, col=2
)

# 3. Vendas por cidade
city_sales = df.groupby('City')['Revenue'].sum().nlargest(10).sort_values()
fig.add_trace(
    go.Bar(
        y=city_sales.index,
        x=city_sales.values,
        orientation='h',
        name='Vendas por Cidade',
        marker=dict(color='#2ca02c'),
        hovertemplate='%{y}<br>Receita: $%{x:,.2f}<extra></extra>'
    ),
    row=2, col=1
)

# 4. Vendas por hora
hourly_sales = df.groupby('Hour')['Revenue'].sum()
fig.add_trace(
    go.Bar(
        x=hourly_sales.index,
        y=hourly_sales.values,
        name='Vendas por Hora',
        marker=dict(color='#d62728'),
        hovertemplate='Hora: %{x}h<br>Receita: $%{y:,.2f}<extra></extra>'
    ),
    row=2, col=2
)

# 5. Distribui├º├úo de receita (box plot)
fig.add_trace(
    go.Box(
        y=df['Revenue'],
        name='Distribui├º├úo',
        marker=dict(color='#9467bd'),
        boxmean='sd'
    ),
    row=3, col=1
)

# 6. Vendas por dia da semana
days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
dow_sales = df.groupby('DayOfWeek')['Revenue'].sum()
fig.add_trace(
    go.Bar(
        x=[days[i] for i in dow_sales.index],
        y=dow_sales.values,
        name='Vendas por Dia',
        marker=dict(color='#8c564b'),
        hovertemplate='%{x}<br>Receita: $%{y:,.2f}<extra></extra>'
    ),
    row=3, col=2
)

# Atualizar layout
fig.update_layout(
    title_text="<b>Dashboard de An├ílise de Vendas E-commerce</b>",
    title_font_size=24,
    title_x=0.5,
    showlegend=False,
    height=1400,
    hovermode='closest',
    template='plotly_white'
)

# Ajustar eixos
fig.update_xaxes(title_text="M├¬s", row=1, col=1)
fig.update_yaxes(title_text="Receita ($)", row=1, col=1)
fig.update_xaxes(title_text="Receita ($)", row=1, col=2)
fig.update_xaxes(title_text="Receita ($)", row=2, col=1)
fig.update_xaxes(title_text="Hora", row=2, col=2)
fig.update_yaxes(title_text="Receita ($)", row=2, col=2)
fig.update_yaxes(title_text="Receita ($)", row=3, col=1)
fig.update_xaxes(title_text="Dia da Semana", row=3, col=2)
fig.update_yaxes(title_text="Receita ($)", row=3, col=2)

# Salvar dashboard principal
output_file = "reports/dashboard_vendas.html"
Path("reports").mkdir(exist_ok=True)
fig.write_html(output_file, auto_open=False)
print(f"[OK] Dashboard salvo: {output_file}")

# ===== DASHBOARD DE PREVIS├òES =====
if has_predictions:
    print("\n3. Criando dashboard de previs├╡es...")
    
    # Criar figura de previs├╡es
    fig_pred = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '≡ƒö« Previs├╡es Random Forest - Top 15 Produtos',
            '≡ƒôê Previs├╡es SARIMA - 6 Meses Futuros',
            '≡ƒÄ» M├⌐tricas dos Modelos',
            '≡ƒÆ░ Previs├úo Total por M├¬s (Random Forest)'
        ),
        specs=[
            [{"type": "bar"}, {"type": "scatter"}],
            [{"type": "bar"}, {"type": "bar"}]
        ],
        vertical_spacing=0.15,
        horizontal_spacing=0.12
    )
    
    # 1. Top previs├╡es Random Forest
    top_pred = pred_rf.nlargest(15, 'PredRevenue')
    top_pred['Label'] = top_pred['Product'].str[:25] + ' - ' + top_pred['City'].str[:10]
    
    fig_pred.add_trace(
        go.Bar(
            y=top_pred['Label'],
            x=top_pred['PredRevenue'],
            orientation='h',
            marker=dict(color='#17becf'),
            hovertemplate='%{y}<br>Previs├úo: $%{x:,.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 2. Previs├╡es SARIMA
    pred_sarima['Month'] = pd.to_datetime(pred_sarima['Month'])
    
    fig_pred.add_trace(
        go.Scatter(
            x=pred_sarima['Month'],
            y=pred_sarima['Prediction'],
            mode='lines+markers',
            name='Previs├úo',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=12),
            hovertemplate='%{x|%Y-%m}<br>Previs├úo: $%{y:,.2f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Adicionar intervalo de confian├ºa
    fig_pred.add_trace(
        go.Scatter(
            x=pred_sarima['Month'],
            y=pred_sarima['Upper_CI'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ),
        row=1, col=2
    )
    
    fig_pred.add_trace(
        go.Scatter(
            x=pred_sarima['Month'],
            y=pred_sarima['Lower_CI'],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(31, 119, 180, 0.2)',
            line=dict(width=0),
            name='IC 80%',
            hovertemplate='IC: $%{y:,.2f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 3. M├⌐tricas dos modelos
    colors = ['#2ca02c', '#d62728']
    for i, row in metrics.iterrows():
        fig_pred.add_trace(
            go.Bar(
                x=['MAE', 'RMSE'],
                y=[row['MAE'], row['RMSE']],
                name=row['Model'],
                marker=dict(color=colors[i]),
                hovertemplate='%{x}: $%{y:,.2f}<extra></extra>'
            ),
            row=2, col=1
        )
    
    # 4. Previs├úo total por m├¬s
    monthly_pred = pred_rf.groupby('YearMonth')['PredRevenue'].sum().reset_index()
    monthly_pred['YearMonth'] = pd.to_datetime(monthly_pred['YearMonth'])
    
    fig_pred.add_trace(
        go.Bar(
            x=monthly_pred['YearMonth'].dt.strftime('%Y-%m'),
            y=monthly_pred['PredRevenue'],
            marker=dict(color='#ff7f0e'),
            hovertemplate='%{x}<br>Previs├úo Total: $%{y:,.2f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    # Layout
    fig_pred.update_layout(
        title_text="<b>Dashboard de Previs├╡es - Modelos Preditivos</b>",
        title_font_size=24,
        title_x=0.5,
        height=1000,
        showlegend=True,
        hovermode='closest',
        template='plotly_white'
    )
    
    # Ajustar eixos
    fig_pred.update_xaxes(title_text="Previs├úo de Receita ($)", row=1, col=1)
    fig_pred.update_xaxes(title_text="M├¬s", row=1, col=2)
    fig_pred.update_yaxes(title_text="Receita ($)", row=1, col=2)
    fig_pred.update_xaxes(title_text="M├⌐trica", row=2, col=1)
    fig_pred.update_yaxes(title_text="Valor ($)", row=2, col=1)
    fig_pred.update_xaxes(title_text="M├¬s", row=2, col=2)
    fig_pred.update_yaxes(title_text="Receita Total ($)", row=2, col=2)
    
    # Salvar dashboard de previs├╡es
    output_pred = "reports/dashboard_previsoes.html"
    fig_pred.write_html(output_pred, auto_open=False)
    print(f"[OK] Dashboard de previs├╡es salvo: {output_pred}")

# ===== GR├üFICO INTERATIVO DE PRODUTOS =====
print("\n4. Criando visualiza├º├úo de produtos...")

# Treemap de produtos por receita
product_revenue = df.groupby(['Product', 'City']).agg({
    'Revenue': 'sum',
    'Quantity Ordered': 'sum'
}).reset_index()
product_revenue = product_revenue.rename(columns={'Quantity Ordered': 'Quantity'})

fig_treemap = px.treemap(
    product_revenue.nlargest(50, 'Revenue'),
    path=['Product', 'City'],
    values='Revenue',
    title='<b>Distribui├º├úo de Receita por Produto e Cidade</b>',
    color='Revenue',
    color_continuous_scale='Blues',
    hover_data={'Revenue': ':$,.2f', 'Quantity': ':,'}
)

fig_treemap.update_layout(height=700)
output_treemap = "reports/dashboard_produtos.html"
fig_treemap.write_html(output_treemap, auto_open=False)
print(f"[OK] Dashboard de produtos salvo: {output_treemap}")

# ===== ABRIR NO NAVEGADOR =====
print("\n" + "="*70)
print("[SUCESSO] DASHBOARDS CRIADOS COM SUCESSO!")
print("="*70)

print("\nArquivos HTML gerados:")
print(f"  1. {output_file}")
if has_predictions:
    print(f"  2. {output_pred}")
print(f"  3. {output_treemap}")

print("\nAbrindo dashboards no navegador...")

# Abrir dashboards
for file in [output_file, output_pred if has_predictions else None, output_treemap]:
    if file:
        abs_path = Path(file).absolute()
        webbrowser.open(f'file:///{abs_path}')

print("\n" + "="*70)
print("Os dashboards foram abertos no seu navegador!")
print("Voc├¬ pode explorar os gr├íficos interativos:")
print("  - Zoom: clique e arraste")
print("  - Detalhes: passe o mouse sobre os elementos")
print("  - Download: bot├úo de c├ómera no canto superior direito")
print("="*70)

