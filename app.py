import streamlit as st
import pandas as pd

st.title('都道府県別にみた年別死亡数')

df = pd.read_csv('people.csv', encoding='cp932')

# 縦長に変換
df_long = df.melt(
    id_vars='都道府県',
    var_name='年',
    value_name='死亡数')

df_long['年'] = df_long['年'].astype(int)

# 年のリスト
years = sorted(df_long['年'].unique())

with st.sidebar:
    # ページリンク
    st.page_link("https://www.e-stat.go.jp/stat-search/files?page=1&query=%E9%83%BD%E9%81%93%E5%BA%9C%E7%9C%8C%E5%88%A5&layout=dataset&bunya_l=02&year=20250%2C20240%2C20230%2C20220&stat_infid=000040316502&collect_area=000&metadata=1&data=1",
              label="e-Sat data", icon="🌎")
    branch = st.multiselect('都道府県を選択してください（複数選択可）',
                            df['都道府県'].unique())
    
    year = st.selectbox('表示する年を選択してください',
                    years)
    
    range_mode = st.checkbox('年の推移を表示する')
    if range_mode:
            year_range = st.slider(label='表示する年の範囲を選択してください',
                        min_value= 1975,
                        max_value= 2024,
                        value=(1990, 2015) )

df = df_long.copy()

df = df[df['都道府県'].isin(branch)]
df = df[df['年'] == year]

df.drop('年', axis=1, inplace=True)
df.set_index('都道府県', inplace=True)

st.subheader(f'{year}年 都道府県別死亡数 (横軸：都道府県, 縦軸：死亡数(人))')
st.dataframe(df, width=800, height=200)
st.bar_chart(df)

if range_mode:
    df2 = df_long.copy()
    df2 =  df2[df2['都道府県'].isin(branch)]
    df2 = df2[(df2['年'] >= year_range[0]) &
            (df2['年'] <= year_range[1])]

    st.subheader(f'{year_range[0]}年～{year_range[1]}年 死亡数推移 (横軸：年, 縦軸：死亡数(人))')
    df_chart = df2.pivot(
        index='年',
        columns='都道府県',
        values='死亡数'
    )
    st.line_chart(df_chart)