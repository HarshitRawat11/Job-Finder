from dotenv import load_dotenv
import requests
import json
import os

load_dotenv('job-saas/.env')

headers = {
    "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
    "Content-Type": "application/json",
}

# params = {
#     # "dataset_id": "gd_lpfll7v5hcqtkxl6l",
#     # "include_errors": "true",
#     # "type": "discover_new",
#     # "discover_by": "keyword",
#     "limit_per_input": "5"
# }

# data = json.dumps({
#     "input": [{"location":"paris","keyword":"product manager","country":"FR","time_range":"Past month","job_type":"Full-time","experience_level":"Internship","remote":"On-site","company":"","location_radius":""}],
# })

# response = requests.post(
#     "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true&type=discover_new&discover_by=keyword",
#     headers=headers,
#     params=params,
#     data=data
# )

# print(response.json())

snapshot_id = 'sd_mlwf8e70zb6o23xy3'
# url = f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}'

# print(requests.get(url, headers=headers).json()['status'])

url = f'https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json'

response = requests.get(url, headers=headers)

response.raise_for_status()

print(response.json())