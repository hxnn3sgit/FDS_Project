import requests
import json
import itertools
import time

# Define the API endpoint
cdx_url = "https://arquivo.pt/wayback/cdx"

# Newspapers to search
newsp = [ 'cmjornal.pt/*', 
         'dn.pt/*',
         'sol.sapo.pt/*',
         'expresso.pt/*',
         ]

# Tags to search within newspaper's links
tags = ['politica', 'chega', 'ventura']

# Process the response into a list
data = []

# Check if the response is in NDJSON format
for i in newsp:
    for tag in tags:
        params = {
        'url': i,
        'fields': 'url,timestamp,status',
        'from': '2019',
        'to': '2020',
        'filter': 'original:'+tag,
        'output': 'json',
        'limit': '10'
        }
        
        response = requests.get(cdx_url, params=params)

        if response.status_code == 200:
            if response.headers.get('Content-Type') == 'text/x-ndjson':
                # Process each line as a separate JSON object
                for line in response.text.splitlines():
                    try:
                        record = json.loads(line)
                        if record['status'] == '200':
                            data.append(record)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line: {line}")
                        print(f"JSONDecodeError: {e}")
                    except TypeError as e:
                        print(f"Unexpected data format: {line}")
                        print(f"TypeError: {e}")
                    except requests.exceptions.Timeout:
                        print("The request timed out. Please try again later.")
                    except requests.exceptions.RequestException as e:
                        print(f"An error occurred: {e}")
            else:
                print("Response is not in NDJSON format.")
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break   

# Print the number of records retrieved
print(f"Retrieved {len(data)} records.")

# Insert the new data into cdx_results.json
with open("cdx_results.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
    

# 'folhanacional.pt/*',
# 'jn.pt/*',
# 'ionline.sapo.pt/*',
# 'sol.sapo.pt/*',
# 'observador.pt/*',
# 'publico.pt/*',
# 'sabado.pt/*',
# 'sapo.pt/*',
# 'visao.pt/*',
