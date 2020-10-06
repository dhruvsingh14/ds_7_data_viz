###############################################################
# Week 3.1: Waffle Charts, Word Clouds, and Regression Plots  #
###############################################################

# importing libraries
import numpy as np
import pandas as pd
import xlrd
from PIL import Image # converts images into arrays

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
import matplotlib.patches as mpatches # required for waffle charts

mpl.style.use('ggplot')

# print('Matplotlib version: ', mpl.__version__) # >= 3.1.3

#################
# Waffle Charts #
#################

# creating a new dataframe comrpising of nordic countries
df_dsn = df_can.loc[['Denmark', 'Norway', 'Sweden'], :]
df_dsn

#computing proportion of values to the whole
total_values = sum(df_dsn['Total'])
category_proportions = [(float(value) / total_values) for value in df_dsn['Total']]

# printing these proportions for each value of total yearly immigration
# relative to total immigration from country to canada

for i, proportion in enumerate(category_proportions):
    print (df_dsn.index.values[i] + ': ' + str(proportion))


# preparing to define the dimensions of our chart
width = 40 # width of chart
height = 10 # height of chart
total_num_tiles = width * height # total number of tiles in grid
# print ('Total number of tiles is ', total_num_tiles)

# computing tiles per category ((country+year total)/country total)
tiles_per_category = [round(proportion * total_num_tiles) for proportion in category_proportions]

# printing out our number of tiles per category

for i, tiles in enumerate(tiles_per_category):
    print (df_dsn.index.values[i] + ': ' + str(tiles))


# declaring empty matrix to prepare for waffle chart
waffle_chart = np.zeros((height, width))

# defining indices to loop through
category_index = 0
tile_index = 0

# populating the waffle chart
for col in range(width):
    for row in range(height):
        tile_index += 1

        # if the number for current category is equal to corresponding tiles..
        if tile_index > sum(tiles_per_category[0:category_index]):
            # .. proceed to next
            category_index += 1

        # setting class value to an integer
        waffle_chart[row, col] = category_index

# print ('Waffle chart populated!')
waffle_chart

# preparing to map waffle to a visual

fig = plt.figure()

# using matshow to display the waffle chart
colormap = plt.cm.coolwarm
plt.matshow(waffle_chart, cmap=colormap)
plt.colorbar()

plt.show()


# prettyfying or souping up the chart, iteration 1
# declaring a new figure object

fig = plt.figure()

# using matshow to display the waffle chart
colormap = plt.cm.coolwarm
plt.matshow(waffle_chart, cmap=colormap)
plt.colorbar()

# getting the axes
ax = plt.gca()

# setting minor ticks
ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
ax.set_yticks(np.arange(-.5, (height), 1), minor=True)

# adding in gridlines based on minor ticks
ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

plt.xticks([])
plt.yticks([])

plt.show()


# prettyfying, souping up the chart, iteration 2
# declaring a new figure object

fig = plt.figure()

# using matshow to display the waffle chart
colormap = plt.cm.coolwarm
plt.matshow(waffle_chart, cmap=colormap)
plt.colorbar()

# getting the axes
ax = plt.gca()

# setting minor ticks
ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
ax.set_yticks(np.arange(-.5, (height), 1), minor=True)

# adding in gridlines based on minor ticks
ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

plt.xticks([])
plt.yticks([])

# computing cumulative sums
values_cumsum = np.cumsum(df_dsn['Total'])
total_values = values_cumsum[len(values_cumsum) - 1]

# creating the legend
legend_handles = []
for i, category in enumerate(df_dsn.index.values):
    label_str = category + ' (' + str(df_dsn['Total'][i]) + ')'
    color_val = colormap(float(values_cumsum[i])/total_values)
    legend_handles.append(mpatches.Patch(color=color_val, label=label_str))

# adding legend to chart
plt.legend(handles=legend_handles,
           loc='lower center',
           ncol=len(df_dsn.index.values),
           bbox_to_anchor=(0., -0.2, 0.95, .1)
           )

plt.show()

# awesome, the legend really adds a cool element


