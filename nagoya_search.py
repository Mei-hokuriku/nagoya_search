#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[2]:


merged_df = pd.read_csv("nagoya_merged.csv")


# In[3]:


st.title("うなぎ屋サーチ")

price_type = st.radio(
    "比較したい価格を選択してください",
    options=["ランチ価格", "ディナー価格"],
    index=0,
    horizontal=True
)

price = "price_lunch" if price_type == "ランチ価格" else "price_dinner"

price_limit = st.slider("最低価格の上限", min_value=1000, max_value=10000, step=200, value=6000)
score_limit = st.slider("人気スコアの下限", min_value=0.0, max_value=35.0, step=2.0, value=5.0)


# In[5]:


filtered_df = merged_df[
    (merged_df[price] <= price_limit)&
    (merged_df['pop_score'] >= score_limit)
]


# In[6]:


fig = px.scatter(
    filtered_df,
    x='pop_score',
    y=price,
    hover_data=['name_nagoya', 'address', 'star', 'review'],
    title='人気スコアと最低価格の散布図'
)

st.plotly_chart(fig)


# In[7]:


selected_nagoya = st.selectbox('気になるうなぎ屋を選んで詳細を確認', filtered_df['name_nagoya'])

if selected_nagoya:
    url = filtered_df[filtered_df['name_nagoya'] == selected_nagoya]['link_detail'].values[0]
    st.markdown(f"[{selected_nagoya}のページへ移動]({url})", unsafe_allow_html=True)


# In[8]:


sort_key = st.selectbox(
    "ランキング基準を選んでください",
    ("star", "pop_score", "review", price)
)
ascending = True if sort_key == price else False


# In[9]:


st.subheader(f"{sort_key} によるうなぎ屋ランキング（上位10件）")
ranking_df = filtered_df.sort_values(by=sort_key, ascending=ascending).head(10)
st.dataframe(ranking_df[["name_nagoya", price, "pop_score", "star", "review", "address"]])


# In[ ]:




