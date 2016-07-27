# Huetiful Weather
A visual weather report for your favourite cities.

## Requirements
This script requires Python 2.6+, but at this stage won't work with 3+. All dependencies are included in requirements.txt. To install, simply run:

```pip install -r requirements.txt```

## Configuration
Change these variables to suit your needs.

```python
# Transition time in ms
transition_time = 2000

# WOEIDs for Melbourne, New York, and Paris. WOEID Lookup: http://woeid.rosselliot.co.nz/lookup
locations = (1103816, 2459115, 615702)

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

```

This script looks for environment variables called HUE_BRIDGE_IP and HUE_USERNAME.
```
ip = os.environ['HUE_BRIDGE_IP']            # IP of your Hue Bridge. nano ~/.bash_profile and add: export HUE_BRIDGE_IP="XXX.XXX.XXX.XXX"
username = os.environ['HUE_USERNAME']       # Username set up on your Hue Bridge.
```

## How it works
Hueforecast works by querying the Yahoo Weather API. The temperature is translated to a hue between blue and red, and saturation/brightness is affected by the environmental conditions. For example, if the weather is cold and rainy, the globe assigned to that location will appear a dim blue colour. If the weather is hot and clear, the globe assigned to that location will appear bright red.

## A note on WOEIDs
Yahoo's Weather API uses WOEIDs (Where On Earth) as a way of identifying locations. To find the WOEID of your preferred location, go to http://woeid.rosselliot.co.nz/lookup

## Running
```python huetifulweather.py```

To output the temperature and colour information, simply use a -d switch.

```python huetifulweather.py -d```

Example output:

```
Melbourne
	Fri, 22 Jul 2016 10:00 AM AEST
	Showers
	16.1c
	RGB: (2.1741898148148175, 1.9125000000000003, 6.375)
	HSB: (243.51851851851853, 70.0, 2.5)
-----
New York
	Thu, 21 Jul 2016 08:00 PM EDT
	Breezy
	27.8c
	RGB: (178.5, 0.0, 132.49768518518533)
	HSB: (315.46296296296293, 100.0, 70.0)
-----
Paris
	Fri, 22 Jul 2016 02:00 AM CEST
	Cloudy
	20.0c
	RGB: (3.957812500000003, 1.9125000000000003, 6.375)
	HSB: (267.5, 70.0, 2.5)
```

## Launchd
I run this script as a global daemon using launchd, which is terrible, so I have included a template (com.dan.huetifulweather.plist) to run it every 5 minutes. The file contains some environment variables and paths you will need to change before you load it, all variables are surrounded by braces ({}).

To install, simply run:

```launchctl load /path/to/com.dan.huetifulweather.plist```
