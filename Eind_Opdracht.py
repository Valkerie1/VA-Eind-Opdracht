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

st.markdown('***')
st.markdown("<h1 style='text-align: center; color: black;'>Levensverwachting over de wereld</h1>", unsafe_allow_html=True)
st.markdown('***')

st.markdown('''

beetje text

''')






@st.cache
def load_who_data():
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
	who_data['Country'] = who_data['Country'].str.replace(' ','')
	
	remap = {"UnitedStates" : "UnitedStatesofAmerica"}
	who_data['Country'] = who_data['Country'].replace(remap)
	
	who_data.rename({'GDP ($ per capita)':'GDP', 'Infant mortality (per 1000 births)':'Infant_mortality','Phones (per 1000)':'Phones'},axis=1,inplace=True)
	who_data.drop(who_data[who_data['GDP']>50000].index,inplace=True)
	who_data['Infant_log'] = np.log(who_data['Infant_mortality'])
	return who_data

WHO_data = load_who_data()



# Inladen van geojson data + bewerking
countries = gpd.read_file('countries.geojson')
#who_data['Country'] = who_data['Country'].str.replace(' ','')
countries['ADMIN'] = countries['ADMIN'].str.replace(' ','')

#remap = {"UnitedStates" : "UnitedStatesofAmerica"}
#who_data['Country'] = who_data['Country'].replace(remap)

