####################################################
# Week 2.1: Area Plots, Histograms, and Bar Plots  #
####################################################

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
# Area Plots #
##############

df_can.sort_values(['Total'], ascending=False, axis=0, inplace=True)

# very interesting way of grabbing top entries, and saving to a dataset
# using head
df_top5 = df_can.head()

# transposing columns of the matrix to forms rows for each year
df_top5 = df_top5[years].transpose()
df_top5.head()

# producing a stacked area plot

df_top5.index = df_top5.index.map(int) # changing index to integer for plotting purposes
# not fully sure what changing index to integer accomplishes (yet)


df_top5.plot(kind='area',
            stacked=False,
            figsize=(20, 10), # tells what size to adjust window to
            )

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Numer of Immigrants')
plt.xlabel('Years')

plt.show()



# tweaking alpha transparency value
df_top5.plot(kind='area',
            alpha=0.25, # 0-1 scale, default a= 0.5
            stacked=False, # overlays plots
            figsize=(20, 10), # tells what size to adjust window to
            )

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Numer of Immigrants')
plt.xlabel('Years')

plt.show()


# Two types of plotting

# option 1, using scripting layer, procedural, used so far
# option 2, object oriented, more flexibility, preferred


ax = df_top5.plot(kind='area', alpha=0.35, figsize=(20,10))

ax.set_title('Immigration Trend of Top 5 Countries')
ax.set_ylabel('Number of Immigrants')
ax.set_xlabel('Years')

plt.show()


####################################################
# Q1: Scripting layer, stacked area plot, a = 0.45 #
####################################################

# setting alpha transparency value to 0.45

df_top5.plot(kind='area',
            alpha=0.45, # 0-1 scale, default a= 0.5
            stacked=False, # overlays plots
            figsize=(20, 10), # tells what size to adjust window to
            )

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Numer of Immigrants')
plt.xlabel('Years')

plt.show()


###################################################
# Q2: Artist layer, unstacked area plot, a = 0.55 #
###################################################

# a = 0.55

ax = df_top5.plot(kind='area', alpha=0.55, figsize=(20,10))

ax.set_title('Immigration Trend of Top 5 Countries')
ax.set_ylabel('Number of Immigrants')
ax.set_xlabel('Years')

plt.show()


##############
# Histograms #
##############

# viewing 2013 data
df_can['2013'].head()

# using numpy's histogram functionality to extract metrics
# cut points, and count per interval

count, bin_edges = np.histogram(df_can['2013'])

# printing
count
bin_edges

# using above extracted metrics to plot our histogram
# can scale accordingly

df_can['2013'].plot(kind='hist', figsize=(8,5))

plt.title('Histogram of Immigration from 195 Countries in 2013')
plt.ylabel('Number of Countries')
plt.xlabel('Number of Immigrants')

plt.show()


# iteration 2:
# adding in x-ticks
# 'bin_edges' shows the cut points on axis, here for number of immigrants

count, bin_edges = np.histogram(df_can['2013'])

df_can['2013'].plot(kind='hist', figsize=(8,5), xticks=bin_edges)

plt.title('Histogram of Immigration from 195 Countries in 2013')
plt.ylabel('Number of Countries')
plt.xlabel('Number of Immigrants')

plt.show()

# using x ticks applies more accurate labels to cutpoints
# rather than generic width labels

# viewing a few countries worth of data for all years
df_can.loc[['Denmark', 'Norway', 'Sweden'], years]

# generating histogram

df_can.loc[['Denmark', 'Norway', 'Sweden'], years].plot.hist()
plt.show()


# this plot isn't to our liking, and is in fact smushed in
# transposing data to obtain better plot

# transposing dataframe below, for better plotting ability
df_t = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()
df_t.head()

# generating histogram

df_t.plot(kind='hist', figsize=(10,6))

plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants')

plt.show()


# can enhance clarity, for overlaying regions; and impose clearer x ticks

# obtaining x-ticks

count, bin_edges = np.histogram(df_t, 15)

# un-stacking our histogram to promote transparency

