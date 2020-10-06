###################
# Week 3.2: Maps  #
###################
# importing libraries
import numpy as np
import pandas as pd
import folium

# print('Folium installed and imported!')

#########################
# Producing a World Map #
#########################
# defining the world map
world_map = folium.Map()

# displaying / saving the world map, iteration 1
world_map
world_map.save('world_map.html')

# recreating with a zoom in inplace, iteration 2
# centered on Canada's coordinates, upping the zoom to focus in
world_map = folium.Map(location=[56.130, -106.35], zoom_start=4)

# displaying world map of canada
world_map
world_map.save('world_map.html')

# finally, zooming in further on Canada, iteration 3
world_map = folium.Map(location=[56.130, -106.35], zoom_start=8)

# displaying world map of canada
world_map
world_map.save('world_map.html')

################################
# Q1: Creating a Map of Mexico #
################################

# rendering mexico map
mexico_map = folium.Map(location=[19.45105, -99.1255], zoom_start=4)

# displaying and saving mexico map
mexico_map
mexico_map.save('mexico_map.html')

########################
# A. Stamen Toner Maps #
########################

# creating a stamen toner map, centered on canada
world_map = folium.Map(location=[56.130, -106.35], zoom_start=4, tiles='Stamen Toner')

# displaying world map of canada
world_map
world_map.save('world_map.html')

##########################
# B. Stamen Terrain Maps #
##########################

# creating a stamen terrain map, centered on canada
world_map = folium.Map(location=[56.130, -106.35], zoom_start=4, tiles='Stamen Terrain')

# displaying world map of canada
world_map
world_map.save('world_map.html')

#########################
# C. Mapbox Bright Maps #
#########################

# creating a mapbox bright map
world_map = folium.Map(tiles='Mapbox Bright')

# displaying world map of canada
world_map
world_map.save('world_map.html')


# well this didn't render ^, neither here nor online

########################################
# Q2: Visualizing hill shading, Mexico #
########################################

# creating a stamen terrain map, centered on mexico
mexico_map = folium.Map(location=[19.45105, -99.1255], zoom_start=6, tiles='Stamen Terrain')

# displaying world map of canada
mexico_map
mexico_map.save('mexico_map.html')

#####################
# Maps with Markers #
#####################

df_incidents = pd.read_csv('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Police_Department_Incidents_-_Previous_Year__2016_.csv')
# print('Dataset downloaded and read into a pandas dataframe!')

# eda
df_incidents.head()
df_incidents.shape

# grabbing the first 100 rows using a global variable
limit = 100
df_incidents = df_incidents.iloc[0:limit, :]

df_incidents.shape # checking data dimensions

# shifting our focus to San Francisco
# starting w/ lat long variables
latitude = 37.77
longitude = -122.42

# creating a map and visualizing it
sf_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# displaying the map of sf, iteration 1
sf_map
sf_map.save('sf_map.html')
# the higher zoom helped us see the urban landscape more clearly


# iteration 2: adding markers

# declaring a feature group for plotting crime incidents, iteration 2
incidents = folium.map.FeatureGroup()

# looping through a 100 rows of crimes (each one a record)
# and adding these incidents to the folium feature group

for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        folium.CircleMarker(
            [lat, lng],
            radius=5, # defining size of circle markers
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# adding incidents to the map itself, iteration 2
sf_map.add_child(incidents)

# displaying the map of sf, iteration 2
sf_map
sf_map.save('sf_map.html')


# iteration 3: adding popup text

# declaring a new feature group, iteration 3
incidents = folium.map.FeatureGroup()

# looping through a 100 rows of crimes (each one a record)
# and adding these incidents to the folium feature group

for lat, lng, in zip(df_incidents.Y, df_incidents.X):
    incidents.add_child(
        folium.CircleMarker(
            [lat, lng],
            radius=5, # defining size of circle markers
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# adding pop up text
latitudes = list(df_incidents.Y)
longitudes = list(df_incidents.X)
labels = list(df_incidents.Category)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(sf_map)

# adding incidents to the map itself, iteration 3
sf_map.add_child(incidents)

# displaying the map of sf, iteration 3
sf_map
sf_map.save('sf_map.html')


# iteration 4: reducing clutter

# creating a map and visualizing it
sf_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# looping through a 100 rows of crimes (each one a record)
# and adding these incidents to the folium feature group
for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.CircleMarker(
        [lat, lng],
        radius=5, # defining size of circle markers
        color='yellow',
        fill=True,
        popup=label,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(sf_map)


# displaying the map of sf, iteration 4
sf_map
sf_map.save('sf_map.html')


from folium import plugins

# iteration 5, starting afresh with a clean copy of sf map

sf_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# declaring a cluster object for the incidents listed herein
incidents = plugins.MarkerCluster().add_to(sf_map)

# looping through a 100 rows of crimes (each one a record)
# and adding these incidents to the cluster group
for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.Marker(
        [lat, lng],
        icon=None,
        popup=label
    ).add_to(incidents)

# displaying the map of sf, iteration 4
sf_map
sf_map.save('sf_map.html')


###################
# Choropleth Maps #
###################
import xlrd
import wget

# reading in canada data again
df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2)

# print('Data read into a pandas dataframe!')

# checking first 5 rows
df_can.head()

# checking dimensions
df_can.shape

# dropping unnecessary columns
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)

# renaming column headers
df_can.rename(columns={'OdName': 'Country', 'AreaName':'Continent', 'RegName': 'Region'}, inplace=True)

# assigning column types to string
df_can.columns = list(map(str, df_can.columns))

# adding a column for total immigration for 1980-2013
df_can['Total'] = df_can.sum(axis=1)

# capturing list of years, for category visualization
years = list(map(str, range(1980, 2014)))

# print('data dimensions:', df_can.shape) # sick command for printing dimensionality

# printing head of dataset
df_can.head()

# downloading GeoJson file using wget
url = 'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/world_countries.json'
wget.download(url, 'world_countries.json')

# print('GeoJSON file downloaded!')

# geojson file being read in
world_geo = r'world_countries.json'

# iteration 1
# creating a simple world map

world_map = folium.Map(location=[0,0], zoom_start=2, tiles='Mapbox Bright')

world_map
world_map.save('world_map.html')

# generating choropleth map w/ total immigration for each country to canada, from 1980 - 2013

world_map.choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Immigration to Canada'
)

# displaying map
world_map
world_map.save('world_map.html')


# iteration 2
# geojson file being read in
world_geo = r'world_countries.json'

# creating a numpy array spaced from min_immig to max_immig
threshold_scale = np.linspace(df_can['Total'].min(),
                              df_can['Total'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist() # converting the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1 # making sure last value of list exceeds max val

# allowing folium to compute scale
world_map = folium.Map(location=[0,0], zoom_start=2, tiles='Mapbox Bright')
folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Immigration to Canada',
    reset=True
).add_to(world_map)

# displaying map
world_map
world_map.save('world_map.html')











# in order to display plot within window
# plt.show()
