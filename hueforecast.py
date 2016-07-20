from beautifulhue.api import Bridge
from time import sleep
from sys import stdout
from numpy import clip, interp
from lib import ColorHelper, Converter
import os
import requests
import datetime
import colorsys
import copy
import argparse

# Number of seconds to wait between requests
interval = 60

# Transition time in ms
transition_time = 2000

# WOEIDs for Melbourne, New York, and Paris. WOEID Lookup: http://woeid.rosselliot.co.nz/lookup
locations = [1103816, 2459115, 615702]

# Minimum temperature
temp_min = 5

# Maximum temperature
temp_max = 35

# Start hue: Blue
hue_min = 175

# End hue: Red
hue_max = 360

# Default saturation
saturation = 100

# Default brightness
brightness = 100

# Yahoo Weather API endpoint
endpoint = 'https://query.yahooapis.com/v1/public/yql'

# Querystring object
querystring = { 'q': 'select * from weather.forecast where woeid={0}', 'format': 'json', 'env': 'store://datatables.org/alltableswithkeys' }

# Colour converter
converter = Converter()

# IP of your Hue Bridge. nano ~/.bash_profile and add: export HUE_BRIDGE_IP="XXX.XXX.XXX.XXX"
ip = os.environ['HUE_BRIDGE_IP']

# Username set up on your Hue Bridge.
username = os.environ['HUE_USERNAME']

# Bridge object
bridge = Bridge(device={ 'ip': ip }, user={ 'name': username })

# Colour map
hsvmap = [ { 'text': ['Thunderstorms', 'Rain'], 'saturation': 0.5, 'brightness': 0.01 },
	{ 'text': ['Cloudy', 'Mostly Cloudy', 'Showers'], 'saturation': 0.75, 'brightness': 0.05 },
	{ 'text': ['Partly Cloudy', 'Scattered Showers'], 'saturation': 0.95, 'brightness': 0.4 },
	{ 'text': ['Mostly Sunny'], 'saturation': 0.9, 'brightness': 0.5 },
	{ 'text': ['Clear', 'Breezy'], 'saturation': 1.0, 'brightness': 0.8 },
	{ 'text': ['Sunny'], 'saturation': 1.0, 'brightness': 1.0} ]


# Convert farenheit to celcius because Americans are barbarians
def farenheit_to_celsius(temp):
	return (temp-32)/1.8

# Convert temperature to HSV
def temp_to_hsv(temp):
	return (interp(clip(temp, temp_min, temp_max), [temp_min, temp_max], [hue_min, hue_max]), saturation, brightness)

def run(debug):
	try:
		globe = 1
		# Loop through each location
		for woeid in locations:
			# Deep copy the querystring object
			query = copy.deepcopy(querystring)
			query['q'] = query['q'].format(woeid)

			# Send the request
			response = requests.get(endpoint, params=query)

			# Get the response
			json = response.json()

			# Get the first day of the forecast
			day = json['query']['results']['channel']['item']['forecast'][0]

			# Get the location
			location = json['query']['results']['channel']['location']['city']

			text = day['text']
			date = day['date']
			high = int(day['high'])
			temp = farenheit_to_celsius(high)
			h,s,b = temp_to_hsv(temp)

			# Map the weather description to the colour
			lookup = [item for item in hsvmap if text in item['text']]

			# If there's a match, then change the saturation and brightness
			if lookup:
				s = s*lookup[0]['saturation']
				b = b*lookup[0]['brightness']

			# Convert to RGB
			red,green,blue = colorsys.hsv_to_rgb(h/360, b/100, s/100)

			# Convert to XY
			xy = converter.rgbToCIE1931(red,green,blue)

			# Debugging
			if debug:
				print(location)
				print(date)
				print(text)
				print("%.1fc" % round(temp,1))
				print('-----')

			# JSON sent to the Hue Bridge
			resource = {
				'which': globe,
				'data':{
					'state':{ 'on': True, 'xy':xy, 'bri': int((b/100)*254), 'transitiontime': (transition_time/100) }
				}
			}

			# Update the globe
			bridge.light.update(resource)
			globe+=1

	except Exception as e:
		print("Exception: %s" % str(e))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', action='store_true')
	args = parser.parse_args()

	while True:
		run(args.d)
		sleep(interval)
