import streamlit as st
from pathlib import Path

from graph.graph import app

st.title('Estruturar tabela com IA')

onclick = st.button('Começar ?', type='primary')


if onclick:
    path = Path('../data/imgs/')
    if not path.exists():
        st.warning('Arquivo não encontrado')
        raise FileNotFoundError('Arquivo não encontrado')

    for path in path.glob('*.*'):
        with st.spinner('Processando...'):
            res = app.invoke({'image_path': path, 'structure': True})
        st.subheader(path.stem)
        st.image(str(path))
        st.dataframe(res['descriptions'][0])



