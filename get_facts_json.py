import requests
import json

url = "https://myhotel.giatamedia.com/i18n/facts/en"
response = requests.get(url)

# Ensure we fail fast if the web request failed
response.raise_for_status()

data = response.json()
# print(data)

# Save the data to a JSON file
with open('./data/facts.json', 'w') as f:
    json.dump(data, f)