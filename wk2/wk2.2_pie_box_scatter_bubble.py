########################################
# Week 2.2: Pie, Box, Scatter, Bubble  #
########################################

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

# checking dimensions
df_can.shape

#############
# Reshaping #
#############

# dropping unnecessary columns
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)
df_can.head()

# renaming column headers
df_can.rename(columns={'OdName': 'Country', 'AreaName':'Continent', 'RegName': 'Region'}, inplace=True)
df_can.head()

# new command for doing the same thing, ie checking column types
# tests if column is a string header, boolean logic
all(isinstance(column, str) for column in df_can.columns)

# assigning column types to string, then rechecking
df_can.columns = list(map(str, df_can.columns))
all(isinstance(column, str) for column in df_can.columns)

# resetting index to unique country name
df_can.set_index('Country', inplace=True)
df_can.head()

# preparing to visualize canadian data:
# by first adding a column for total immigration for 1980-2013
df_can['Total'] = df_can.sum(axis=1)
df_can.head()

# printing m by n
# print('data dimensions:', df_can.shape) # sick command for printing dimensionality

# creating a varlist that can be used to call colnmaes while plotting or subsetting
# capturing list of years, for category visualization
years = list(map(str, range(1980, 2014)))
years

#####################################
# Visualizing Data using Matplotlib #
#####################################

# importing libs
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('ggplot')

# print('Matplotlib version: ', mpl.__version__) # >= 3.1.3

##############
# Pie Charts #
##############

# grouping countries by continents, and summing within continents
df_continents = df_can.groupby('Continent', axis=0).sum()

# output of groupby is a groupby type object
# summarizing along the vertical axis
type(df_can.groupby('Continent', axis=0))
df_continents.head()

# autopct is a way to calculate and represent proportions

df_continents['Total'].plot(kind='pie',
                            figsize=(5,6),
                            autopct='%1.1f%%', # adding in percentages
                            startangle=90,     # starting at 90 degrees
                            shadow=True,       # adding in shadow effects
                            )

plt.title('Immigration to Canada by Continent [1980 - 2013]')
plt.axis('equal') # sets pie into a circle type shape

plt.show()


# adjusting plot contours to better reflect reality

colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
explode_list = [0.1, 0, 0, 0, 0.1, 0.1] # ratios for wedge separating continents

df_continents['Total'].plot(kind='pie',
                            figsize=(15,6),
                            autopct='%1.1f%%',
                            startangle=90,
                            labels=None,          # switches off labels
                            pctdistance=1.12,     # ratio b/w center of pie slices and text starts
                            colors=colors_list,   # custom colors
                            explode=explode_list  # explodes lowest continents
                            )

# scaling title up by 12% to match pctdistance
plt.title('Immigration to Canada by Continent [1980 - 2013]', y=1.12)

plt.axis('equal')

# adding in a plot legend
plt.legend(labels=df_continents.index, loc='upper left')

plt.show()


# oh my god, it's beautiful!!
# the exploder actually nudges it out of the pie an inch!

################################
# Q1: Groupby, 2013 Pie Charts #
################################

df_can_13 = df_can[['Continent', '2013']]
df_can_13.head()

df_continents_13 = df_can_13.groupby('Continent', axis=0).sum()
df_continents_13.head()


colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
explode_list = [0.1, 0, 0, 0, 0.1, 0.1] # ratios for wedge separating continents

df_continents_13['2013'].plot(kind='pie',
                            figsize=(15,10),
                            autopct='%1.1f%%',
                            startangle=90,
                            labels=None,          # switches off labels
                            pctdistance=1.12,     # ratio b/w center of pie slices and text starts
                            colors=colors_list,   # custom colors
                            explode=explode_list  # explodes lowest continents
                            )

# scaling title up by 10% to match pctdistance
plt.title('Immigration to Canada by Continent - 2013', y=1.10)

plt.axis('equal')

# adding in a plot legend
plt.legend(labels=df_continents.index, loc='upper left')

plt.show()


#############
# Box Plots #
#############

# creating a new dataframe with countries restructed merely to japan
df_japan = df_can.loc[['Japan'], years].transpose()
df_japan.head()

# reverting back to the ole' box plot

