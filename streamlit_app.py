import pandas as pd
import streamlit as st
import re
import pycountry_convert as pc
from Streamlit_plots.vpot_plots import plot_streamlit_vpot
from Streamlit_plots.ambv_plots import plot_streamlit_ambv
from Streamlit_plots.ambcass_plots import main_ambcass

ambcass = pd.read_csv('../data/Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')
ambv = pd.read_csv('../data/Aggregated_Metrics_By_Video.csv').iloc[1:].reset_index(drop=True)
acv = pd.read_csv('../data/All_Comments_Final.csv')
vpot = pd.read_csv('../data/Video_Performance_Over_Time.csv')

# "vpot" dataset changes
vpot['Date'] = pd.to_datetime(vpot['Date'])
vpot = pd.merge(vpot, vpot.groupby('Video Title')['Date'].agg('min'), left_on='Video Title', right_index=True, how='left')
vpot = vpot.rename(columns={'Date_x': 'Date', 'Date_y':'Start Date'})
vpot['Days from start'] = vpot['Date'] - vpot['Start Date']
vpot['Days from start'] = vpot['Days from start'].dt.days

# "ambv" dataset change
ambv.columns = list(map(lambda x:re.sub(r'[^a-zA-Z0-9\(\)\%\- ]', '', x), ambv.columns))
ambv = ambv.astype({'Video publish time':'datetime64[ns]',
                   'Average view duration':'datetime64[ns]'})
ambv['Average view duration'] = ambv['Average view duration'].dt.minute * 60 + ambv['Average view duration'].dt.second
ambv = pd.merge(ambv, vpot[['Video Length', 'External Video ID']], left_on='Video', right_on='External Video ID', how='left').iloc[:, :-1]
thumbnail_links = ambcass[['External Video ID', 'Thumbnail link']].drop_duplicates().reset_index(drop=True)
ambv = pd.merge(ambv, thumbnail_links, left_on='Video', right_on='External Video ID', how='left').drop('External Video ID', axis=1)
# "ambcass" dataset change
code_d = pc.map_country_alpha2_to_country_alpha3()
ambcass['Country Code'] = ambcass['Country Code'].replace('XK', 'ZZ')
ambcass['Country Code'] = ambcass['Country Code'].fillna('ZZ')
code_d['ZZ'] = None
ambcass['Country Code'] = ambcass['Country Code'].apply(lambda x: code_d[x])


st.write("""
# Exploratory Data Analysis 
""")

filenames = ['Aggregated_Metrics_By_Country_And_Subscriber_Status',
'Aggregated_Metrics_By_Video', 'All_Comments_Final', 'Video_Performance_Over_Time']
filenames = list(map(lambda x: ' '.join(x.split('_')).capitalize(), filenames))
fn = st.selectbox('Choose dataset:', filenames)
if fn == filenames[0]:
    main_ambcass(ambcass)
elif fn == filenames[1]:
    plot_streamlit_ambv(ambv)
elif fn == filenames[2]:
    pass 
else:
    plot_streamlit_vpot(vpot)