# LOGGING
import logging 

# SCRAPING IMPORTS
import xmltodict
import functools 
import requests
import time 
import os

from datetime import datetime

# SQL IMPORTS
import sqlalchemy as sa
import pandas as pd

from sqlalchemy import column

# Bus Open API Key
bus_key = os.environ.get("BUS_API")

# SQL Environment Variables & Config 
sql_pwd = os.environ.get("SQL_PWD")
db_config = {
    'username': 'sa',
    'password': os.environ.get("SQL_PWD"),
    'server': os.environ.get("SQL_SERVER"),
    'port': '1433',
    'database': os.environ.get("BUS_DB"),
    'driver': 'ODBC Driver 18 for SQL Server',
    'table': os.environ.get("BUS_TABLE")
}

time_format = "%Y-%m-%d, %H:%M:%S"
def string_time_now():
    return datetime.strftime(datetime.now(), time_format)

def get_data():
    url = f"https://data.bus-data.dft.gov.uk/api/v1/datafeed/?lineRef=51&operatorRef=BORD&api_key={bus_key}"
    response = requests.get(url)

    if response.status_code != 200:
        logging.info('({string_time_now()}) Request Error. Status Code: {response.status_code}.')
        return [] 

    data_dict = xmltodict.parse(response.text)

    try:
        bus_keys = ["Siri", "ServiceDelivery", "VehicleMonitoringDelivery", "VehicleActivity"]
        buses = functools.reduce(dict.get, bus_keys, data_dict)
    except KeyError as e:
        print("Information not found: {e}")

    information = []

    for bus in buses:
        dt_format = "%Y-%m-%dT%H:%M:%S+00:00"
        timestamp = bus.get('RecordedAtTime') 

        journey = bus.get('MonitoredVehicleJourney')
        if not journey or not timestamp: 
            logging.info('({string_time_now()}) No timestamp or journey information.')
            continue 
    

        line = journey.get('PublishedLineName')
        origin = journey.get('OriginName')
        destination = journey.get('DestinationName')
        origin_est_departure = journey.get('OriginAimedDepartureTime')
        destination_est_arrival = journey.get('DestinationAimedArrivalTime')
        coords = journey.get('VehicleLocation')
        if coords:
            latitude = coords.get('Latitude')
            longitude = coords.get('Longitude')
        else:
            logging.info('{timestamp}: No coords')
            latitude = None
            longitude = None

        bearing = journey.get('Bearing')
        number_plate = journey.get('VehicleRef')
            
        direction = journey.get('DirectionRef')

        journey_id_keys = ["Extensions", "VehicleJourney", "Operational", "TicketMachine", "JourneyCode"]
        vehicle_id_keys = ["Extensions", "VehicleJourney", "VehicleUniqueId"]

        journey_id = functools.reduce(dict.__getitem__, journey_id_keys, bus)
        vehicle_id = functools.reduce(dict.__getitem__, vehicle_id_keys, bus)
        
        timestamp = datetime.strptime(timestamp, dt_format)
        if origin_est_departure:
            origin_est_departure = datetime.strptime(origin_est_departure, dt_format)
        if destination_est_arrival:
            destination_est_arrival = datetime.strptime(destination_est_arrival, dt_format)
       
        info_dict = {
            'time': timestamp,
            'line_ref': line,
            'vehicle_id': vehicle_id,
            'number_plate': number_plate,
            'journey_id': journey_id,
            'direction': direction,
            'origin': origin,
            'destination': destination,
            'origin_est_departure': origin_est_departure,
            'destination_est_arrival': destination_est_arrival,
            'longitude': longitude,
            'latitude': latitude,
            'bearing': bearing
        }
        information.append(info_dict)

    return information

def gen_connection(config):
    connection_uri = sa.engine.url.URL(
        'mssql+pyodbc',
        username=config['username'],
        password=config['password'],
        host=config['server'],
        port=config['port'],
        database=config['database'],
        query = { 
            'driver': config['driver'], 
            'TrustServerCertificate': 'yes'
        }
    )
    return connection_uri

def insert_to_sql(bus_data, config):
    connection_uri = gen_connection(config)
        
    column_names = [
        "id", 
        "time",
        "line_ref",
        "vehicle_id",
        "number_plate",
        "journey_id",
        "direction",
        "origin",
        "destination",
        "origin_est_departure",
        "destination_est_arrival",
        "latitude",
        "longitude",
        "bearing"
    ]
   
    columns = [column(x) for x in column_names] 

    table = sa.table(config["table"], *columns)

    engine = sa.create_engine(connection_uri, pool_recycle=360)
    with engine.begin() as conn:
        for bus in bus_data:
            insert_query = sa.insert(table).values(bus)
            compiled_insert = insert_query.compile()
            result = conn.execute(insert_query)
        conn.commit()


if __name__ == '__main__':
    FORMAT = "%(message)s"
    logging.basicConfig(filename='scraping.log', level=logging.INFO, format=FORMAT)
    # 2024-11-7 is 7th of November, 2024
    end_date = datetime(2024, 11, 7)
    
    connection_uri = gen_connection(db_config) 
    engine = sa.create_engine(connection_uri, pool_recycle=360)
    with engine.begin() as conn:
        query = sa.text(f'SELECT TOP 1 time FROM {db_config["table"]} ORDER BY id ASC')
        latest_time = pd.read_sql_query(query, conn)['time']
        if len(latest_time) == 0:
            latest_time = datetime.now()
        else:
            latest_time = latest_time[0]
    
    logging.info(f'({string_time_now()}) Scraping started.')
    while datetime.now() < end_date:
        bus_data = get_data()
        if len(bus_data) == 0:
            continue

        timestamp = bus_data[0]['time']
        if timestamp <= latest_time: 
            time.sleep(10)
            continue 

        insert_to_sql(bus_data, db_config)
        latest_time = timestamp 
        logging.info(f'({datetime.strftime(timestamp, time_format)}) Insertion.')
        print(f"({datetime.strftime(timestamp, time_format)}) Insertion.")
        time.sleep(10)