df_japan.plot(kind='box', figsize=(8,6))

plt.title('Box plot of Japanese Immigrants from 1980 - 2013')
plt.ylabel('Number of Immigrants')

plt.show()


# descriptive stats for japan
df_japan.describe()

##############
# Q2:  Plots #
##############

df_CI = df_can.loc[['India', 'China'], years].transpose()
df_CI.head()

# descriptive stats for india and china
df_CI.describe()

# plotting countries' spreads side by side

df_CI.plot(kind='box', figsize=(8,6))

plt.title('Box plot of Chinese & Indian Immigrants from 1980 - 2013')
plt.ylabel('Number of Immigrants')

plt.show()
# distribution is wayy wider for China.


# horizontal plots are another way to go
# we merely flip axes labels

df_CI.plot(kind='box', figsize=(10, 7), color='blue', vert=False)

plt.title('Box plot of Chinese & Indian Immigrants from 1980 - 2013')
plt.xlabel('Number of Immigrants')

plt.show()


############
# Subplots #
############

# grids and panels
fig = plt.figure() # creating figure

ax0 = fig.add_subplot(1, 2, 1) # add subplot 1 // # 1 row, 2 columns, plt 1
ax1 = fig.add_subplot(1, 2, 2) # add subplot 2 // # 1 row, 2 columns, plt 2

# subplot 1: is a box plot
df_CI.plot(kind='box', color='blue', vert=False, figsize=(20, 6), ax=ax0) # adding to sb plt1
ax0.set_title('Box Plots of Immigrants from China and India (1980 - 2013)')
ax0.set_xlabel('Number of Immigrants')
ax0.set_ylabel('Countries')

# subplot 2: is a line plot
df_CI.plot(kind='line', figsize=(20, 6), ax=ax1) # adding to sb plt2
ax1.set_title('Line Plots of Immigrants from China and India (1980 - 2013)')
ax1.set_xlabel('Number of Immigrants')
ax1.set_ylabel('Countries')

plt.show()


#################################
# Q3: top 15, grouped by decade #
#################################

# getting the dataset for top 15 countries

# sorting
df_top15 = df_can.sort_values('Total', ascending=False)

# restricting our analysis to top 15 totals
df_top15 = df_top15.head(15)
df_top15.head()

# subsetting to totals column
# df_top15 = df_top15.loc[:,'Total']

eighties = list(map(str, range(1980, 1989)))
nineties = list(map(str, range(1990, 1999)))
twothousands = list(map(str, range(2000, 2009)))
twentytens = list(map(str, range(2010, 2014)))

df_can['Total_80'] = df_can[eighties].sum(axis=1)
df_can['Total_90'] = df_can[nineties].sum(axis=1)
df_can['Total_00'] = df_can[twothousands].sum(axis=1)
df_can['Total_10'] = df_can[twentytens].sum(axis=1)

#print(df_can[eighties].head())
#print(df_can['Total_80'].head())

new_df = df_can[['Total_80', 'Total_90', 'Total_00']]

new_df.head()
new_df.tail()

# dataframe comprising totals from each decade
new_df.describe()

# new_df = new_df.transpose()
# new_df.head()

# plotting decades' spreads side by side

new_df.plot(kind='box', figsize=(8,6))

plt.title('Box plot of Top 15 Immigrant Countries, by decade (from 1980 - 2013)')
plt.ylabel('Number of Immigrants')

plt.show()


################
# Scatter Plot #
################

# collapsing each year column into a single aggregated row
df_tot = pd.DataFrame(df_can[years].sum(axis=0))
print(df_tot.head())

# Changing year types to int, to measure incremental effects when regressing
df_tot.index = map(int, df_tot.index)

# resetting the index to reframe it as a column
df_tot.reset_index(inplace = True)

# renaming columns
df_tot.columns = ['year', 'total']

# viewing the final outputted dataset creation
print(df_tot.head())

# finally, compiling our plot

df_tot.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')

plt.title('Total Immigration to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')

