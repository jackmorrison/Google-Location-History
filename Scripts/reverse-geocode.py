import pandas as pd, time, requests, json, os.path, logging as lg, datetime as dt, io

pause = 0.1 #google limits to 10 requests per second
use_second_geocoder = False #only set to True on last pass, if multiple
max_google_requests = 3500
google_requests_count = 0 
final_output_filename = 'full-dataset/google-location-history.csv'

#configure local caching
geocode_cache_filename = 'full-dataset/reverse_geocode_cache_test.js'
cache_save_frequency = 100
requests_count = 0
geocode_cache = json.load(open(geocode_cache_filename)) if os.path.isfile(geocode_cache_filename) else ()

#create a logger to capture progress
log = lg.getLogger('reverse_geocoder')
if not getattr(log, 'handler_set', None):
	todays_date = dt.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
	log_filename = 'logs/reverse_geocoder_{}.log'.format(todays_date)
	handler = lg.FileHandler(log_filename, encoding='utf-8')
	formatter = lg.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
	handler.setFormatter(formatter)
	log.addHandler(handler)
	log.setLevel(lg.INFO)
	log.handler_set = True
	
#set up the working file 
working_filename = 'full-dataset/google-location-history-to-geocode.csv'
if not os.path.isfile(working_filename):
	df_temp = pd.read_csv('full-dataset/location-history-clustered_full_dataset.csv', encoding='utf-8')
	df_temp.to_csv(working_filename, index=False, encoding='utf-8')
	
	
# saves the dict cache to disk as json
def save_cache_to_disk(cache, filename):
    with open(filename, 'w') as cache_file:
        cache_file.write(json.dumps(cache))
    #log.info('saved {:,} cached items to {}'.format(len(cache.keys()), filename))
	
	
# make a http request
def make_request(url):
    log.info('requesting {}'.format(url))
    return requests.get(url).json()
	
# parse route data from a google reverse-geocode result
def get_route_google(result):
    if pd.notnull(result):
        if 'address_components' in result:
            for component in result['address_components']:
                if 'route' in component['types']:
                    return component['long_name']

	
# parse neighborhood data from a google reverse-geocode result
def get_neighborhood_google(result):
    if pd.notnull(result):
        if 'address_components' in result:
            for component in result['address_components']:
                if 'neighborhood' in component['types']:
                    return component['long_name']
                elif 'sublocality_level_1' in component['types']:
                    return component['long_name']
                elif 'sublocality_level_2' in component['types']:
                    return component['long_name']                

# parse city data from a google reverse-geocode result
# to find city, return the finest-grain address component 
# google returns these components in order from finest to coarsest grained
def get_city_google(result):
    if pd.notnull(result):
        if 'address_components' in result:
            for component in result['address_components']:
                if 'locality' in component['types']:
                    return component['long_name']
                elif 'postal_town' in component['types']:
                    return component['long_name']              
                elif 'administrative_area_level_5' in component['types']:
                    return component['long_name']
                elif 'administrative_area_level_4' in component['types']:
                    return component['long_name']
                elif 'administrative_area_level_3' in component['types']:
                    return component['long_name']
                elif 'administrative_area_level_2' in component['types']:
                    return component['long_name']

# parse state data from a google reverse-geocode result                
# to find state, you want the lowest-level admin area available
# but, google returns admin areas listed from highest-level to lowest
# so you can't just return as soon as you find the first match
# this is is opposite of the previous, because this time we want the coarsest-grain match
# otherwise we end up with counties and so forth instead of states
def get_state_google(result):
    if pd.notnull(result):
        state = None
        if 'address_components' in result:
            for component in result['address_components']:
                if 'administrative_area_level_1' in component['types']:
                    state = component['long_name']
                elif 'administrative_area_level_2' in component['types']:
                    state = component['long_name']
                elif 'administrative_area_level_3' in component['types']:
                    state = component['long_name']
                elif 'locality' in component['types']:
                    state = component['long_name']
        return state

# parse country data from a google reverse-geocode result
def get_country_google(result):
    if pd.notnull(result):
        if 'address_components' in result:
            for component in result['address_components']:
                if 'country' in component['types']:
                    return component['long_name']
					

# parse city, state, country data from a nominatim reverse-geocode result
def parse_nominatim_data(data):
    country = None
    state = None
    city = None
    if isinstance(data, dict):
        if 'address' in data:
            if 'country' in data['address']:
                country = data['address']['country']

            #state
            if 'region' in data['address']:
                state = data['address']['region']
            if 'state' in data['address']:
                state = data['address']['state']

            #city
            if 'county' in data['address']:
                county = data['address']['county']
            if 'village' in data['address']:
                city = data['address']['village']
            if 'city' in data['address']:
                city = data['address']['city']
    return city, state, country
	
	
# pass latlng data to osm nominatim to reverse geocode it
def reverse_geocode_nominatim(latlng):

    time.sleep(pause)
    url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=1'
    data = make_request(url.format(latlng.split(',')[0], latlng.split(',')[1]))

    place = {}
    place['neighborhood'] = None
    place['city'], place['state'], place['country'] = parse_nominatim_data(data)
    return place	
	
