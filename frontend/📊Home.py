from pathlib import Path

import streamlit as st

from frontend.data_analysis import calculate_pareto_dataframe, ParetoChart, load_csv

# Configuração inicial da página
st.set_page_config(
    page_title="Análise de Pareto",
    page_icon="📊",
    layout="wide",
)


# Função para exibir as imagens de uma categoria
def display_images_by_category(selection, df, image_dir):
    """
    Exibe imagens relacionadas a uma categoria selecionada.
    """
    if not selection:
        st.warning("Selecione uma categoria para visualizar imagens.")
        return

    # Filtrar caminhos de imagens pela seleção
    paths = list(Path(image_dir).glob('*.*'))
    filtered_paths = [
        path for path in paths if path.stem in df.query("label == @selection")['file'].values
    ]

    if not filtered_paths:
        st.info("Nenhuma imagem encontrada para a categoria selecionada.")
        return

    # Exibir imagens em colunas
    cols = st.columns(3)
    for i, image_path in enumerate(filtered_paths):
        with cols[i % 3]:  # Distribuir imagens em 3 colunas
            st.write(image_path.stem)
            st.image(str(image_path), use_container_width=True)


# Layout principal
def main():
    st.title("Análise de Pareto")
    st.write("Faça upload de um arquivo CSV para iniciar a análise.")

    # Upload de arquivo
    file = st.file_uploader("Carregar arquivo CSV", type="csv")
    df = load_csv(file, default_path="../data/classificacao.csv")

    if df is not None:
        # Exibir o DataFrame original
        st.subheader("Dados Carregados")
        _, center, _ = st.columns([1, 10, 1])
        center.dataframe(df, use_container_width=True)
    else:
        st.error("Erro ao carregar o arquivo. Verifique o formato e tente novamente.")
        return

    # Cálculo do Pareto
    df_pareto = calculate_pareto_dataframe(df, "label")

    # Exibir gráfico de Pareto
    st.divider()
    fig = ParetoChart(df_pareto).generate_combined_chart
    selected_click = st.plotly_chart(fig, on_select='rerun')
    event_label = (selected_click.selection.points and selected_click.selection.points[0]['x']) or None

    st.divider()
    st.subheader('Tabelas')
    options = df_pareto.label
    selection = st.segmented_control(
        "Mostrar tabela por categoria", options, selection_mode="single", default=event_label
    )

    display_images_by_category(selection, df, '../data/imgs/')


_, container, _ = st.columns((1, 10, 1))

with container:
    main()




