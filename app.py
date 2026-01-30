import streamlit as st
import pandas as pd

st.title('自然公園の公園数と年間利用者数')

df = pd.read_csv('park.csv')

with st.sidebar:
    branch = st.multiselect('公園分類を選択してください（複数選択可）',
                            df['公園分類'].unique())
    year = st.number_input('年次を選択してください',
                           min_value=df['年'].min(),
                           max_value=df['年'].max(),
                           value=df['年'].min(),
                           step=1)
    
df = df[df['支店'].isin(branch)]
df = df[df['年']==year]
df.drop('年',axis=1,inplace=True)
df.set_index('支店',inplace=True)