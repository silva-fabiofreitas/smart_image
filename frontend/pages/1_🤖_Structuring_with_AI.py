import streamlit as st
from pathlib import Path

from graph.graph import app

# Configuração inicial da página
st.set_page_config(
    page_title="Análise de Pareto",
    page_icon="📊",
    layout="wide",
)

st.title('Estruturar tabela com IA')
st.write('Com a evolução do GPT-4, estruturar dados de tabelas a partir de imagens tornou-se mais acessível e '
             'eficiente. Essa abordagem combina o poder do reconhecimento visual com a habilidade de modelagem de'
             ' linguagem para transformar tabelas em formatos estruturados, como JSON ou modelos Pydantic.')

onclick = st.button('Começar ?', type='primary')


if onclick:
    path = Path('../data/imgs/')
    if not path.exists():
        st.warning('Arquivo não encontrado')
        raise FileNotFoundError('Arquivo não encontrado')

    cols = st.columns([6, 6])
    for i, path in enumerate(path.glob('*.*')):

        with cols[i % 2]:
            with st.spinner('Processando...'):
                res = app.invoke({'image_path': path, 'structure': True})
            st.subheader(path.stem)
            st.image(str(path))
            st.dataframe(res['descriptions'][0])
