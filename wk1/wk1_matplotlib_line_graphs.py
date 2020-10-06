################################################
# Week 1: Intro to Matplotlib and Line Graphs  #
################################################

# importing libraries
import numpy as np
import pandas as pd
import xlrd

#############
# Read Data #
#############
# read url
df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2)

# print('Data read into a pandas dataframe!')

# checking first 5 rows
df_can.head()
df_can.tail()

#######
# EDA #
#######

# tabulating basic info about our dataframe
# df_can.info()

# investigating columns and metadata
# df_can.columns.values

# this lists row indices
# df_can.index.values

# returns columns and indices types / classes
type(df_can.columns)
type(df_can.index)

# converting columns, and indices to lists
df_can.columns.tolist()
df_can.index.tolist()

# checking type post - list conversion
type(df_can.columns.tolist())
type(df_can.index.tolist())

# checking dimensions
df_can.shape

#############
# Reshaping #
#############

# dropping unnecessary columns
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)
# print(df_can.head(2))

# renaming column headers
df_can.rename(columns={'OdName': 'Country', 'AreaName':'Continent', 'RegName': 'Region'}, inplace=True)
df_can.columns

# preparing to visualize canadian data:

# by first adding a column for total immigration for 1980-2013
df_can['Total'] = df_can.sum(axis=1)


# tabulating null cells
df_can.isnull().sum()

# printing dataset metrics
df_can.describe()

#############################################
# Subsetting: using indices, row conditions #
#############################################

# printing a single specific column
df_can.Country

# printing a series of columns
df_can[['Country', 1980, 1981, 1982, 1983, 1984, 1985]]

# setting index to be the country names
df_can.set_index('Country', inplace=True)
df_can.head(3)

# option: removing the name of the dataset index
df_can.index.name = None

# 1: checking now data for Japan, using conditionality
df_can.loc['Japan'] # loc always indicates row + condition

# alternatively
df_can.iloc[87]
df_can[df_can.index == 'Japan'].T.squeeze()

# 2. pulling a specific year, and col values data
# ie filtering by 2 columns: index, & colname 2013
df_can.loc['Japan', 2013]
# alternate method # filtering by row num and col num
df_can.iloc[87, 36]

# 3: extending to years b/w 1980 and 1985
df_can.loc['Japan', [1980, 1981, 1982, 1983, 1984, 1985]]
# alternate method # filtering by row num and col num
df_can.iloc[87, [3, 4, 5, 6, 7, 8]]

# converting colnames for year and all others to string
df_can.columns = list(map(str, df_can.columns))

# printing col types by itself
# [print (type(x)) for x in df_can.columns.values]

# capturing list of years, for category visualization
years = list(map(str, range(1980, 2014)))
years

# filtering / subsetting rows, conditionally, using logic

# 1. creating var capturing logical subset, where continent is asia
condition = df_can['Continent'] == 'Asia'
condition

# 2. applying condition to subset
df_can[condition]

# upping the conditionality to multiple criteria
# (i) country = asia, and (ii) region = south asia
df_can[(df_can['Continent'] == 'Asia') & (df_can['Region'] == 'Southern Asia')]

# ^ this is golden for drilling down

# printing some stuff
# print('data dimensions:', df_can.shape) # sick command for printing dimensionality
df_can.columns
df_can.head(2)

################################
# Visualizing using Matplotlib #
################################
import matplotlib as mpl
import matplotlib.pyplot as plt

# print('Matplotlib version: ', mpl.__version__)

plt.style.available # printing options out
mpl.style.use(['ggplot']) # lol reverting back to to the ole' gg

# plotting some haitian data, inflows to the can
haiti = df_can.loc['Haiti', years]
haiti.head()
# prints/ saves haiti row data as a series

haiti.plot()
plt.show()
# haitian inflows hella spiked in aroun 2011-2012

# recalibrating indices to numeric values integers for plotting purposes

# buiding plot metrics: labelling axes
haiti.index = haiti.index.map(int)
haiti.plot(kind='line')

plt.title('Immigration from Haiti')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')

plt.show()


# buiding plot metrics: adding a point label
haiti.index = haiti.index.map(int)
haiti.plot(kind='line')

plt.title('Immigration from Haiti')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')

# labelling 2010 earthquake
# haitians be eatin mudcakes
plt.text(2000, 6000, '2010 Earthquake')

plt.show()

####################################
# Q1: China-India comparison rates #
####################################

indochina = df_can.loc[['India', 'China'], years]
print(indochina.head())


# buiding plot metrics: labelling axes
# indochina.index = indochina.index.map(int)
indochina.plot(kind='line')

plt.title('Immigration from India and China')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')

plt.show()

# transposing columns to get something more sensible
indochina = indochina.transpose()
print(indochina.head())
# this helps clarify it

## comparing india and china immigration trends!
indochina.plot(kind='line')
plt.title('Immigration from India and China')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')
plt.show()



################################
# Q2: Highest Immig. Countries #
################################
df_can_sorted = df_can.sort_values('Total', ascending=False)
df_can_sorted
print(df_can_sorted.head())

df_can_top5 = df_can_sorted.iloc[[0,1,2,3,4]]
print(df_can_top5)


df_can_top5 = df_can_top5.loc[:,years]
print(df_can_top5)

df_can_top5 = df_can_top5.transpose()
print(df_can_top5.head())


## comparing top5 immigration trends!
df_can_top5.plot(kind='line')
plt.title('Immigration from Top 5 Countries')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')
plt.show()






















# in order to display plot within window
# plt.show()