df_t.plot(kind ='hist',
          figsize=(10, 6),
          bins=15,
          alpha=0.6,
          xticks=bin_edges,
          color=['coral', 'darkslateblue', 'mediumseagreen']
          )

plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants')

plt.show()


# much much sicker, it still doesn't show us consecutive years' patterns
# though it does show absolute numbers

# alternatively, we can have them sit one on top of the other
# as in a stacked plot
count, bin_edges = np.histogram(df_t, 15)

# clipping axes using x min and max values, plus some buffer
xmin = bin_edges[0] - 10
xmax = bin_edges[-1] + 10

# stacked plot

df_t.plot(kind ='hist',
          figsize=(10, 6),
          bins=15,
          xticks=bin_edges,
          color=['coral', 'darkslateblue', 'mediumseagreen'],
          stacked=True,
          xlim=(xmin, xmax)
          )

plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants')

plt.show()

# here it is the width from the base to the top that implies the column's count
# ie, its difference, rather than it's distance from the x-axis

#######################################################
# Q3: Scripting layer, un-stacked hist plot, a = 0.35 #
#######################################################

# obtaining plot for south east europian nations
df_can.loc[['Greece', 'Albania', 'Bulgaria'], years]

# transposing for a better plot
df_t2 = df_can.loc[['Greece', 'Albania', 'Bulgaria'], years].transpose()
df_t2.head()

count, bin_edges = np.histogram(df_t2, 15)


# plotting unstacked, overlayed histogram, with alpha = 0.35
df_t2.plot(kind ='hist',
          figsize=(10, 6),
          bins=15,
          alpha=0.35,
          xticks=bin_edges,
          color=['coral', 'darkslateblue', 'mediumseagreen']
          )

plt.title('Histogram of Immigration from Greece, Albania, and Bulgaria from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants')

plt.show()


##############
# Bar Charts #
##############

# restricting our analysis to Iceland
df_iceland = df_can.loc['Iceland', years]
df_iceland.head()

# plotting a preliminary chart

df_iceland.plot(kind='bar', figsize=(10, 6))

plt.xlabel('Year')
plt.ylabel('Number of Immigrants')
plt.title('Icelandic immigrants to Canada from 1980 to 2013')

plt.show()



# annotating plot further with arrow

df_iceland.plot(kind='bar', figsize=(10, 6), rot=90)

plt.xlabel('Year')
plt.ylabel('Number of Immigrants')
plt.title('Icelandic immigrants to Canada from 1980 to 2013')

# using arrow annotation
plt.annotate('', # blank, no text here
             xy=(32, 70), # places head of arrow here
             xytext=(28, 20), # places base of arrow here
             xycoords='data',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)

)

plt.show()


# adding text rotation and text annotation to our plot

df_iceland.plot(kind='bar', figsize=(10, 6), rot=90)

plt.xlabel('Year')
plt.ylabel('Number of Immigrants')
plt.title('Icelandic immigrants to Canada from 1980 to 2013')

# using arrow annotation
plt.annotate('', # blank, no text here
             xy=(32, 70), # places head of arrow here
             xytext=(28, 20), # places base of arrow here
             xycoords='data',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)

)

# using text annotation
plt.annotate('2008 - 2011 Financial Crisis', # text to display
             xy=(28, 30), # starts text here
             rotation=72.5, # matches arrow head, using trial and error
             va='bottom', # text vertically bottom aligned
             ha='left', # text vertically left aligned
             )


plt.show()


###########################################################
# Q4: Scripting layer, swapping axes, horizontal bar plot #
###########################################################

# sorting
top15_can = df_can.sort_values('Total', ascending=False)
top15_can.head()

# subsetting to totals column
top15_can = top15_can.loc[:,'Total']

# restricting our analysis to top 15 totals
top15_can = top15_can.head(15)
print(top15_can.head())


# plotting horizontal plot with barh
top15_can.plot(kind='barh', figsize=(10, 10))

plt.xlabel('Number of Immigrants')
plt.ylabel('Country')
plt.title('Top 15 Countries - total immigrants to Canada from 1980 to 2013')

plt.show()































# in order to display plot within window
# plt.show()