WHO = gpd.GeoDataFrame(pd.merge(WHO_data, countries, 
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







boxplot_selectbox = st.selectbox(label='', options=['Sterfgevallen per regio' , 'Kindersterfte per regio' , 'GDP per regio']) 

if boxplot_selectbox == 'GDP per regio':
	fig_boxplot_gdp = px.box(data_frame=WHO_data, x=WHO_data['Region'], y='GDP', 
             color='Region')
	fig_boxplot_gdp.update_xaxes(title_text = 'Regio')
	fig_boxplot_gdp.update_yaxes(title_text = 'GDP ($ per inwoner)')
	fig_boxplot_gdp.update_layout({'title':{'text':'GDP per regio', 
                            'x':0.5}})
	st.plotly_chart(fig_boxplot_gdp)

if boxplot_selectbox == 'Sterfgevallen per regio':
	fig_boxplot_sterfgevallen = px.box(data_frame=WHO_data, x=WHO_data['Region'], y='Deathrate', 
             color='Region')
	fig_boxplot_sterfgevallen.update_xaxes(title_text = 'Regio')
	fig_boxplot_sterfgevallen.update_yaxes(title_text = 'Sterfgevallen (per 1.000 inwoners)')
	fig_boxplot_sterfgevallen.update_layout({'title':{'text':'Sterfgevallen per regio', 
                            'x':0.5}})
	st.plotly_chart(fig_boxplot_sterfgevallen)

if boxplot_selectbox == 'Kindersterfte per regio':
	fig_boxplot_kindersterfte = px.box(data_frame=WHO_data, x=WHO_data['Region'], y='Infant_mortality', 
             color='Region')
	fig_boxplot_kindersterfte.update_xaxes(title_text = 'Regio')
	fig_boxplot_kindersterfte.update_yaxes(title_text = 'Kindersterfte (per 1.000 geboortes)')
	fig_boxplot_kindersterfte.update_layout({'title':{'text':'Kindersterfte per regio', 
                            'x':0.5}})
	st.plotly_chart(fig_boxplot_kindersterfte)



with st.expander('Meer informatie:'):
	st.subheader('Boxplot extra informatie')
	st.markdown('''De boxplots geven informatie weer voor 8 regio's op de wereld. 
		     De weergegeven waardes zijn het gemiddelde van de landen die zich binnen dezelfde regio bevinden.''')

	
	
st.markdown('***')	


col1, col2 = st.columns(2)

fig_scatter_GDP_InfantMortality = px.scatter(data_frame=WHO_data,
                x='GDP',
                y='Infant_mortality',
                trendline='ols', 
                trendline_options=dict(log_y=True),
                trendline_color_override="red")

fig_scatter_GDP_InfantMortality.update_xaxes(title_text = 'GDP ($ per inwoner)')
fig_scatter_GDP_InfantMortality.update_yaxes(title_text = 'Kindersterfte (per 1000 geboortes)')
fig_scatter_GDP_InfantMortality.update_layout({'title':{'text':'Relatie tussen GDP en kindersterfte', 
                                                               'x':0.5}})
    
col1.plotly_chart(fig_scatter_GDP_InfantMortality)


fig_scatter_GDP_Literacy = px.scatter(data_frame=WHO_data,
                x='GDP',
                y='Literacy (%)',
                trendline='ols',
                trendline_options=dict(log_x=True),
                trendline_color_override="red")

fig_scatter_GDP_Literacy.update_xaxes(title_text = 'GDP ($ per inwoner)')
fig_scatter_GDP_Literacy.update_yaxes(title_text = 'Geletterdheid (in %)')
fig_scatter_GDP_Literacy.update_layout({'title':{'text':'Relatie tussen GDP en de geletterdheid', 
                                                        'x':0.5}})
    
col2.plotly_chart(fig_scatter_GDP_Literacy)






st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Wereldkaart</h3>", unsafe_allow_html=True)
st.markdown('***')



col1, col2 = st.columns(2)

Kaart_variable_opties = col1.selectbox(label= 'Kies een variable:' , options= ['GDP' , 'Sterfgevallen' , 'Kindersterfte'])
kaart_opties = col2.selectbox(label= 'Kies een regio:', options= ['Alles', 'Afrika', 'Asië', 'Europa', 'Gemenebestand van onafhankelijke staten', 'Latijns-Amerika', 'Midden-Oosten','Noord-Amerika','Oceanië'])


if Kaart_variable_opties == 'GDP':
	
	if kaart_opties == 'Alles':
		m = folium.Map(zoom_control = True, zoom_start=1, location=[50,0],
		tiles = 'cartodb positron')

		m.choropleth(
    		geo_data = WHO,
    		name = 'geometry',
    		data = WHO,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(m)
	

	if kaart_opties == 'Afrika':
		mAFRICA = folium.Map(zoom_control = False, zoom_start=3, location=[0.0893191, 15.1101691],
		tiles = 'cartodb positron')

		mAFRICA.choropleth(
    		geo_data = AFRICA,
    		name = 'geometry',
    		data = AFRICA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mAFRICA)

	if kaart_opties == 'Asië':
		mASIA = folium.Map(zoom_control = False, zoom_start=3, location=[28.0893191, 105.1101691],
		tiles = 'cartodb positron')

		mASIA.choropleth(
    		geo_data = ASIA,
    		name = 'geometry',
    		data = ASIA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mASIA)

	if kaart_opties == 'Europa':
		mEUROPE = folium.Map(zoom_control = False, zoom_start=3, location=[54.0893191, 25.1101691],
		tiles = 'cartodb positron')

		mEUROPE.choropleth(
    		geo_data = EUROPE,
    		name = 'geometry',
    		data = EUROPE,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mEUROPE)

	if kaart_opties == 'Gemenebestand van onafhankelijke staten':
		mCIS = folium.Map(zoom_control = False, zoom_start=2, location=[65.0893191, 100.1101691],
		tiles = 'cartodb positron')

		mCIS.choropleth(
    		geo_data = CIS,
    		name = 'geometry',
    		data = CIS,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mCIS)

	if kaart_opties == 'Latijns-Amerika':
		mLATINAMERICA = folium.Map(zoom_control = False, zoom_start=3, location=[-18, -60.1101691],
		tiles = 'cartodb positron')

		mLATINAMERICA.choropleth(
    		geo_data = LATINAMERICA,
    		name = 'geometry',
    		data = LATINAMERICA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mLATINAMERICA)

	if kaart_opties == 'Midden-Oosten':
		mMIDDLEEAST = folium.Map(zoom_control = False, zoom_start=4, location=[30.0893191, 45.1101691],
		tiles = 'cartodb positron')

		mMIDDLEEAST.choropleth(
    		geo_data = MIDDLEEAST,
    		name = 'geometry',
    		data = MIDDLEEAST,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mMIDDLEEAST)

	if kaart_opties == 'Noord-Amerika':
		mNORTHERNAMERICA = folium.Map(zoom_control = False, zoom_start=2, location=[70.0893191, -110.1101691],
		tiles = 'cartodb positron')

		mNORTHERNAMERICA.choropleth(
    		geo_data = NORTHERNAMERICA,
    		name = 'geometry',
    		data = NORTHERNAMERICA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mNORTHERNAMERICA)

	if kaart_opties == 'Oceanië':
		mOCEANIA = folium.Map(zoom_control = False, zoom_start=3, location=[-35.0893191, 140.1101691],
		tiles = 'cartodb positron')

		mOCEANIA.choropleth(
    		geo_data = OCEANIA,
    		name = 'geometry',
    		data = OCEANIA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)")

		folium_static(mOCEANIA)

if Kaart_variable_opties == 'Sterfgevallen':
	
	if kaart_opties == 'Alles':
		m = folium.Map(zoom_control = True, zoom_start=1, location=[50,0],
		tiles = 'cartodb positron')

		m.choropleth(
    		geo_data = WHO,
    		name = 'geometry',
    		data = WHO,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(m)
	

	if kaart_opties == 'Afrika':
		mAFRICA = folium.Map(zoom_control = False, zoom_start=3, location=[0.0893191, 15.1101691],
		tiles = 'cartodb positron')

		mAFRICA.choropleth(
    		geo_data = AFRICA,
    		name = 'geometry',
    		data = AFRICA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mAFRICA)

	if kaart_opties == 'Asië':
		mASIA = folium.Map(zoom_control = False, zoom_start=3, location=[28.0893191, 105.1101691],
		tiles = 'cartodb positron')

		mASIA.choropleth(
    		geo_data = ASIA,
    		name = 'geometry',
    		data = ASIA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mASIA)

	if kaart_opties == 'Europa':
		mEUROPE = folium.Map(zoom_control = False, zoom_start=3, location=[54.0893191, 25.1101691],
		tiles = 'cartodb positron')

		mEUROPE.choropleth(
    		geo_data = EUROPE,
    		name = 'geometry',
    		data = EUROPE,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mEUROPE)

	if kaart_opties == 'Gemenebestand van onafhankelijke staten':
		mCIS = folium.Map(zoom_control = False, zoom_start=2, location=[65.0893191, 100.1101691],
		tiles = 'cartodb positron')

		mCIS.choropleth(
    		geo_data = CIS,
    		name = 'geometry',
    		data = CIS,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mCIS)

	if kaart_opties == 'Latijns-Amerika':
		mLATINAMERICA = folium.Map(zoom_control = False, zoom_start=3, location=[-18, -60.1101691],
		tiles = 'cartodb positron')

		mLATINAMERICA.choropleth(
    		geo_data = LATINAMERICA,
    		name = 'geometry',
    		data = LATINAMERICA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mLATINAMERICA)

	if kaart_opties == 'Midden-Oosten':
		mMIDDLEEAST = folium.Map(zoom_control = False, zoom_start=4, location=[30.0893191, 45.1101691],
		tiles = 'cartodb positron')

		mMIDDLEEAST.choropleth(
    		geo_data = MIDDLEEAST,
    		name = 'geometry',
    		data = MIDDLEEAST,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mMIDDLEEAST)

	if kaart_opties == 'Noord-Amerika':
		mNORTHERNAMERICA = folium.Map(zoom_control = False, zoom_start=2, location=[70.0893191, -110.1101691],
		tiles = 'cartodb positron')

		mNORTHERNAMERICA.choropleth(
    		geo_data = NORTHERNAMERICA,
    		name = 'geometry',
    		data = NORTHERNAMERICA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mNORTHERNAMERICA)

	if kaart_opties == 'Oceanië':
		mOCEANIA = folium.Map(zoom_control = False, zoom_start=3, location=[-35.0893191, 140.1101691],
		tiles = 'cartodb positron')

		mOCEANIA.choropleth(
    		geo_data = OCEANIA,
    		name = 'geometry',
    		data = OCEANIA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)")

		folium_static(mOCEANIA)
		
if Kaart_variable_opties == 'Kindersterfte':
	
	if kaart_opties == 'Alles':
		m = folium.Map(zoom_control = True, zoom_start=1, location=[50,0],
		tiles = 'cartodb positron')

		m.choropleth(
    		geo_data = WHO,
    		name = 'geometry',
    		data = WHO,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(m)
	

	if kaart_opties == 'Afrika':
		mAFRICA = folium.Map(zoom_control = False, zoom_start=3, location=[0.0893191, 15.1101691],
		tiles = 'cartodb positron')

		mAFRICA.choropleth(
    		geo_data = AFRICA,
    		name = 'geometry',
    		data = AFRICA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mAFRICA)

	if kaart_opties == 'Asië':
		mASIA = folium.Map(zoom_control = False, zoom_start=3, location=[28.0893191, 105.1101691],
		tiles = 'cartodb positron')

		mASIA.choropleth(
    		geo_data = ASIA,
    		name = 'geometry',
    		data = ASIA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mASIA)

	if kaart_opties == 'Europa':
		mEUROPE = folium.Map(zoom_control = False, zoom_start=3, location=[54.0893191, 25.1101691],
		tiles = 'cartodb positron')

		mEUROPE.choropleth(
    		geo_data = EUROPE,
    		name = 'geometry',
    		data = EUROPE,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mEUROPE)

	if kaart_opties == 'Gemenebestand van onafhankelijke staten':
		mCIS = folium.Map(zoom_control = False, zoom_start=2, location=[65.0893191, 100.1101691],
		tiles = 'cartodb positron')

		mCIS.choropleth(
    		geo_data = CIS,
    		name = 'geometry',
    		data = CIS,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mCIS)

	if kaart_opties == 'Latijns-Amerika':
		mLATINAMERICA = folium.Map(zoom_control = False, zoom_start=3, location=[-18, -60.1101691],
		tiles = 'cartodb positron')

		mLATINAMERICA.choropleth(
    		geo_data = LATINAMERICA,
    		name = 'geometry',
    		data = LATINAMERICA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mLATINAMERICA)

	if kaart_opties == 'Midden-Oosten':
		mMIDDLEEAST = folium.Map(zoom_control = False, zoom_start=4, location=[30.0893191, 45.1101691],
		tiles = 'cartodb positron')

		mMIDDLEEAST.choropleth(
    		geo_data = MIDDLEEAST,
    		name = 'geometry',
    		data = MIDDLEEAST,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mMIDDLEEAST)

	if kaart_opties == 'Noord-Amerika':
		mNORTHERNAMERICA = folium.Map(zoom_control = False, zoom_start=2, location=[70.0893191, -110.1101691],
		tiles = 'cartodb positron')

		mNORTHERNAMERICA.choropleth(
    		geo_data = NORTHERNAMERICA,
    		name = 'geometry',
    		data = NORTHERNAMERICA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mNORTHERNAMERICA)

	if kaart_opties == 'Oceanië':
		mOCEANIA = folium.Map(zoom_control = False, zoom_start=3, location=[-35.0893191, 140.1101691],
		tiles = 'cartodb positron')

		mOCEANIA.choropleth(
    		geo_data = OCEANIA,
    		name = 'geometry',
    		data = OCEANIA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)")

		folium_static(mOCEANIA)		





st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Leeftijdspiramide per land</h3>", unsafe_allow_html=True)
st.markdown('***')


leeftijdspyramid_opties = st.selectbox(label='Kies een land:', options= world_age_categories['Country'].unique(), index=0)

country_input = leeftijdspyramid_opties

y_range = world_age_categories[world_age_categories['Country']==country_input]['Age']
men = world_age_categories[world_age_categories['Country']==country_input]['Perc_men']
women = world_age_categories[world_age_categories['Country']==country_input]['Perc_women']

layout_range = [-round(men.max(),0)-2, round(women.max(),0)+2]
layout_tick_vals = [-round(men.max(),0), -round(men.max()/2,0) , 0 , round(women.max()/2,0) , round(women.max(),0)]
layout_tick_text = [str(-round(men.max(),0))+'%', str(-round(men.max()/2,0))+'%' , str(0)+'%' , str(round(women.max()/2,0))+'%' , str(round(women.max(),0))+'%']

fig_bar_population = go.Figure()

fig_bar_population.add_trace(go.Bar(y=y_range, x=-men, name='Male', orientation = 'h'))
fig_bar_population.add_trace(go.Bar(y=y_range, x=women, name='Female', orientation = 'h'))

fig_bar_population.update_layout(title={'text': 'Population pyramid of '+str(country_input), 'x' : 0.5},
                 xaxis={'range':layout_range,
                       'tickvals':layout_tick_vals,
                       'ticktext':layout_tick_text,
                       'title':'Percentage van de bevolking'},
                 yaxis={'title':'Leeftijd'},
                 barmode='overlay',
                 bargap=0.1,
                 hovermode='x'
                 )               

st.plotly_chart(fig_bar_population)



with st.expander('Meer informatie:'):
	st.subheader('Leeftijdspiramide extra informatie')
	st.markdown('''De Leeftijdspiramide geeft weer hoe de leeftijd binnen een bepaald land is opgebouwd. 
		     Dit wordt gedaan door het land in verschillende leeftijdscategorieën op te delen.
		     Daarna wordt het percentage berekend dat zich in elke leeftijdscategorie bevind.
		     Een gezonde bevolking heeft in elke leeftijdscategorie het zelfde percentage zitten.
		     Als de lagere categorieën een hoog percentage hebben dan heeft het land te maken met 
		     veel geboortes of veel sterfgevallen. Als de hogere categorieën een hoog percentage hebben
		     dan betekend dit dat er weinig geboortes zijn en dus dat de bevolking vergrijsd''')
	

	
st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Kindersterfte linear model</h3>", unsafe_allow_html=True)
st.markdown('***')	

col1, col2 = st.columns(2)

fig_linearmodel = go.Figure()
fig_linearmodel = px.scatter(x='GDP', y='Infant_mortality', data_frame=WHO_data, trendline='ols', trendline_color_override='red')
fig_linearmodel.update_xaxes(title_text = 'GDP')
fig_linearmodel.update_yaxes(title_text = 'Kindersterfte (per 1.000 geboortes)')
fig_linearmodel.update_layout({'title':{'text':'Relatie kindersterfte en GDP', 
                            'x':0.5}})
col1.plotly_chart(fig_linearmodel)

with col1.expander('Meer informatie:'):
	model_infant = ols('Infant_mortality ~ GDP ', data=WHO_data).fit()
	st.write(model_infant.summary())

fig_linearmodel_log = go.Figure()
fig_linearmodel_log = px.scatter(x='GDP', y='Infant_log', data_frame=WHO_data, trendline='ols', trendline_color_override='red')
fig_linearmodel_log.update_xaxes(title_text = 'GDP')
fig_linearmodel_log.update_yaxes(title_text = 'Kindersterfte (per 1.000 geboortes) in logaritmische schaal')
fig_linearmodel_log.update_layout({'title':{'text':'Relatie kindersterfte en GDP', 
                            'x':0.5}})
col2.plotly_chart(fig_linearmodel_log)

with col2.expander('Meer informatie:'):
	model_infant_log = ols('Infant_log ~ GDP ', data=WHO_data).fit()
	st.write(model_infant_log.summary())

	
	
st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Bronnen</h3>", unsafe_allow_html=True)
st.markdown('***')	

st.markdown(''' 
https://www.populationpyramid.net/

https://www.who.int/data/collections
''')
	

