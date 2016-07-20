# Hueforecast
A visual weather report for your favourite cities.

## Requirements
This script requires Python 2.6+, but at this stage won't work with 3+. All dependencies are included in requirements.txt. To install, simply run:

```pip install -r requirements.txt```

## Configuration
Change these variables to suit your needs.

```python
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
```python huemovie.py```

For extra information, simply use a -d switch.
```python hueforecast.py -d```

The script will run on a loop until you cancel it.
