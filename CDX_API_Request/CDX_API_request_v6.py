import requests
import json
import time


# Define the API endpoint
cdx_url = "https://arquivo.pt/wayback/cdx"

# Newspapers to search
newsp = ['cmjornal.pt/*', 
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

# Tags to search within newspaper's links
tags = ['-chega-', '-ventura-']

# Process the response into a list
data = {}

# Define the maximum number of retries
max_retries = 2
delay_between_requests = 5 # seconds

# Function to handle requests with retries and delays
def fetch_data_w_retries(url, params, retries=max_retries):
    """
    Makes a GET request to the given URL with the given parameters, and 
    retries the request up to 'retries' times if it fails. If the request 
    fails after all retries, returns None.
    
    :param url: str, the URL to make the request to
    :param params: dict, the parameters to send with the request
    :param retries: int, the number of times to retry the request if it fails
    :return: requests.Response, or None if the request fails after all retries
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status() # Raise an error for 4xx or 5xx responses
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Attempt {attempt + 1} of {retries}")
            if attempt < retries - 1:
                print(f"Retrieved {len(data)} records.")
                time.sleep(delay_between_requests) # Wait before retrying
            else:
                print("Max retries reached. Skipping.")
                return None

# Check if the response is in NDJSON format
for i in newsp:
    for tag in tags:
        params = {
        'url': i,
        'fields': 'url,timestamp,status',
        'from': '20230101',
        'to': '20240101',
        'filter': 'original:'+tag,
        'output': 'json',
        'limit': '5000'
        }
        
        response = fetch_data_w_retries(cdx_url, params)

        if response:
            if response.status_code == 200:
                if response.headers.get('Content-Type') == 'text/x-ndjson':
                    # Process each line as a separate JSON object
                    for line in response.text.splitlines():
                        try:
                            record = json.loads(line)

                            status = record.get('status')

                            if status == '200':
                                data.append(record)
                            else:
                                if status is None:
                                    print(f"Record missing 'status' field: {record}")
                                    print(f"Retrieved {len(data)} records.")

                                else:
                                    print(f"Record with status '{status}': {record}")
                                    print(f"Retrieved {len(data)} records.")

                        except json.JSONDecodeError as e:
                            print(f"Error parsing line: {line}")
                            print(f"JSONDecodeError: {e}")
                        except TypeError as e:
                            print(f"Unexpected data format: {line}")
                            print(f"TypeError: {e}")
                else:
                    print("Response is not in NDJSON format.")
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        else:
            print("Failed to retrieve data.")

# Print the number of records retrieved
print(f"Retrieved {len(data)} records.")

# Insert the new data into cdx_results.json
with open("cdx_results.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