# creating instead a function that generates our waffle chart
def create_waffle_chart(categories, values, height, width, colormap, value_sign=''):

    #computing proportion of values to the whole
    total_values = sum(values)
    category_proportions = [(float(value) / total_values) for value in values]

    # total number of tiles in grid
    total_num_tiles = width * height
    print ('Total number of tiles is ', total_num_tiles)

    # computing tiles per category ((country+year total)/country total)
    tiles_per_category = [round(proportion * total_num_tiles) for proportion in category_proportions]

    # printing out our number of tiles per category
    for i, tiles in enumerate(tiles_per_category):
        print (df_dsn.index.values[i] + ': ' + str(tiles))

    # declaring empty matrix to prepare for waffle chart
    waffle_chart = np.zeros((height, width))

    # defining indices to loop through
    category_index = 0
    tile_index = 0

    # populating the waffle chart
    for col in range(width):
            for row in range(height):
                tile_index += 1

                # if the number for current category is equal to corresponding tiles..
                if tile_index > sum(tiles_per_category[0:category_index]):
                    # .. proceed to next
                    category_index += 1

                # setting class value to an integer
                waffle_chart[row, col] = category_index


    # declaring a new figure object
    fig = plt.figure()

    # using matshow to display the waffle chart
    colormap = plt.cm.coolwarm
    plt.matshow(waffle_chart, cmap=colormap)
    plt.colorbar()

    # getting the axes
    ax = plt.gca()

    # setting minor ticks
    ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
    ax.set_yticks(np.arange(-.5, (height), 1), minor=True)

    # adding in gridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    plt.xticks([])
    plt.yticks([])

    # computing cumulative sums
    values_cumsum = np.cumsum(values)
    total_values = values_cumsum[len(values_cumsum) - 1]

    # creating the legend
    legend_handles = []
    for i, category in enumerate(categories):
        if value_sign == '%':
            label_str = category + ' (' + str(values[i]) + value_sign + ')'
        else:
            label_str = category + ' (' + value_sign + str(values[i]) + ')'

        color_val = colormap(float(values_cumsum[i])/total_values)
        legend_handles.append(mpatches.Patch(color=color_val, label=label_str))

    # adding legend to chart
    plt.legend(
        handles=legend_handles,
        loc='lower center',
        ncol=len(categories),
        bbox_to_anchor=(0., -0.2, 0.95, .1)
    )

    plt.show()

# now, to create a waffle chart
width = 40 # width of our chart
height = 10 # height of our chart

categories = df_dsn.index.values # categories: of year_country
values = df_dsn['Total'] # corresponding values to year_country categories

colormap = plt.cm.coolwarm # color map class being added

# create_waffle_chart(categories, values, height, width, colormap)

###############
# Word Clouds #
###############

# importing package
from wordcloud import WordCloud, STOPWORDS
import wget

# print('Wordcloud is installed and imported!')

# downloading text file using wget
url = 'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/alice_novel.txt'
wget.download(url, 'alice_novel.txt')

# opening text file and reading it into a variable called alice_novel
alice_novel = open('alice_novel.txt', 'r').read()
# print('File downloaded and saved!')

# removes redundant 'stopwords'
stopwords = set(STOPWORDS)

# preparing to generate a word cloud
# by first subsetting to the first 2000 words of the novel

# declaring a word cloud object
alice_wc = WordCloud(
    background_color='white',
    max_words=2000,
    stopwords=stopwords
)

# generating the word cloud
alice_wc.generate(alice_novel)


# actually plotting the cloud display, iteration 1
plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')
plt.show()



# resizing the word cloud, iteration 2
fig = plt.figure()
fig.set_figwidth(14)  # setting width
fig.set_figheight(18) # setting height

# displaying the cloud, iteration 2
plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')
plt.show()



# scrapping unnecessary words, iteration 3
stopwords.add('said') # adding said to stopwords

# re-generating the cloud visual, iteration 3
alice_wc.generate(alice_novel)

# displaying the word cloud, iteration 3
fig = plt.figure()
fig.set_figwidth(14)  # setting width
fig.set_figheight(18) # setting height

plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')
plt.show()


# using wordcloud to superimpose cloud visuals onto a mask image

# downloading image
url2 = 'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Images/alice_mask.png'
wget.download(url2, 'alice_mask.png')

# reading in and saving mask image file
alice_mask = np.array(Image.open('alice_mask.png'))
# print('Image downloaded and saved!')


# opening and displaying image shell
fig = plt.figure()
fig.set_figwidth(14)  # setting width
fig.set_figheight(18) # setting height

plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis('off')
plt.show()



# declaring a word cloud object, iteration 4
alice_wc = WordCloud(background_color='white', max_words=2000, mask=alice_mask, stopwords=stopwords)

# generating the word cloud, iteration 4
alice_wc.generate(alice_novel)

# displaying the word cloud, iteration 4
fig = plt.figure()
fig.set_figwidth(14)  # setting width
fig.set_figheight(18) # setting height

plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')
plt.show()


# switching gears back to regression plots, and canada data
df_can.head()

# checking total immigration from 190 to 2013
total_immigration = df_can['Total'].sum()
total_immigration

# using single word country names to generate word cloud
# based on frequency
max_words = 90
word_string = ''
for country in df_can.index.values:
    # checking if a country's name is a single-word name
    if len(country.split(' ')) == 1:
        repeat_num_times = int(df_can.loc[country, 'Total']/float(total_immigration)*max_words)
        word_string = word_string + ((country + ' ') * repeat_num_times)

# displaying generated text
word_string


# creating the word cloud, no stopwords
wordcloud = WordCloud(background_color='white').generate(word_string)
# print('Word cloud created!')

# displaying the country word cloud
fig = plt.figure()
fig.set_figwidth(14)  # setting width
fig.set_figheight(18) # setting height

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


####################
# Regression Plots #
####################

# importing seaborn
import seaborn as sns
# print('Seaborn installed and imported!')

# using the sum() method to get the total population per year
# in essence, collapsing by year,across all countries
df_tot = pd.DataFrame(df_can[years].sum(axis=0))

# changing year type to float to measure incremental change
df_tot.index = map(float, df_tot.index)

# resetting index to use as a column
df_tot.reset_index(inplace=True)

# renaming columns
df_tot.columns = ['year', 'total']

# viewing outputted dataframe
df_tot.head()


# plot 1, using regplot
ax = sns.regplot(x='year', y='total', data=df_tot)
plt.show()



# plot 2, switching color to green
ax = sns.regplot(x='year', y='total', data=df_tot, color='green')
plt.show()



# plot 3, changing markers to + signs
ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+')
plt.show()



# plot 4, blowing up the plot size
plt.figure(figsize=(15,10))
ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+')
plt.show()



# plot 5, blowing up marker size, adding axis labels, title
plt.figure(figsize=(15,10))
ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+', scatter_kws={'s': 200})

ax.set(xlabel='Year', ylabel='Total Immigration') # adding axes labels
ax.set_title('Total Immigration to Canada from 1980 - 2013') # add title
plt.show()



# plot 6, increasing font size of tickmark labels, title, axes
plt.figure(figsize=(15,10))
sns.set(font_scale=1.5)

ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+', scatter_kws={'s': 200})
ax.set(xlabel='Year', ylabel='Total Immigration') # adding axes labels
ax.set_title('Total Immigration to Canada from 1980 - 2013') # add title

plt.show()



# plot 6.1, optional features: white background
plt.figure(figsize=(15,10))
sns.set(font_scale=1.5)
sns.set_style('ticks') # changing background to white

ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+', scatter_kws={'s': 200})
ax.set(xlabel='Year', ylabel='Total Immigration') # adding axes labels
ax.set_title('Total Immigration to Canada from 1980 - 2013') # add title

plt.show()



# plot 6.2, optional features: gridlines
plt.figure(figsize=(15,10))
sns.set(font_scale=1.5)
sns.set_style('whitegrid')

ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+', scatter_kws={'s': 200})
ax.set(xlabel='Year', ylabel='Total Immigration') # adding axes labels
ax.set_title('Total Immigration to Canada from 1980 - 2013') # add title

plt.show()



############################################################
# Q1: Scatterplot of Nordic Countries, fitted with Regline #
############################################################

# Question: Use seaborn to create a scatter plot with a
# regression line to visualize the total immigration from
# Denmark, Sweden, and Norway to Canada from 1980 to 2013.


# subsetting to denmark, norway, and sweden
df_dsn = df_can.loc[['Denmark', 'Norway', 'Sweden'], :]

# collapsing across countries, for each year
dsn_tot = pd.DataFrame(df_dsn[years].sum(axis=0))

# changing year type to float to measure incremental change
dsn_tot.index = map(float, dsn_tot.index)

# resetting index to use as a column
dsn_tot.reset_index(inplace=True)

# renaming columns
dsn_tot.columns = ['year', 'total']

# viewing outputted dataframe
dsn_tot.head()


# creating a fleshed out regression plot for our data
plt.figure(figsize=(15,10))
sns.set(font_scale=1.5)

ax = sns.regplot(x='year', y='total', data=dsn_tot, color='green', marker='+', scatter_kws={'s': 200})
ax.set(xlabel='Year', ylabel='Total Immigration') # adding axes labels
ax.set_title('Total Immigration from Nordic Countries to Canada from 1980 - 2013') # add title

plt.show()















# in order to display plot within window
# plt.show()
