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
st.markdown("<h1 style='text-align: center; color: black;'>(Kinder)sterfte in de wereld</h1>", unsafe_allow_html=True)
st.markdown('***')

st.markdown('''

Welkom op dit interactieve dashboard!

In dit dashboard kijken we naar de relaties tussen (kinder)sterfte en GDP per regio. 
Alle visualisaties zijn interactief, wat inhoudt dat je precies kunt selecteren/filteren wat je wilt zien. 
Onder de visualisaties staat een box met "Meer informatie:" hier kun je op klikken om meer inzage te krijgen in de visualisaties en wat er nou precies wordt weergegeven.

''')



st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Boxplot</h3>", unsafe_allow_html=True)
st.markdown('***')



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
	
	remap = {"UnitedStates" : "UnitedStatesofAmerica", 
        	"Congo,Dem.Rep." : "DemocraticRepublicoftheCongo",
        	"Congo,Repub.ofthe" : "RepublicofCongo",
        	"Tanzania" : "UnitedRepublicofTanzania",
       		"CentralAfricanRep." : "CentralAfricanRepublic",
        	"Bosnia&Herzegovina":"BosniaandHerzegovina",
        	"Serbia":"RepublicofSerbia", 
        	"Korea,North" : "NorthKorea",
        	"Korea,South" : "SouthKorea"}
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
st.markdown("<h3 style='text-align: center; color: black;'>Spreidingsdiagram</h3>", unsafe_allow_html=True)
st.markdown('***')	


col1, col2 = st.columns(2)

fig_scatter_trend = col2.checkbox('Trendlijn', value=False)

if fig_scatter_trend == True:
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
if fig_scatter_trend == False:
	fig_scatter_GDP_InfantMortality = px.scatter(data_frame=WHO_data,
                x='GDP',
                y='Infant_mortality')

	fig_scatter_GDP_InfantMortality.update_xaxes(title_text = 'GDP ($ per inwoner)')
	fig_scatter_GDP_InfantMortality.update_yaxes(title_text = 'Kindersterfte (per 1000 geboortes)')
	fig_scatter_GDP_InfantMortality.update_layout({'title':{'text':'Relatie tussen GDP en kindersterfte', 
                                                               'x':0.5}})
    
	col1.plotly_chart(fig_scatter_GDP_InfantMortality)	


with st.expander('Meer informatie:'):
	st.subheader('Spreidingsdiagram extra informatie')
	st.markdown('''In dit spreidingsdiagram is de relatie tussen kindersterfte en GDP te zien. 
	In deze spreidingsdiagram is duidelijk zichtbaar dat het aannemelijk is dat als een land een hoge GDP heeft dat de kans op een hoge kindersterfte klein is. 
	Met de optie "Trendlijn" kan de trendlijn worden weergegeven.''')





st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Wereldkaart</h3>", unsafe_allow_html=True)
st.markdown('***')



col1, col2 = st.columns(2)

Kaart_variable_opties = col1.selectbox(label= 'Kies een variable:' , options= ['GDP' , 'Sterfgevallen' , 'Kindersterfte'])
kaart_opties = col2.selectbox(label= 'Kies een regio:', options= ['Alles', 'Afrika', 'Asi??', 'Europa', 'Gemenebestand van onafhankelijke staten', 'Latijns-Amerika', 'Midden-Oosten','Noord-Amerika','Oceani??'])



style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}

highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

