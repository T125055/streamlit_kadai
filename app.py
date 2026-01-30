import streamlit as st
import pandas as pd

st.title('都道府県別にみた年別死亡数')

df = pd.read_csv('people.csv', encoding='cp932')

df_long = df.melt(
    id_vars='都道府県',
    var_name='年',
    value_name='死亡数')

df_long['年'] = df_long['年'].astype(int)

with st.sidebar:
    branch = st.multiselect('都道府県を選択してください（複数選択可）',
                            df['都道府県'].unique())
    
    year = st.slider(label='年を選択してください',
                        min_value= 1975,
                        max_value= 2024,
                        value=2000 )

df = df_long.copy()

df = df[df['都道府県'].isin(branch)]
df = df[df['年'] == year]

df.drop('年', axis=1, inplace=True)
df.set_index('都道府県', inplace=True)

st.dataframe(df, width=800, height=200)
st.line_chart(df)