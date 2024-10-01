# Scraping Buses

Borders Buses has a live tracking tool which allows us to scrape live information and view how frequently that the buses are on time.

## Goal 
Determine bus route which is typically latest, and by how much.

Importantly, I want to know how late the 51 is, and how often. 

## How 

We can scrape the following information from the borders buses website.

Static information:
- Routes
    - Name of Route
    - Stops
        - Stop time 
        - Location/Coordinates


Live information:
- Bus 
    - Bus location
    - Bus numberplate
    - Live route.

From this, we can determine if it is at the stop on time, determined from the location of our static information collected.

## Information on How to Scrape

Scraping this will not be easy and it will require having the process running permanently for a long period, perhaps many weeks.

### Live Scraping

Information on the location of a given bus is served by such an address:
``` https://www.bordersbuses.co.uk/services/BORD/51 ```

Response is in a json-format (praise). 

### Static Scraping

The static information such as stop times and names is readily available but the coordinate location is not publicly available.
We will have to coordinate the stop times with the coordinates based on the scraping - which shows stop name and coordinates, fortunately, so we can pair by name.

The stop information, for coordinate locations, can be found using this following link: 
``` https://www.bordersbuses.co.uk/_ajax/lines/stops/BORD/51 ```

Note that the final directory denotes the bus route number. Hence, this is the stops for the bus route 51.
