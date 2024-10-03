import requests

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://www.bordersbuses.co.uk/services/BORD/X62',
    'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

response = requests.get("https://www.bordersbuses.co.uk/_ajax/lines/vehicles?lines%5B0%5D=BORD:X62", headers=headers)

print(response.text)
