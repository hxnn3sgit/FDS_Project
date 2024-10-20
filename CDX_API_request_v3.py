import requests
import json

# Define the API endpoint
cdx_url = "https://arquivo.pt/wayback/cdx"

# Newspapers to search
newsp = [ 'cmjornal.pt/*', 
         'dn.pt/*',
         'expresso.pt/*',
         'folhanacional.pt/*',
         'jn.pt/*',
         'ionline.sapo.pt/*',
         'sol.sapo.pt/*',
         'observador.pt/*',
         'publico.pt/*',
         'sabado.pt/*',
         'sapo.pt/*',
         'visao.pt/*',
         ]

for i in newsp:
    print(i)

# Make the request to the API
params = {
    'url': 'publico.pt/*',
    'fields': 'url,timestamp,status',
    'from': '2019',
    'to': '2024',
    'filter': 'original:politica',
    'output': 'json',
    'limit': '10'
}

type(params)

# Request data
response = requests.get(cdx_url, params=params)

# Process the response into a list
data = []

# Check if the response is in NDJSON format
if response.headers.get('Content-Type') == 'text/x-ndjson':
    # Process each line as a separate JSON object
    for line in response.text.splitlines():
        try:
            data.append(json.loads(line)) #
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {line}")
            print(f"JSONDecodeError: {e}")
else:
    print("Response is not in NDJSON format.")

# Insert the new data into cdx_results.json
with open("cdx_results.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
    