# pass the Google API latlng data to reverse geocode it
def reverse_geocode_google(latlng):
    
    global google_requests_count
    
    if google_requests_count < max_google_requests:
        # we have not yet made the max # of requests
        time.sleep(pause)
        google_requests_count += 1
        url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyALaksk8veGOJ78dUtHl3ckTqIOw_YXeYI&latlng={}'
        data = make_request(url.format(latlng))
        if len(data['results']) > 0:
            result = data['results'][0]
            
            place = {}
            place['route'] = get_route_google(result)
            place['neighborhood'] = get_neighborhood_google(result)
            place['city'] = get_city_google(result)
            place['state'] = get_state_google(result)
            place['country'] = get_country_google(result)
            return place
			
			
def reverse_geocode(latlng, reverse_geocode_function=reverse_geocode_google, use_cache=True):
    
    global geocode_cache, requests_count
    
    if use_cache and latlng in geocode_cache and pd.notnull(geocode_cache[latlng]):
        log.info('retrieving results from cache for lat-long "{}"'.format(latlng))
        return geocode_cache[latlng]
    else:
        place = reverse_geocode_function(latlng)
        #geocode_cache[latlng] = place
        log.info('stored place details in cache for lat-long "{}"'.format(latlng))
        
        requests_count += 1
        if requests_count % cache_save_frequency == 0: 
            save_cache_to_disk(geocode_cache, geocode_cache_filename)
            
        return place
		
		

def get_place_by_latlng(latlng, component):
    try:
        return place_dict[latlng][component]
    except:
        return None
		
		

df = pd.read_csv(working_filename, encoding='utf-8')
print('{:,} rows in dataset'.format(len(df)))


# create city, state, country, route columns only if they don't already exist
new_cols = ['city', 'state', 'country', 'neighborhood', 'route']
for col in new_cols:
    if not col in df.columns:
        df[col] = None
        
# drop the locations and timestamp_ms columns if they are still here
cols_to_remove = ['locations', 'timestamp_ms']
for col in cols_to_remove:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)
        
df.head()


# put latlng in the format google likes so it's easy to call their api
# and round to 7 decimal places so our cache's keys are consistent
# (so you don't get weird float precision artifacts like 114.1702368000000001)
df['latlng'] = df.apply(lambda row: '{:.7f},{:.7f}'.format(row['lat'], row['lon']), axis=1)


mask = pd.isnull(df['country']) & pd.isnull(df['state']) & pd.isnull(df['city']) & pd.isnull(df['neighborhood']) & pd.isnull(df['route'])
ungeocoded_rows = df[mask]
print('{:,} out of {:,} rows lack reverse-geocode results'.format(len(ungeocoded_rows), len(df)))
print('We will attempt to reverse-geocode up to {:,} rows with Google'.format(max_google_requests))

#Reverse-geocode location history with Google API

unique_latlngs = df['latlng'].dropna().sort_values().unique()
place_dict = {}


for latlng in unique_latlngs:
    place_dict[latlng] = reverse_geocode(latlng, reverse_geocode_google)
	
for component in ['country', 'state', 'city', 'neighborhood', 'route']:
    df[component] = df['latlng'].apply(get_place_by_latlng, args=(component,))
	

mask = pd.isnull(df['country']) & pd.isnull(df['state']) & pd.isnull(df['city']) & pd.isnull(df['neighborhood']) & pd.isnull(df['route'])
ungeocoded_rows = df[mask]
print('{:,} out of {:,} rows still lack reverse-geocode results'.format(len(ungeocoded_rows), len(df)))


#only use second-geocoder on last pass

if use_second_geocoder:
    unique_latlngs = ungeocoded_rows['latlng'].dropna().sort_values().unique()
    for latlng in unique_latlngs:
        place_dict[latlng] = reverse_geocode(latlng, reverse_geocode_nominatim)
    for component in ['country', 'state', 'city', 'neighborhood','route']:
        df[component] = df['latlng'].apply(get_place_by_latlng, args=(component,))

		
mask = pd.isnull(df['country']) & pd.isnull(df['state']) & pd.isnull(df['city']) & pd.isnull(df['neighborhood']) & pd.isnull(df['route'])
ungeocoded_rows = df[mask]
print('{:,} out of {:,} rows still lack reverse-geocode results'.format(len(ungeocoded_rows), len(df)))


df.tail()

# save cache to disk
save_cache_to_disk(geocode_cache, geocode_cache_filename)

# save the entire data set to the working file
df.to_csv(working_filename, encoding='utf-8', index=False)

# save the useful columns to a final output file
cols_to_retain = ['datetime', 'neighborhood', 'city', 'state', 'country', 'route', 'lat', 'lon']
df[cols_to_retain].to_csv(final_output_filename, encoding='utf-8', index=False)
