import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

def plot_streamlit_ambcass(df):
    # options = ['World', 'North America', 'South America', 'Europe', 'Asia', 'Africa']
    all_titles = df['Video Title'].unique()
    title = st.sidebar.multiselect('Video titles:', all_titles, default=all_titles[:3])
    numeric_features = df.select_dtypes(include=np.number).columns.drop('Video Length')
    numeric_features = list(numeric_features)
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    with col1:
        fig1_x = st.selectbox('Scatter X axis:', numeric_features)
    with col2:
        fig1_y = st.selectbox('Scatter Y axis:', numeric_features)
    with col3:
        fig1_color = st.selectbox('Scatter color:', numeric_features + ['Video Title', None])
    with col4:
        fig1_size = st.selectbox('Scatter size:', numeric_features + [None])
    with col5:
        fig1_x_scale = st.selectbox('Scatter X axis scale:', ['Normal', 'Logarithmic'])
        fig1_x_scale_ = fig1_x_scale == 'Logarithmic'
    with col6:
        fig1_y_scale = st.selectbox('Scatter Y axis scale', ['Normal', 'Logarithmic'])
        fig1_y_scale_ = fig1_y_scale == 'Logarithmic'

    _temp = df[df['Video Title'].isin(title)]
    line = px.scatter(_temp, color=fig1_color, size=fig1_size,
                      x=fig1_x, y=fig1_y, log_x=fig1_x_scale_, log_y=fig1_y_scale_,
                      labels={'x': f'Cumulative sum of {fig1_x}'}, 
                      title=f'Scatter between {fig1_x} and {fig1_y}')
    st.plotly_chart(line)

    _col1, _col2, _col3 = st.columns(3)
    _col4, _col5, _col6, _col7 = st.columns(4)
    with _col1:
        fig2_x = st.selectbox('Histogram X axis:', numeric_features)
    with _col2:
        fig2_y = st.selectbox('Histogram Y axis:', numeric_features + [None])
    with _col3:
        fig2_color = st.selectbox('Histogram color:', ['Video Title', None])
    with _col4:
        fig2_y_scale = st.selectbox('Histogram Y axis scale:', ['Normal', 'Logarithmic'])
        fig2_y_scale_ = fig2_y_scale == 'Logarithmic'
    with _col5:
        nbins = st.slider('Number of bins:', 5, 50, 10)
    with _col6:
        barmode = st.selectbox('Barmode:', ['stack', 'group', 'overlay'])
    with _col7:
        barnorm = st.selectbox('Barnorm:', [None, 'percent', 'fraction'])

    hist = px.histogram(_temp, color=fig2_color,
                        x=fig2_x, y=fig2_y, log_y=fig2_y_scale_, nbins=nbins, 
                        barmode=barmode, barnorm=barnorm,
                        title=f'Histogram for {fig1_x}')
    st.plotly_chart(hist)


def plot_streamlit_ambcass_map(df):
    options = ['World', 'North America', 'South America', 'Europe', 'Asia', 'Africa']
    all_titles = df['Video Title'].unique()
    titles = st.sidebar.multiselect('Video titles:', all_titles, default=all_titles[::40])
    numeric_features = df.select_dtypes(include=np.number).columns.drop(['Video Length'])
    numeric_features = list(numeric_features)

    def find_ratio(sub):
        return (sub['Views'] * sub['Average View Percentage']).sum() / sub['Views'].sum()

    # __temp = _temp.groupby('Country Code').sum().drop('Is Subscribed', axis=1)
    # __temp['Video Length'] = _temp.groupby('Country Code')['Video Length'].mean()
    # __temp['Average View Percentage'] = _temp.groupby('Country Code')[['Views', 'Average View Percentage']].apply(find_ratio)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        col_widget = st.selectbox(label='Feature:', options=numeric_features)
    
    scopes = ['World', 'North America', 'Asia', 'Europe', 'South America', 'Africa']
    with col2:
        scope = st.selectbox(label='Scope:', options=scopes)
    
    scales = ['Normal', 'Logarithmic']
    with col3:
        scale = st.selectbox(label='Scale', options=scales)
    
    with col4:
        agg_func = st.selectbox('Aggregation function:', ['sum', 'mean', 'median', 'max', 'min', 'default'])

    all_projections = ['equirectangular', 'mercator', 'orthographic', 'natural earth', 
                       'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 
                       'azimuthal equidistant', 'conic equal area', 'conic conformal', 
                       'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 
                       'transverse mercator', 'winkel tripel', 'aitoff', 'sinusoidal']

    projection = st.sidebar.selectbox(label='Projection:', options=all_projections)

    if scope == 'World':
        title = f'{col_widget} around the world'
    else:
        title = f'{col_widget} in {scope}'

    _temp = df[df['Video Title'].isin(titles)]
    _temp = _temp.groupby('Country Code')[numeric_features].agg(agg_func).reset_index() if agg_func != 'default' else _temp

    values = _temp[col_widget] if scale == 'Normal' else np.log(_temp[col_widget])
    fig = px.choropleth(_temp, 
                        locations='Country Code',
                        color=values,
                        title=title, #color_continuous_scale='tropic',
                        projection=projection, scope=scope.lower())

    st.plotly_chart(fig)


def main_ambcass(df):
    pl = st.selectbox('Choose plots', ['Scatter & Histogram', 'Map'])
    if pl == 'Scatter & Histogram':
        plot_streamlit_ambcass(df)
    elif pl == 'Map':
        plot_streamlit_ambcass_map(df)
    else:
        st.write('Something is wrong. There is no such plot.')