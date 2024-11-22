"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def pareto_df(df, name):
    ...



st.header("Arquivo")
file = st.file_uploader("Arquivo", type="csv")
if file is not None:
    df = pd.read_csv(file, sep=';', index_col=0)
    st.dataframe(df)
    st.dataframe(df.label.value_counts(ascending=True).reset_index())