if Kaart_variable_opties == 'GDP':
	
	if kaart_opties == 'Alles':
		m = folium.Map(zoom_control = True, zoom_start=1, location=[50,0],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = WHO,
    		name = 'geometry',
    		data = WHO,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(m)
		
		Info_m = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		m.add_child(Info_m)	

		folium_static(m)
	

	if kaart_opties == 'Afrika':
		mAFRICA = folium.Map(zoom_control = False, zoom_start=3, location=[0.0893191, 15.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = AFRICA,
    		name = 'geometry',
    		data = AFRICA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mAFRICA)
			
		Info_mAFRICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mAFRICA.add_child(Info_mAFRICA)	

		folium_static(mAFRICA)

	if kaart_opties == 'Asi??':
		mASIA = folium.Map(zoom_control = False, zoom_start=3, location=[28.0893191, 105.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = ASIA,
    		name = 'geometry',
    		data = ASIA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mASIA)
			
		Info_mASIA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mASIA.add_child(Info_mASIA)	

		folium_static(mASIA)

	if kaart_opties == 'Europa':
		mEUROPE = folium.Map(zoom_control = False, zoom_start=3, location=[54.0893191, 25.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = EUROPE,
    		name = 'geometry',
    		data = EUROPE,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mEUROPE)
			
		Info_mEUROPE = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mEUROPE.add_child(Info_mEUROPE)	

		folium_static(mEUROPE)

	if kaart_opties == 'Gemenebestand van onafhankelijke staten':
		mCIS = folium.Map(zoom_control = False, zoom_start=2, location=[65.0893191, 100.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = CIS,
    		name = 'geometry',
    		data = CIS,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mCIS)
			
		Info_mCIS = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mCIS.add_child(Info_mCIS)	

		folium_static(mCIS)

	if kaart_opties == 'Latijns-Amerika':
		mLATINAMERICA = folium.Map(zoom_control = False, zoom_start=3, location=[-18, -60.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = LATINAMERICA,
    		name = 'geometry',
    		data = LATINAMERICA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mLATINAMERICA)
			
		Info_mLATINAMERICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mLATINAMERICA.add_child(Info_mLATINAMERICA)	

		folium_static(mLATINAMERICA)

	if kaart_opties == 'Midden-Oosten':
		mMIDDLEEAST = folium.Map(zoom_control = False, zoom_start=4, location=[30.0893191, 45.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = MIDDLEEAST,
    		name = 'geometry',
    		data = MIDDLEEAST,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mMIDDLEEAST)
			
		Info_mMIDDLEEAST = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mMIDDLEEAST.add_child(Info_mMIDDLEEAST)	

		folium_static(mMIDDLEEAST)

	if kaart_opties == 'Noord-Amerika':
		mNORTHERNAMERICA = folium.Map(zoom_control = False, zoom_start=2, location=[70.0893191, -110.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = NORTHERNAMERICA,
    		name = 'geometry',
    		data = NORTHERNAMERICA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mNORTHERNAMERICA)
			
		Info_mNORTHERNAMERICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mNORTHERNAMERICA.add_child(Info_mNORTHERNAMERICA)	

		folium_static(mNORTHERNAMERICA)

	if kaart_opties == 'Oceani??':
		mOCEANIA = folium.Map(zoom_control = False, zoom_start=3, location=[-35.0893191, 140.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = OCEANIA,
    		name = 'geometry',
    		data = OCEANIA,
    		columns = ["Country", "GDP"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "GDP ($ per capita)").add_to(mOCEANIA)
			
		Info_mOCEANIA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'GDP'],
                           aliases=['Land: ','GDP: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mOCEANIA.add_child(Info_mOCEANIA)	

		folium_static(mOCEANIA)

if Kaart_variable_opties == 'Sterfgevallen':
	
	if kaart_opties == 'Alles':
		m = folium.Map(zoom_control = True, zoom_start=1, location=[50,0],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = WHO,
    		name = 'geometry',
    		data = WHO,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(m)
			
		Info_m = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		m.add_child(Info_m)	

		folium_static(m)
	

	if kaart_opties == 'Afrika':
		mAFRICA = folium.Map(zoom_control = False, zoom_start=3, location=[0.0893191, 15.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = AFRICA,
    		name = 'geometry',
    		data = AFRICA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mAFRICA)
			
		Info_mAFRICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mAFRICA.add_child(Info_mAFRICA)	

		folium_static(mAFRICA)

	if kaart_opties == 'Asi??':
		mASIA = folium.Map(zoom_control = False, zoom_start=3, location=[28.0893191, 105.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = ASIA,
    		name = 'geometry',
    		data = ASIA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mASIA)
			
		Info_mASIA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mASIA.add_child(Info_mASIA)	

		folium_static(mASIA)

	if kaart_opties == 'Europa':
		mEUROPE = folium.Map(zoom_control = False, zoom_start=3, location=[54.0893191, 25.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = EUROPE,
    		name = 'geometry',
    		data = EUROPE,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mEUROPE)
			
		Info_mEUROPE = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mEUROPE.add_child(Info_mEUROPE)	

		folium_static(mEUROPE)

	if kaart_opties == 'Gemenebestand van onafhankelijke staten':
		mCIS = folium.Map(zoom_control = False, zoom_start=2, location=[65.0893191, 100.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = CIS,
    		name = 'geometry',
    		data = CIS,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mCIS)
			
		Info_mCIS = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mCIS.add_child(Info_mCIS)	

		folium_static(mCIS)

	if kaart_opties == 'Latijns-Amerika':
		mLATINAMERICA = folium.Map(zoom_control = False, zoom_start=3, location=[-18, -60.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = LATINAMERICA,
    		name = 'geometry',
    		data = LATINAMERICA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mLATINAMERICA)
			
		Info_mLATINAMERICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mLATINAMERICA.add_child(Info_mLATINAMERICA)	

		folium_static(mLATINAMERICA)

	if kaart_opties == 'Midden-Oosten':
		mMIDDLEEAST = folium.Map(zoom_control = False, zoom_start=4, location=[30.0893191, 45.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = MIDDLEEAST,
    		name = 'geometry',
    		data = MIDDLEEAST,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mMIDDLEEAST)
			
		Info_mMIDDLEEAST = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mMIDDLEEAST.add_child(Info_mMIDDLEEAST)	

		folium_static(mMIDDLEEAST)

	if kaart_opties == 'Noord-Amerika':
		mNORTHERNAMERICA = folium.Map(zoom_control = False, zoom_start=2, location=[70.0893191, -110.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = NORTHERNAMERICA,
    		name = 'geometry',
    		data = NORTHERNAMERICA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mNORTHERNAMERICA)
			
		Info_mNORTHERNAMERICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mNORTHERNAMERICA.add_child(Info_mNORTHERNAMERICA)	

		folium_static(mNORTHERNAMERICA)

	if kaart_opties == 'Oceani??':
		mOCEANIA = folium.Map(zoom_control = False, zoom_start=3, location=[-35.0893191, 140.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = OCEANIA,
    		name = 'geometry',
    		data = OCEANIA,
    		columns = ["Country", "Deathrate"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Sterfgevallen (per 1.000 inwoners)").add_to(mOCEANIA)
			
		Info_mOCEANIA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Deathrate'],
                           aliases=['Land: ','Sterfgevallen: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mOCEANIA.add_child(Info_mOCEANIA)	

		folium_static(mOCEANIA)
		
if Kaart_variable_opties == 'Kindersterfte':
	
	if kaart_opties == 'Alles':
		m = folium.Map(zoom_control = True, zoom_start=1, location=[50,0],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = WHO,
    		name = 'geometry',
    		data = WHO,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(m)
			
		Info_m = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		m.add_child(Info_m)	

		folium_static(m)
	

	if kaart_opties == 'Afrika':
		mAFRICA = folium.Map(zoom_control = False, zoom_start=3, location=[0.0893191, 15.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = AFRICA,
    		name = 'geometry',
    		data = AFRICA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mAFRICA)
			
		Info_mAFRICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mAFRICA.add_child(Info_mAFRICA)	

		folium_static(mAFRICA)

	if kaart_opties == 'Asi??':
		mASIA = folium.Map(zoom_control = False, zoom_start=3, location=[28.0893191, 105.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = ASIA,
    		name = 'geometry',
    		data = ASIA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mASIA)
			
		Info_mASIA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mASIA.add_child(Info_mASIA)	

		folium_static(mASIA)

	if kaart_opties == 'Europa':
		mEUROPE = folium.Map(zoom_control = False, zoom_start=3, location=[54.0893191, 25.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = EUROPE,
    		name = 'geometry',
    		data = EUROPE,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mEUROPE)
			
		Info_mEUROPE = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mEUROPE.add_child(Info_mEUROPE)	

		folium_static(mEUROPE)

	if kaart_opties == 'Gemenebestand van onafhankelijke staten':
		mCIS = folium.Map(zoom_control = False, zoom_start=2, location=[65.0893191, 100.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = CIS,
    		name = 'geometry',
    		data = CIS,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mCIS)
			
		Info_mCIS = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mCIS.add_child(Info_mCIS)	

		folium_static(mCIS)

	if kaart_opties == 'Latijns-Amerika':
		mLATINAMERICA = folium.Map(zoom_control = False, zoom_start=3, location=[-18, -60.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = LATINAMERICA,
    		name = 'geometry',
    		data = LATINAMERICA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mLATINAMERICA)
			
		Info_mLATINAMERICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mLATINAMERICA.add_child(Info_mLATINAMERICA)	

		folium_static(mLATINAMERICA)

	if kaart_opties == 'Midden-Oosten':
		mMIDDLEEAST = folium.Map(zoom_control = False, zoom_start=4, location=[30.0893191, 45.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = MIDDLEEAST,
    		name = 'geometry',
    		data = MIDDLEEAST,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mMIDDLEEAST)
			
		Info_mMIDDLEEAST = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mMIDDLEEAST.add_child(Info_mMIDDLEEAST)	

		folium_static(mMIDDLEEAST)

	if kaart_opties == 'Noord-Amerika':
		mNORTHERNAMERICA = folium.Map(zoom_control = False, zoom_start=2, location=[70.0893191, -110.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = NORTHERNAMERICA,
    		name = 'geometry',
    		data = NORTHERNAMERICA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mNORTHERNAMERICA)
			
		Info_mNORTHERNAMERICA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mNORTHERNAMERICA.add_child(Info_mNORTHERNAMERICA)	

		folium_static(mNORTHERNAMERICA)

	if kaart_opties == 'Oceani??':
		mOCEANIA = folium.Map(zoom_control = False, zoom_start=3, location=[-35.0893191, 140.1101691],
		tiles = 'cartodb positron')

		folium.Choropleth(
    		geo_data = OCEANIA,
    		name = 'geometry',
    		data = OCEANIA,
    		columns = ["Country", "Infant_mortality"],
    		key_on = 'feature.properties.Country',
    		line_opacity = 0.5,
    		fill_opacity = 0.75,
    		fill_color = 'YlOrRd',
    		legend_name = "Kindersterfte (per 1.000 geboortes)").add_to(mOCEANIA)
			
		Info_mOCEANIA = folium.features.GeoJson(
                           WHO,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['Country', 'Infant_mortality'],
                           aliases=['Land: ','Kindersterfte: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
		mOCEANIA.add_child(Info_mOCEANIA)	

		folium_static(mOCEANIA)		

with st.expander('Meer informatie:'):
	st.subheader('Wereldkaart extra informatie')
	st.markdown('''In deze visualisatie is de wereldkaart te zien. 
	Je kunt de variabelen kindersterfte, sterfgevallen en GDP selecteren in de linker dropdown menu en aan de rechterkant kan je selecteren van welke regio de data wilt zien. 
	In de legenda is te zien hoe donkerder rood de kleur is hoe hoger de waardes zijn. De kleuren worden bepaald op basis van de data die is aangevinkt, 
	dus als bijvoorbeeld alleen Europa is aangeklikt als regio dan wordt de donkerheid bepaald aan de hand van alleen de landen in Europa.''')



st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Histogram van de leeftijdsverdeling per land</h3>", unsafe_allow_html=True)
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

fig_bar_population.update_layout(title={'text': 'Populatie piramide van '+str(country_input), 'x' : 0.5},
                 xaxis={'range':layout_range,
                       'tickvals':layout_tick_vals,
                       'ticktext':layout_tick_text,
                       'title':'Percentage van de bevolking'},
                 yaxis={'title':'Leeftijd'},
                 barmode='overlay',
                 bargap=0.1,
                 hovermode='x',
                 colorway=['powderblue','hotpink']
                 )               

st.plotly_chart(fig_bar_population)



with st.expander('Meer informatie:'):
	st.subheader('Leeftijdspiramide extra informatie')
	st.markdown('''De Leeftijdspiramide geeft weer hoe de leeftijd binnen een bepaald land is opgebouwd. 
		     Dit wordt gedaan door het land in verschillende leeftijdscategorie??n op te delen.
		     Daarna wordt het percentage van de bevolking berekend dat zich in elke leeftijdscategorie bevind.
		     Een gezonde bevolking heeft in elke leeftijdscategorie hetzelfde percentage zitten.
		     Als de lagere categorie??n een hoog percentage hebben dan heeft het land te maken met 
		     veel geboortes of veel sterfgevallen. Als de hogere categorie??n een hoog percentage hebben
		     dan betekend dit dat er weinig geboortes zijn en dus dat de bevolking vergrijsd''')
	

	
st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Kindersterfte linear model</h3>", unsafe_allow_html=True)
st.markdown('***')	

fig_linearmodel_trend = st.checkbox('Trendlijn', value=True)

col1, col2 = st.columns(2)

if fig_linearmodel_trend == True:
	fig_linearmodel = go.Figure()
	fig_linearmodel = px.scatter(x='GDP', y='Infant_mortality', data_frame=WHO_data, trendline='ols', trendline_color_override='red')
	fig_linearmodel.update_xaxes(title_text = 'GDP')
	fig_linearmodel.update_yaxes(title_text = 'Kindersterfte (per 1.000 geboortes)')
	fig_linearmodel.update_layout({'title':{'text':'Relatie kindersterfte en GDP', 
                            'x':0.5}})
	col1.plotly_chart(fig_linearmodel)

	with col1.expander('Model samenvatting:'):
		model_infant = ols('Infant_mortality ~ GDP ', data=WHO_data).fit()
		st.write(model_infant.summary())

	fig_linearmodel_log = go.Figure()
	fig_linearmodel_log = px.scatter(x='GDP', y='Infant_log', data_frame=WHO_data, trendline='ols', trendline_color_override='red')
	fig_linearmodel_log.update_xaxes(title_text = 'GDP')
	fig_linearmodel_log.update_yaxes(title_text = 'Kindersterfte (per 1.000 geboortes) in logaritmische schaal')
	fig_linearmodel_log.update_layout({'title':{'text':'Relatie kindersterfte en GDP', 
                            'x':0.5}})
	col2.plotly_chart(fig_linearmodel_log)

	with col2.expander('Model samenvatting:'):
		model_infant_log = ols('Infant_log ~ GDP ', data=WHO_data).fit()
		st.write(model_infant_log.summary())
		
if fig_linearmodel_trend == False:
	fig_linearmodel = go.Figure()
	fig_linearmodel = px.scatter(x='GDP', y='Infant_mortality', data_frame=WHO_data)
	fig_linearmodel.update_xaxes(title_text = 'GDP')
	fig_linearmodel.update_yaxes(title_text = 'Kindersterfte (per 1.000 geboortes)')
	fig_linearmodel.update_layout({'title':{'text':'Relatie kindersterfte en GDP', 
                            'x':0.5}})
	col1.plotly_chart(fig_linearmodel)

	with col1.expander('Model samenvatting:'):
		model_infant = ols('Infant_mortality ~ GDP ', data=WHO_data).fit()
		st.write(model_infant.summary())

	fig_linearmodel_log = go.Figure()
	fig_linearmodel_log = px.scatter(x='GDP', y='Infant_log', data_frame=WHO_data)
	fig_linearmodel_log.update_xaxes(title_text = 'GDP')
	fig_linearmodel_log.update_yaxes(title_text = 'Kindersterfte (per 1.000 geboortes) in logaritmische schaal')
	fig_linearmodel_log.update_layout({'title':{'text':'Relatie kindersterfte en GDP', 
                            'x':0.5}})
	col2.plotly_chart(fig_linearmodel_log)

	with col2.expander('Model samenvatting:'):
		model_infant_log = ols('Infant_log ~ GDP ', data=WHO_data).fit()
		st.write(model_infant_log.summary())		

with st.expander('Meer informatie:'):
	st.subheader('Linear model extra informatie')
	st.markdown('''Aan de linkerkant staat een grafiek met de relatie tussen kindersterfte en GDP. 
	Hierop is een voorspellingsmodel toegepast en zoals te zien is bij de samenvatting van het model heeft deze een R-squared van 0,38. 
	Aan de rechterkant is ook een grafiek weergegeven met dezelfde relatie als de linker grafiek, alleen hier staan de waardes op een logaritmische schaal. 
	Ook op de rechter grafiek is een voorspellingsmodel toegepast, deze geeft een R-squared 0,65. Dit is een significante verbetering van het model. 
	Met dit model kan dus op een goede manier de kindersterfte voorspeld worden aan de hand van het GDP.''')		
		

	
st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Bronnen</h3>", unsafe_allow_html=True)
st.markdown('***')	

st.markdown(''' 
https://www.populationpyramid.net/

https://www.who.int/data/collections

https://datahub.io/core/geo-countries
''')

st.markdown('''




Gemaakt door:

- Jelle Aardema 500815973
- Daan Bouwmeester 500826025
''')
