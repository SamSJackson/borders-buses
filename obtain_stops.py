import pandas as pd 
import requests

bus_route = input("Name bus route ID: ")

try:
    stops_req = requests.get(f"https://www.bordersbuses.co.uk/_ajax/lines/stops/BORD/{bus_route}")
    stops_json = stops_req.json()
except:
    print(f"Invalid bus route: {bus_route}")
    raise 


all_stops_info = stops_json['features']

'''
We want the following information from the features
- Stop Name
- Stop Coordinates
- atcoCode 
- stopType 
'''

information = []
for stop in all_stops_info: 
    coordinates = stop['geometry']['coordinates']
    properties = stop['properties']

    name = properties['commonName']
    stop_type = properties['stopType']
    atco = properties['atcoCode']

    information.append((atco, name, stop_type, coordinates))

df = pd.DataFrame(data=information, columns=["stop_id", "stop_name", "stop_type", "coordinates"])

try:
    df.to_csv(f"stops/live_route_{bus_route}.csv", index=False, mode='x')
    print(f"Written to CSV in /stops/live_route_{bus_route}.csv")
except FileExistsError as e:
    print("File already exists")
except:
    raise 