plt.show()
'''
# grabbing columns into arrays for plotting fit line

# this method for subsetting doesn't yield arrays # avoid.
# x = df_tot['year']   # year array for x-axis fit
# y = df_tot['total']  # total for y-axis fit

print(x)
print(y)

fit = np.polyfit(x, y, 1, full=True)
print(fit)

# plotting a more souped up grpah, w/ fit line

df_tot.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')

plt.title('Total Immigration to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')

# plotting line of best fit
plt.plot(x, fit[0] * x + fit[1], color='red') # recall x is the years variable
plt.annotate('y={0:.0f} x + {1:.0f}'.format(fit[0], fit[1]), xy=(2000, 150000))
# fit[0] and fit[1] extracts the coefficients for use in plotting
plt.show()
'''
# printing out our the best fit line
# print('No. Immigrants = {0:.0f} * Year + {1:.0f}'.format(fit[0], fit[1]))
# .0f is a way of formatting decimals when calling vars into strings

#####################################################
# Q4: Scatterplot of immigrations: Nordic -> Canada #
#####################################################

# subsetting to nordic countries
df_countries = df_can.loc[['Denmark', 'Norway', 'Sweden'], years]
df_countries.head()

# summing numbers across the years for these three countries
df_total = pd.DataFrame(df_countries[years].sum(axis=0))

# Changing year types to int, to measure incremental effects when regressing
df_total.index = map(int, df_total.index)

# resetting the index in place
df_total.reset_index(inplace = True)

# renaming columns to year and total
df_total.columns = ['year', 'total']

# displaying our resulting dataframe
df_total.head()


# generating the scatterplot total vs year

df_total.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')

plt.title('Total Immigration From Nordic Countries to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')

plt.show()

# no strong upward or downward trajectory
# if you fitted a line across the years, it would pretty much be flat.

################
# Bubble Plots #
################

# fetching the data for argentina and brazil
df_can_t = df_can[years].transpose() # transposing our data

# Changing year types to int, to measure incremental effects when regressing
df_can_t.index = map(int, df_can_t.index)

# relabelling the index name prior to resetting it
df_can_t.index.name = 'Year'
# resetting the index in place
df_can_t.reset_index(inplace = True)

# displaying our resulting dataframe
df_can_t.head()

# now, normalizing Brazil and Argentina data to make it comparable
# to be utilized in plots
norm_brazil = (df_can_t['Brazil'] - df_can_t['Brazil'].min()) / (df_can_t['Brazil'].max() - df_can_t['Brazil'].min())
norm_argentina = (df_can_t['Argentina'] - df_can_t['Argentina'].min()) / (df_can_t['Argentina'].max() - df_can_t['Argentina'].min())

# now, setting up our scatterplot for the respective countries

ax0 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Brazil',
                    figsize=(14, 8),
                    alpha=0.5,
                    color='green',
                    s=norm_brazil * 2000 + 10, # pass in weights
                    xlim=(1975, 2015)
                    )

ax1 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Argentina',
                    alpha=0.5,
                    color="blue",
                    s=norm_argentina * 2000 + 10,
                    ax = ax0 # anchoring axes to combine plots
                    )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration From Brazil and Argentina from 1980 - 2013')
ax0.legend(['Brazil', 'Argentina'], loc='upper left', fontsize='x-large')

plt.show()


####################################
# Q5: China and India Bubble Plots #
####################################

# fetching the data for china and india:

# now, normalizing China and India data to make it comparable
# to be utilized in plots
norm_china = (df_can_t['China'] - df_can_t['China'].min()) / (df_can_t['China'].max() - df_can_t['China'].min())
norm_india = (df_can_t['India'] - df_can_t['India'].min()) / (df_can_t['India'].max() - df_can_t['India'].min())

# now, setting up our scatterplot for the respective countries
ax0 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='China',
                    figsize=(14, 8),
                    alpha=0.5,
                    color='green',
                    s=norm_china * 2000 + 10, # pass in weights
                    xlim=(1975, 2015)
                    )

ax1 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='India',
                    alpha=0.5,
                    color="blue",
                    s=norm_india * 2000 + 10,
                    ax = ax0 # anchoring axes to combine plots
                    )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration From China and India from 1980 - 2013')
ax0.legend(['China', 'India'], loc='upper left', fontsize='x-large')

plt.show()

































# in order to display plot within window
# plt.show()
