import requests
import json
import itertools

# Define the API endpoint
cdx_url = "https://arquivo.pt/wayback/cdx"

# Newspapers to search
newsp = [ 'cmjornal.pt/*', 
         'dn.pt/*',
         'expresso.pt/*',
         'folhanacional.pt/*',
         'ionline.sapo.pt/*',
         'jn.pt/*',
         'observador.pt/*',
         'publico.pt/*',
         'sabado.pt/*',
         'sapo.pt/*',
         'sol.sapo.pt/*',
         'visao.pt/*',
         ]

# Tags to search within newspaper's links
tags = ['politica',
        'atualidade'
        'portugal'
        'detalhe'
        ]

# Process the response into a list
data = []

# Check if the response is in NDJSON format
for i in newsp:
    for tag in tags:
        params = {
        'url': i,
        'fields': 'url,timestamp,status',
        'from': '2019',
        'to': '2024',
        'filter': 'original:'+tag,
        'output': 'json',
        'limit': '1'
        }
        
        response = requests.get(cdx_url, params=params)

        if response.status_code == 200:
            if response.headers.get('Content-Type') == 'text/x-ndjson':
                # Process each line as a separate JSON object
                for line in response.text.splitlines():
                    try:
                        data.append(json.loads(line)) 
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line: {line}")
                        print(f"JSONDecodeError: {e}")
            else:
                print("Response is not in NDJSON format.")
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break   

# Insert the new data into cdx_results.json
with open("cdx_results.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
    
