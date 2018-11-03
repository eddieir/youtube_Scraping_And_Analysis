from bokeh.plotting import figure
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.us_states import data as statesData
import bokeh
import nltk
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import wikipedia
from geopy.geocoders import Nominatim
page = wikipedia.page("List_of_school_shootings_in_the_United_States")
html = page.html().encode("UTF-8")
#print (html[:1000])
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table')
print(str(table))
for span in table.select("span.sortkey"):
    span.decompose()
df = pd.read_html(str(table), header=0)[0]
# print(df)
# print(df.describe())
df['tokenized'] = df['Description'].apply(nltk.word_tokenize)
print(df.head(n=3))


def return_coordinate(local):
    location = geolocator.geocode(local)
    return pd.Series({'latitude': location.latitude, "longitude": location.longitude})


geolocator = Nominatim()
#print(return_coordinate("New York, New York"))


df[['latitude', 'longitude']] = df.apply(
    lambda row: return_coordinate(str(row['Location'])), axis=1)
print(df.head(n=10))


def split_and_strip(row):
    return [x.strip() for x in row["Location"].split(',')][1]


df['state'] = df.apply(lambda row: split_and_strip(row), axis=1)

print (df.head(n=10))

df['deaths_and_injuries'] = str(df['Deaths']) + df['Injuries']
df.describe()


# now it is the time to do the mapping


state_df = df.groupby(df['state'])['deaths_and_injuries'].sum()
print(state_df.head(n=5))
colors = bokeh.palettes.OrRd5[::-1]
color_mapper = bokeh.models.mappers.LinearColorMapper(palette=colors)
state_dict = state_df.to_dict()

# state leven information
new_state_xs = []
new_state_ys = []
state_name = []
state_count = []
for abbr, state in statesData.items():
    new_state_xs.append(state['lons'])
    new_state_ys.append(state['lats'])
    state_name.append(state['name'])
    state_count.append(state_dict.get(state['name'], 0))

incident_data_source = bokeh.models.sources.ColumnDataSource(df)
state_data_source = bokeh.models.sources.ColumnDataSource(
    data=dict(x=new_state_xs, y=new_state_ys, color=state_count))


plot = figure(title="School shooting", plot_width=800, plot_height=500)
plot.patches('x', 'y', source=state_data_source, color={
             'field': 'color', 'transform': color_mapper}, line_color="white", line_width=0.5)

circle = bokeh.models.markers.Circle(
    x='longitude', y='latitude', size='deaths_and_injuries')
plot.add_glyph(incident_data_source, circle)
show(plot)
