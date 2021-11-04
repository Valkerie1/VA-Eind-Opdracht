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


# inladen van WHO data + bewerking
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

mappings = {'ASIA (EX. NEAR EAST)         ':"ASIA",
           'EASTERN EUROPE                     ':"EUROPE",
           'NORTHERN AFRICA                    ':"AFRICA",
           'OCEANIA                            ':"OCEANIA",
           'WESTERN EUROPE                     ':"EUROPE",
           'SUB-SAHARAN AFRICA                 ':"AFRICA",
           'LATIN AMER. & CARIB    ':"LATIN AMERICA",
           'C.W. OF IND. STATES ':"CIS",
           'NEAR EAST                          ':"MIDDLE EAST",
           'NORTHERN AMERICA                   ':"NORTHERN AMERICA",
           'BALTICS                            ':"EUROPE"}
who_data['Region'] = who_data['Region'].replace(mappings)



# Inladen van geojson data + bewerking
countries = gpd.read_file('countries.geojson')
who_data['Country'] = who_data['Country'].str.replace(' ','')
countries['ADMIN'] = countries['ADMIN'].str.replace(' ','')

remap = {"UnitedStates" : "UnitedStatesofAmerica"}
who_data['Country'] = who_data['Country'].replace(remap)

WHO = gpd.GeoDataFrame(pd.merge(who_data, countries, 
                                left_on="Country", right_on='ADMIN'))

ASIA = WHO[WHO['Region']=='ASIA']
EUROPE = WHO[WHO['Region']=='EUROPE']
AFRICA = WHO[WHO['Region']=='AFRICA']
OCEANIA = WHO[WHO['Region']=='OCEANIA']
LATINAMERICA = WHO[WHO['Region']=='LATIN AMERICA']
CIS = WHO[WHO['Region']=='CIS']
MIDDLEEAST = WHO[WHO['Region']=='MIDDLE EAST']
NORTHERNAMERICA = WHO[WHO['Region']=='NORTHERN AMERICA']



# Inladen van leeftijdsverdeling per land + bewerking
world_age_categories = pd.read_csv('world_age_categories.csv')



# Boxplot
fig_boxplot = px.box(data_frame=who_data, x=who_data['Region'], y='GDP ($ per capita)', 
             color='Region')
fig_boxplot.update_xaxes(title_text = 'Regio')
fig_boxplot.update_yaxes(title_text = 'GDP ($ per inwoner)')
fig_boxplot.update_layout({'title':{'text':'GDP per regio', 
                            'x':0.5}})
    
st.plotly_chart(fig_boxplot)





# Scatterplots
fig_scatter_GDP_InfantMortality = px.scatter(data_frame=who_data,
                x='GDP ($ per capita)',
                y='Infant mortality (per 1000 births)',
                trendline='ols', 
                trendline_options=dict(log_y=True),
                trendline_color_override="red")

fig_scatter_GDP_InfantMortality.update_xaxes(title_text = 'GDP ($ per inwoner)')
fig_scatter_GDP_InfantMortality.update_yaxes(title_text = 'Kindersterfte (per 1000 geboortes)')
fig_scatter_GDP_InfantMortality.update_layout({'title':{'text':'Relatie tussen GDP en kindersterfte', 
                                                               'x':0.5}})
    
st.plotly_chart(fig_scatter_GDP_InfantMortality)



fig_scatter_GDP_Phones = px.scatter(data_frame=who_data,
                x='GDP ($ per capita)',
                y='Phones (per 1000)',
                trendline='ols',
                trendline_color_override="red")

fig_scatter_GDP_Phones.update_xaxes(title_text = 'GDP ($ per inwoner)')
fig_scatter_GDP_Phones.update_yaxes(title_text = 'Aantal telefoons (per 1000 inwoners)')
fig_scatter_GDP_Phones.update_layout({'title':{'text':'Relatie tussen GDP en aantal telefoons per 1000 inwoners', 
                                                      'x':0.5}})
    
st.plotly_chart(fig_scatter_GDP_Phones)



fig_scatter_GDP_Literacy = px.scatter(data_frame=who_data,
                x='GDP ($ per capita)',
                y='Literacy (%)',
                trendline='ols',
                trendline_options=dict(log_x=True),
                trendline_color_override="red")

fig_scatter_GDP_Literacy.update_xaxes(title_text = 'GDP ($ per inwoner)')
fig_scatter_GDP_Literacy.update_yaxes(title_text = 'Geletterdheid (in %)')
fig_scatter_GDP_Literacy.update_layout({'title':{'text':'Relatie tussen GDP en de geletterdheid', 
                                                        'x':0.5}})
    
st.plotly_chart(fig_scatter_GDP_Literacy)






