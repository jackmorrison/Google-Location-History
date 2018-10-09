import pandas as pd, numpy as np, matplotlib.pyplot as plt, json, math, random
from datetime import datetime as dt
from mpl_toolkits.basemap import Basemap
from IPython.display import IFrame


# load the clustered/reduced and reverse-geocoded google location history data
df_ggl = pd.read_csv('full-dataset/google-location-history.csv', encoding='utf-8')
cols_to_retain = ['datetime', 'route','neighborhood', 'city', 'state', 'country', 'lat', 'lon']
df_ggl = df_ggl[cols_to_retain]
print('There are {:,} rows in the google data set'.format(len(df_ggl)))
df_ggl.head()

# de-duplicate rows with identical neighborhood, city, and state
df_ggl = df_ggl.drop_duplicates(subset=['route','neighborhood', 'city', 'state'], keep='first')

print('There are {:,} rows with duplicates removed'.format(len(df_ggl)))


df_ggl = df_ggl.rename(columns={'neighborhood':'place'})

df_combined = pd.concat([df_ggl], axis=0)
df_combined['year'] = df_combined['datetime'].str[6:10]
df_combined['year'] = df_combined['year'].str.replace('1995', '').fillna('')
df_combined = df_combined[['route','place', 'city', 'state', 'country', 'year', 'lat', 'lon']]
df_combined.tail

def get_description(row):
    fields = row[['route','place', 'city', 'state', 'country']].dropna().drop_duplicates()
    if len(fields) == 1:
        # if there's only 1 field, just return it
        return fields.iloc[0]
    elif len(fields) == 2:
        # if there are 2, return them with a line break between
        return fields.iloc[0] + '<br />' + fields.iloc[1]
    elif len(fields) == 3:
        # if there are 3, return the city/state comma-separated, then country after a line break
        return fields.iloc[0] + ', ' + fields.iloc[1] + '<br />' + fields.iloc[2]
    elif len(fields) == 4:
        # if there are 4, return the city/state comma-separated, then country after a line break
        return fields.iloc[0] + ', ' + fields.iloc[1] + '<br />' + fields.iloc[2] + '<br />' + fields.iloc[3]
    elif len(fields) == 5:
        # if there are 5, return the city/state comma-separated, then country after a line break
        return fields.iloc[0] + ', ' + fields.iloc[1] + '<br />' + fields.iloc[2] + ',' + fields.iloc[3] + '<br />' + fields.iloc[4] 
		
		
df_combined['desc'] = df_combined.apply(get_description, axis=1)


# round lat-long to 7 decimal points (to prevent fluky floating point .000000000001 stuff) to reduce js data file size
df_combined['lat'] = df_combined['lat'].round(7)
df_combined['lon'] = df_combined['lon'].round(7)

def df_to_geojson(df, properties=[], lat='lat', lon='lon'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop] if prop in row else None
        geojson['features'].append(feature)
    return geojson
	
	
cols_to_save = ['desc', 'year']
geojson = df_to_geojson(df_combined, cols_to_save)

output_filename = 'leaflet/location-dataset-full-dataset.js'
with open(output_filename, 'w') as output_file:
    output_file.write('var dataset = {};'.format(json.dumps(geojson, separators=(',',':'))))
print('{:,} geotagged features saved to file'.format(len(geojson['features'])))

# show the iframe of the leaflet web map here
IFrame('leaflet/location-map.html', width=600, height=400)

