import aiohttp
import asyncio
import json 

async def fetch_multiple(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)
    return responses

async def fetch(session, url):
    async with session.get(url) as response:
        text = await response.text()
        print(text)
        return json.loads(text)

async def main():
    routes = ["51", "67", "X62"]
    base_url = "https://www.bordersbuses.co.uk/_ajax/lines/vehicles?lines%5B0%5D=BORD:"
    urls = [base_url + route for route in routes]

    requests = await fetch_multiple(urls)

    all_requests = [] 
    for req_json in requests:
        buses = req_json['features']
        
        relevant_features = []
        for bus in buses:
            coordinates = bus['geometry']['coordinates']
            
            properties = bus['properties']
            direction = properties['direction']
            line = properties['line']
            vehicle_id = properties['vehicle']
            fleet_number = properties['meta']['fleet_number']
            bearing = properties.get('bearing', None) 
            compass_direction = properties.get('compassDirection', None)

            relevant_features.append(
                    (
                        vehicle_id, 
                        fleet_number, 
                        line, 
                        bearing, 
                        compass_direction, 
                        coordinates
                    )
                )

        all_requests.append(relevant_features)
    
    return all_requests

results = asyncio.run(main())

results = [
    journey
    for j in results
    for journey in j
]

print(f"{results}")
# This is the information that I want to collect.
# Take from multiple bus services - X62, 51, 67

# Call every 30 seconds from 5am to 10pm. Run for one month as of Monday, the 7th of October.

# Each bus service will produce around 15MB of data over the month, no concerns on storage limits. Insert into SQL database after each request.

