import requests
import json

# Define the API endpoint
cdx_url = "https://arquivo.pt/wayback/cdx"

# Make the request to the API
params = {
    'url': 'publico.pt/*',
    'fields': 'url,timestamp,status',
    'filter': 'original:politica',
    'from': '2017',
    'to': '2020',
    'filter': '!=timestamp:*2018',
    # 'filter': 'timestamp:!=2017',
    # 'filter': 'timestamp:!=2016',
    # 'filter': 'timestamp:!=2015',
    # 'filter': 'timestamp:!=2014',
    # 'filter': 'timestamp:!=2013',
    'output': 'json',
    'limit': '20000'
}

type(params)

# Request data
response = requests.get(cdx_url, params=params)

# Process the response into a list
data = []

# Check if the response is in NDJSON format
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
    # If status code is not 200, skip this instance and move to the next
    print(f"Skipping due to response status: {response.status_code}")

# Insert the new data into cdx_results.json
with open("cdx_results.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
    
