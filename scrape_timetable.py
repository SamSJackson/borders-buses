from bs4 import BeautifulSoup
from selenium import webdriver

def setup_method():
    """Set up webdriver."""
    options = webdriver.FirefoxOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')

    geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

    driver = webdriver.Firefox(options=options, service=driver_service)
    return driver


#bus_route = input("Name bus route ID: ")
#date = input("Input date in format YYYY-MM-DD: ")
#is_outbound = input("Outbound? [Y/N]: ")

#if is_outbound.lower() in ["yes", "y"]:
#    direction = "outbound"
#else:
#    direction = "inbound"

bus_route = "51"
date = "2024-10-02"
direction = "outbound"

url = f"https://www.bordersbuses.co.uk/services/BORD/{bus_route}?date={date}&direction={direction}&all=on"

driver = setup_method()
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
tables = soup.find_all('table')

if len(tables) != 1:
    raise "Too many tables on this site"

table = tables[0]

for row in table.tbody.find_all('tr'):
    columns = row.find_all('td')
    
    if len(columns) == 0:
        continue 

    # Now, I must inspect the table on the website and make the appropriate dataframe.  
