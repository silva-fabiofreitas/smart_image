"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd


def pareto_df(df, name):
    df_pareto = (
        df[name].value_counts()
        .reset_index(name='freq')
        .assign(
            freq_percent=lambda x: x.freq / sum(x.freq),
            acm_percent=lambda x: round(x.freq_percent.cumsum() * 100))
    )
    return df_pareto


st.header("Analise de Pareto")

file = st.file_uploader("Arquivo", type="csv")

if file is not None:
    df = pd.read_csv(file, sep=';', index_col=0)
    st.dataframe(df)
    st.dataframe(df.label.value_counts(ascending=True).reset_index())


df = pd.DataFrame([{'label':'A'}, {'label':'A'},{'label':'A'},{'label':'B'}, {'label':'B'}, {'label':'C'}])

# df = df.label.value_counts().reset_index(name='freq').assign(freq_percent = lambda x: x.freq/sum(x.freq), acm_percent = lambda x: round(x.freq_percent.cumsum()*100))
df = pareto_df(df, 'label')

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio
# pio.templates.default = "ggplot2"

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Atualizar cores e estilo
fig1 = px.bar(df, x='label', y='freq')
fig2 = px.line(df, x='label', y='acm_percent', markers=True)

# Configurar cores para as barras e linha
fig1.update_traces(marker={'color': '#1f77b4', 'line':{'color':'black'}})  # Azul-marinho
fig2.update_traces(marker={'color': '#F27405'}, line={'color': '#F27405'})  # Cinza claro nos marcadores e laranja na linha

# Add traces
fig.add_trace(
    fig1.data[0],
    secondary_y=False,
)

fig.add_trace(
    fig2.data[0],
    secondary_y=True,
)

# Layout
fig.update_layout(
    yaxis=dict(
        showgrid=False,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    xaxis_title="Categorias",
    yaxis_title="Frequency",
    yaxis2_title="Cumulative %",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig)