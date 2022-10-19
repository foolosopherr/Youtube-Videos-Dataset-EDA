import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

def plot_streamlit_vpot(df):
    all_titles = df['Video Title'].unique()
    options = df.select_dtypes(include=np.number).columns.drop('Video Length')
    scales = ['Normal', 'Logarithmic']
    
    video_title = st.sidebar.multiselect(label="Video titles:",
                                         options=all_titles,
                                         default=all_titles[:3])
    
    col1, col2, col3 = st.columns([3,2,2])
    
    with col1:
        feature = st.selectbox("Feature", options)
    with col2:
        scale = st.selectbox('Scale:', scales)
        _scale = scale == "Logarithmic"
    with col3:
        x_axis = st.selectbox('Feature for X axis:', ['Days from start', 'Date'])

    width = st.slider('Plot width:', 500, 2000, 1000)

    fig = px.line(df[df['Video Title'].isin(video_title)], x=x_axis, y=feature, 
                  title=feature, color='Video Title', log_y=_scale, width=width)
    
    st.plotly_chart(fig)

    _col1, _col2 = st.columns(2)
    with _col1:
        barmode_ = ['group', 'stack']
        barmode = st.selectbox('Barmode:', barmode_)
    with _col2:
        barnorm_ = [None, 'percent', 'fraction']
        barnorm = st.selectbox('Barnorm:', barnorm_)
    height = st.slider('Plot height:', 500, 1000, 700)
    fig2 = px.histogram(df[df['Video Title'].isin(video_title)], x='Video Title', y=feature, color='Video Title',
                        title='Histogram', log_y=_scale, width=width, height=height)
    st.plotly_chart(fig2)


# def plot_streamlit_vpot_animation(df):
