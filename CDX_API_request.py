import requests
import json
import pandas as pd

# Define the API endpoint and query parameters
api_request = "https://arquivo.pt/wayback/cdx?url=publico.pt/*&fields=url,timestamp,status&from=2019&to=2024&filter=original:politica"

# Make the request to the API
# response = requests.get(api_request)
# data = response.json()


# for i in response:
#     data.append(i)
#     print(i)

# print("\n ola")       
#save the data to a JSON file
file_path = '/Users/joaop.cardoso/MestradoCD/FCD/Code/cdx_results.json'

f = open(file_path, 'w', encoding='utf-8')

with open('cdx_results.json', 'w') as file:
    json.dump(requests.get(api_request).json(), file_path, ensure_ascii=False, indent=4)



