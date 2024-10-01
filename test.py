import requests

response = requests.get('https://www.bordersbuses.co.uk/_ajax/lines/stops/BORD/X62')

print(response.json())
