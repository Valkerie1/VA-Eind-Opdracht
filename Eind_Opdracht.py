import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import geopandas as gpd
from statsmodels.formula.api import ols
import folium

st.set_page_config(page_title = 'Streamlit Dashboard', layout= 'wide')



who_data = pd.read_csv('countries.csv')

who_data.drop(['Arable (%)', 'Crops (%)', 'Other (%)', 'Agriculture', 'Industry', 'Service', 'Climate'], axis=1, inplace=True)

who_data['Pop. Density (per sq. mi.)'] = who_data['Pop. Density (per sq. mi.)'].str.replace(',', '.').astype(float)
who_data['Coastline (coast/area ratio)'] = who_data['Coastline (coast/area ratio)'].str.replace(',', '.').astype(float)
who_data['Net migration'] = who_data['Net migration'].str.replace(',', '.').astype(float)
who_data['Infant mortality (per 1000 births)'] = who_data['Infant mortality (per 1000 births)'].str.replace(',', '.').astype(float)
who_data['Literacy (%)'] = who_data['Literacy (%)'].str.replace(',', '.').astype(float)
who_data['Phones (per 1000)'] = who_data['Phones (per 1000)'].str.replace(',', '.').astype(float)
who_data['Birthrate'] = who_data['Birthrate'].str.replace(',', '.').astype(float)
who_data['Deathrate'] = who_data['Deathrate'].str.replace(',', '.').astype(float)

st.table(who_data)

