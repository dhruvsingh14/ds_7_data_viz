###############################
# Week 3.3: Data Viz Project  #
###############################

# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

########################
# Q1: Reading the Data #
########################
# loading csv file from online
file_name = 'https://cocl.us/datascience_survey_data/Topic_Survey_Assignment.csv'

# setting col 1 into index
df = pd.read_csv(file_name, index_col=0)
df

#########################################################
# Q2: Using artist layer to render barplots accordingly #
#########################################################

# Sorting df in order of interest
df.sort_values('Very interested', ascending=False, inplace=True)

# converting numbers into percentages
df['Very interested'] = (df['Very interested']/2233)*100
df['Somewhat interested'] = (df['Somewhat interested']/2233)*100
df['Not interested'] = (df['Not interested']/2233)*100

df = df.round({"Very interested":2, "Somewhat interested":2, "Not interested":2})
df

"""
ax = df.plot(kind='bar',
            figsize=(20, 8),
            width = 0.8, # altering bar width
            color=['#5cb85c', '#5bc0de', '#d9534f']) # using diff color for each type
ax.set_title('Interest in Analytics Areas of Expertise', fontsize=16)
ax.set_ylabel('Data Science Category', fontsize=14)
ax.set_xlabel('Numbers of People Interested', fontsize=14)
plt.show()
"""

#####################
# Q3: SF Crime Data #
#####################
# loading csv file from online
file_name = 'https://cocl.us/sanfran_crime_dataset/Police_Department_Incidents_-_Previous_Year__2016_.csv'

# setting col 1 into index
sf_crime_data = pd.read_csv(file_name, index_col=0)
sf_crime_data.head()

sf_crime_agg = sf_crime_data[['PdDistrict', 'Category']]
sf_crime_agg.columns = ['Neighborhood', 'Count']

sf_crime_agg = sf_crime_agg.groupby('Neighborhood').count()
sf_crime_agg.sort_values(['Count'], ascending=False, axis=0, inplace=True)

sf_crime_agg

#####################
# Q4: SF Crime Choropleth #
#####################
import wget
import folium
from folium import plugins

# downloading GeoJson file using wget
# url = 'https://cocl.us/sanfran_geojson/san-francisco.geojson'
# wget.download(url, 'san-francisco.geojson')

"""
# geojson file being read in
sf_crime_map = r'san-francisco.geojson'
sf_crime_map = folium.Map(location=[37.77,-122.42], zoom_start=12, tiles='Mapbox Bright')

sf_crime_map
sf_crime_map.save('sf_crime_map.html')


# generating choropleth map for sf crime rates
folium.Choropleth(
    geo_data=sf_crime_map,
    #data=sf_crime_agg,
    #columns=['Neighborhood', 'Count'],
    #key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Crime Rates in San Francisco'
).add_to(sf_crime_map)

# displaying map
sf_crime_map
sf_crime_map.save('sf_crime_map.html')
"""

latitude = 37.77
longitude = -122.42

# creating a map and visualizing it
sf_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# displaying the map of sf, iteration 1
sf_map
sf_map.save('sf_map.html')
# the higher zoom helped us see the urban landscape more clearly


"""
# geojson file being read in
sf_crime_map = r'san-francisco.geojson'

# creating a numpy array spaced from min_immig to max_immig
threshold_scale = np.linspace(sf_crime_agg['Count'].min(),
                              sf_crime_agg['Count'].min(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist() # converting the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1 # making sure last value of list exceeds max val

# allowing folium to compute scale
sf_crime_map = folium.Map(location=[37.77,-122.42], zoom_start=12, tiles='Mapbox Bright')
folium.Choropleth(
    geo_data=sf_crime_map,
    data=sf_crime_agg,
    columns=['Neighborhood', 'Count'],
    key_on='feature.properties.name',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Crime Rates in San Francisco',
    reset=True
).add_to(sf_crime_map)

# displaying map
sf_crime_map
sf_crime_map.save('sf_crime_map.html')
"""






















# in order to display plot within window
# plt.show()
