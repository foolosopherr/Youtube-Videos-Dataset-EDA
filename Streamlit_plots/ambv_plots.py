import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import urllib.request
from PIL import Image

def plot_streamlit_ambv(df):
    options = df.select_dtypes(include=np.number).columns
    titles_and_links = df[['Video title', 'Thumbnail link']]
    all_titles = titles_and_links['Video title'].unique()
    titles_and_links = {titles_and_links.iloc[i, 0]:titles_and_links.iloc[i, 1] for i in range(titles_and_links.shape[0])}
    options = list(options) + [None]
    titles = st.sidebar.multiselect('Video titles:', all_titles, default=all_titles[::10])
    col1, col2, col3, col4 = st.columns([2,2,1,1])
    with col1:
        x_axis = st.selectbox('X axis feature:', options[:-1])
    with col2:
        y_axis = st.selectbox('Y axis feature:', options)
    with col3:
        y_scale = st.selectbox('Y axis scale:', ['Normal', 'Logarithmic'])
        y_scale_ = y_scale == 'Logarithmic'
    with col4:
        x_scale = st.selectbox('X axis scale:', ['Normal', 'Logarithmic'])
        x_vals = df[df['Video title'].isin(titles)][x_axis].values if x_scale=='Normal' else np.log(df[df['Video title'].isin(titles)][x_axis].values)

    col1_, col2_, col3_, col4_ = st.columns(4)
    with col1_:
        barmode = st.selectbox('Barmode:', ['group', 'stack', 'overlay'])
    with col2_:
        barnorm = st.selectbox('Barnorm:', [None, 'percent', 'fraction'])
    with col3_:
        nbins = st.slider('Number of bins:', 10, 50, 10)
    with col4_:
        color = st.selectbox('Color:', ['Video title', None])

    fig = px.histogram(df[df['Video title'].isin(titles)], x=x_vals, y=y_axis, log_y=y_scale_, color=color, 
                       title='Histogram', barmode=barmode, barnorm=barnorm,
                       nbins=nbins)

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

    col5, col6, col7 = st.columns(3)
    with col5:
        _x_scale = st.selectbox('X scale:', ['Normal', 'Logarithmic'])
        _x_scale_ = _x_scale == 'Logarithmic'
    with col6:
        _y_scale = st.selectbox('Y scale:', ['Normal', 'Logarithmic'])
        _y_scale_ = _y_scale == 'Logarithmic'
    with col7:
        _color = st.selectbox('Color feature:', df.columns)
        showlegend = _color in options[:-1]

    fig1 = px.scatter(df[df['Video title'].isin(titles)], x=x_axis, y=y_axis, color=_color,
                    log_x=_x_scale_, log_y=_y_scale_, hover_name='Video title',
                    title=f'Scatter plot between {x_axis} and {y_axis}')
    fig1.update_layout(showlegend=showlegend)
    st.plotly_chart(fig1)

    with st.expander("Click to view thumbnails"):
        for title in titles:
            link = titles_and_links[title]
            imgname = f"{link.split('/')[-2]}.jpg"
            urllib.request.urlretrieve(link, imgname)
            img = Image.open(imgname)
            st.write(title)
            st.image(img)
