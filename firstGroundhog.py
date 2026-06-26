import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv("fully_exploded.csv")
use_df = df[['slug', 'year', 'shadow']]

# st.write(df.columns.tolist())

df['Name_Category'] = df['name'] + ', ' + df['Category'] + "/" + df['type']

st.write("This is a litte bit of groundhog data.")

all_groundhogs = df[['Name_Category', 'Category', 'slug', 'coordinates']].drop_duplicates(subset='Name_Category')

name_to_slug = dict(zip(all_groundhogs['Name_Category'], all_groundhogs['slug']))
all_labels = all_groundhogs['Name_Category'].tolist()

split = all_groundhogs["coordinates"].str.split(r',|, ',expand=True)

all_groundhogs["lat"] = pd.to_numeric(split[0], errors="coerce")
all_groundhogs["lon"] = pd.to_numeric(split[1], errors="coerce")



with st.container(border = True):
    selected_labels = st.multiselect('"Groundhogs"', all_labels, default = all_labels[:1])        
    
rolling_average = st.toggle("Rolling average")



if selected_labels:
    selected_slugs = [name_to_slug[label] for label in selected_labels]
    filtered = use_df[use_df['slug'].isin(selected_slugs)]
    data = filtered.pivot_table(index='year', columns='slug', values='shadow', aggfunc='first')

    slug_to_name = {v: k for k, v in name_to_slug.items()}
    data.columns = [slug_to_name.get(col, col) for col in data.columns]


    if rolling_average:
        window = st.slider("Rolling window (years)", min_value=2, max_value= 10, value=5)
        data = data.rolling(window).mean()
        data = data.dropna(how='all')

    map_filtered = all_groundhogs[all_groundhogs['slug'].isin(selected_slugs)]

    st.map(map_filtered)

    tab1, tab2 = st.tabs(["Chart", "Dataframe"])
    tab1.line_chart(data, height=250)
    tab2.dataframe(data,height=250, width=True)


else:
    st.info('Select at least one "groundhog" to see data.')





