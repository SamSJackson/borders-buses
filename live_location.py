import pandas as pd
import time 
import requests

req = requests.get("https://www.bordersbuses.co.uk/_ajax/lines/vehicles?lines%5B0%5D=BORD:51")

req_json = req.json()

buses = req_json['features']

relevant_features = []
for bus in buses:
    coordinates = bus['geometry']['coordinates']

    properties = bus['properties']
    direction = properties['direction']
    line = properties['line']
    vehicle_id = properties['vehicle']
    fleet_number = properties['meta']['fleet_number']
    bearing = properties['bearing']
    compass_direction = properties['compassDirection']


    relevant_features.append((vehicle_id, fleet_number, line, bearing, compass_direction, coordinates))

# This is the information that I want to collect.
# Take from multiple bus services - X62, 51, 67

# Call every 30 seconds from 5am to 10pm. Run for one month as of Monday, the 7th of October.

# Each bus service will produce around 15MB of data over the month, no concerns on storage limits. Insert into SQL database after each request.