# Creeren van kaarten
# Wereld
m = folium.Map(zoom_control = True,
tiles = 'cartodb positron')

m.choropleth(
    geo_data = WHO,
    name = 'geometry',
    data = WHO,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(m)

# Asia
mASIA = folium.Map(zoom_control = False, zoom_start=3, location=[28.0893191, 105.1101691],
tiles = 'cartodb positron')

mASIA.choropleth(
    geo_data = ASIA,
    name = 'geometry',
    data = ASIA,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mASIA)

#Europe
mEUROPE = folium.Map(zoom_control = False, zoom_start=3, location=[54.0893191, 25.1101691],
tiles = 'cartodb positron')

mEUROPE.choropleth(
    geo_data = EUROPE,
    name = 'geometry',
    data = EUROPE,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mEUROPE)

#Africa
mAFRICA = folium.Map(zoom_control = False, zoom_start=3, location=[0.0893191, 15.1101691],
tiles = 'cartodb positron')

mAFRICA.choropleth(
    geo_data = AFRICA,
    name = 'geometry',
    data = AFRICA,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mAFRICA)

#Oceania
mOCEANIA = folium.Map(zoom_control = False, zoom_start=3, location=[-35.0893191, 140.1101691],
tiles = 'cartodb positron')

mOCEANIA.choropleth(
    geo_data = OCEANIA,
    name = 'geometry',
    data = OCEANIA,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mOCEANIA)

#Latin America
mLATINAMERICA = folium.Map(zoom_control = False, zoom_start=3, location=[-18, -60.1101691],
tiles = 'cartodb positron')

mLATINAMERICA.choropleth(
    geo_data = LATINAMERICA,
    name = 'geometry',
    data = LATINAMERICA,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mLATINAMERICA)

#Commonwealth of independant states (CIS)
mCIS = folium.Map(zoom_control = False, zoom_start=3, location=[65.0893191, 100.1101691],
tiles = 'cartodb positron')

mCIS.choropleth(
    geo_data = CIS,
    name = 'geometry',
    data = CIS,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mCIS)

#Middle east
mMIDDLEEAST = folium.Map(zoom_control = False, zoom_start=4, location=[30.0893191, 45.1101691],
tiles = 'cartodb positron')

mMIDDLEEAST.choropleth(
    geo_data = MIDDLEEAST,
    name = 'geometry',
    data = MIDDLEEAST,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mMIDDLEEAST)

#Noth America
mNORTHERNAMERICA = folium.Map(zoom_control = False, zoom_start=2, location=[70.0893191, -110.1101691],
tiles = 'cartodb positron')

mNORTHERNAMERICA.choropleth(
    geo_data = NORTHERNAMERICA,
    name = 'geometry',
    data = NORTHERNAMERICA,
    columns = ["Country", "GDP ($ per capita)"],
    key_on = 'feature.properties.Country',
    line_opacity = 0.5,
    fill_opacity = 0.75,
    fill_color = 'YlOrRd',
    legend_name = "GDP ($ per capita)")

folium_static(mNORTHERNAMERICA)






# Leeftijds piramide
country_input = 'Belgium'

y_range = world_age_categories[world_age_categories['Country']==country_input]['Age']
men = world_age_categories[world_age_categories['Country']==country_input]['Perc_men']
women = world_age_categories[world_age_categories['Country']==country_input]['Perc_women']

layout_range = [-round(men.max(),0)-2, round(women.max(),0)+2]
layout_tick_vals = [-round(men.max(),0), -round(men.max()/2,0) , 0 , round(women.max()/2,0) , round(women.max(),0)]
layout_tick_text = [-round(men.max(),0), -round(men.max()/2,0) , 0 , round(women.max()/2,0) , round(women.max(),0)]

layout = go.Layout(yaxis=go.layout.YAxis(title='Leeftijd'),
                   xaxis=go.layout.XAxis(
                       range=layout_range,
                       tickvals=layout_tick_vals,
                       ticktext=layout_tick_text,
                       title='Percentage van de bevolking'),
                   title={'text': 'Verdeling van de bevolking over leeftijds categorieën', 'x' : 0.5},
                   barmode='overlay',
                   bargap=0.1)

data = [go.Bar(y=y_range,
               x=-men,
               orientation='h',
               name='Men',
               text= men.astype('float'),
               textposition='outside',
               hoverinfo= 'text',
               marker=dict(color='powderblue')
               ),
        go.Bar(y=y_range,
               x=women,
               orientation='h',
               name='Women',
               text= women.astype('float'),
               textposition='outside',
               hoverinfo= 'text',
               marker=dict(color='hotpink')
               )]

st.plotly_chart(pyo.iplot(dict(data=data, layout=layout)))


