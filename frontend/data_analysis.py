from pathlib import Path

import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


def calculate_pareto_dataframe(df, column_name):
    """
    Calcula o DataFrame de Pareto com frequências, percentuais e acumulados.
    """
    return (
        df[column_name]
        .value_counts()
        .reset_index(name='frequency')
        .assign(
            freq_percent=lambda x: x.frequency / x.frequency.sum(),
            cumulative_percent=lambda x: round(x.freq_percent.cumsum() * 100, 2)
        )
        .rename(columns={'frequency': 'Freq.', 'freq_percent': 'Freq. (%)', 'cumulative_percent': 'Freq. acm (%)'})
    )


class ParetoChart:
    """
    Classe responsável por criar gráficos de Pareto, incluindo gráficos de barras e linhas acumuladas.
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def create_bar_chart(self):
        """
        Cria o gráfico de barras para os dados de Pareto.
        """
        bar_chart = px.bar(
            self.dataframe,
            x='label',
            y='Freq. (%)',
            title="Gráfico de Barras (Pareto)",
            hover_data={'Freq.': ':Freq.', 'Freq. (%)': ':.2%'}
        )



        bar_chart.update_traces(
            marker=dict(color='#1f77b4', line=dict(color='black', width=0.5))
        )
        bar_chart.update_layout(font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            ),)
        return bar_chart

    def create_line_chart(self):
        """
        Cria o gráfico de linhas para os dados acumulados de Pareto.
        """
        line_chart = px.line(
            self.dataframe,
            x='label',
            y='Freq. acm (%)',
            markers=True,
            title="Linha Acumulada (Pareto)"
        )
        line_chart.update_traces(
            marker=dict(color='#F27405'),
            line=dict(color='#F27405')
        )
        return line_chart

    @property
    def generate_combined_chart(self):
        """
        Gera o gráfico combinado de Pareto com barras e linha acumulada.
        """
        # Criar subplots para combinar gráficos
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Gerar gráficos individuais
        bar_chart = self.create_bar_chart()
        line_chart = self.create_line_chart()

        # Adicionar os gráficos ao subplot
        fig.add_trace(bar_chart.data[0], secondary_y=False)
        fig.add_trace(line_chart.data[0], secondary_y=True)

        # Personalizar layout
        fig.update_layout(
            height=600,
            yaxis=dict(
                showgrid=False,
                dtick=1,
            ),
            title="Gráfico de Pareto",
            xaxis_title="Categorias",
            yaxis_title="Frequência",
            yaxis2_title="Percentual Acumulado (%)",
            plot_bgcolor='#F5F5F5',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            title_font_size=18,
            xaxis_tickfont_size=14,
            yaxis_tickfont_size=14,
            yaxis_titlefont_size=14,
            yaxis2_titlefont_size=14,
            yaxis2_tickfont_size=14,
            hoverlabel_font_size=14,


        )

        return fig


def load_csv(file, default_path=None):
    """
    Carrega o arquivo CSV do upload ou de um caminho padrão.
    """
    if file is not None:
        return pd.read_csv(file, sep=';', index_col=0)
    elif default_path:
        return pd.read_csv(Path(default_path), sep=';', index_col=0)
    else:
        return None
