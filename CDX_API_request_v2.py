import requests
import json

api_url = "https://arquivo.pt/wayback/cdx?url=publico.pt/*&fields=url,timestamp,status&from=2019&to=2024&filter=original:politica&output=json"

response = requests.get(api_url)
data = []

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

# print(response.status_code)

# data = response.text

# print(response.headers.get('Content-Type'))

with open("cdx_results.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
    

# if response.status_code == 200:
#     new_data = response.json()

#     try:
#         with open("cdx_results.json", 'w') as json_file:
#             existing_data = json.load(json_file)
#     except (FileNotFoundError, json.decoder.JSONDecodeError):
#         existing_data = []

#     existing_data.append(new_data)

#     with open("cdx_results".json, 'w') as json_file:
#         json.dump(existing_data, json_file, indent=4)
#         print("Data appended to data.json file")
# else:
#     print("Failed to retrieve data from the API. Status code: ", response.status_code)  

