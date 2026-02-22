import os
import requests
from dotenv import load_dotenv
import json
import time

from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv('job-saas/.env')

@tool('search_jobs_linkedin', description='Search Linkedin for job listings using parameters (location, keyword, country, experience_level, job_type, company, remote, location_radius, time_range) based on user input. This function returns all found job listings.')
def search_jobs_on_linkedin(
        location: str, 
        keyword: str, 
        country: str, 
        job_type: str,
        experience_level: str, 
        company: str, 
        remote: str, 
        location_radius: str, 
        time_range: str = 'Past month'
):

    url = f'https://api.brightdata.com/datasets/v3/trigger'


    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    params = {
        "dataset_id": "gd_lpfll7v5hcqtkxl6l",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
        "limit_per_input": "5"
    }

    data = json.dumps({
        "input": [
            {
                "location":location,
                "keyword":keyword,
                "country":country,
                "time_range":time_range,
                "job_type":job_type,
                "experience_level":experience_level,
                "remote":remote,
                "company":company,
                "location_radius":location_radius,
            }],
    })

    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true&type=discover_new&discover_by=keyword",
        headers=headers,
        params=params,
        data=data
    )

    response.raise_for_status()
    
    snapshot_id = response.json()['snapshot_id']
    
    # 'sd_mlwf8e70zb6o23xy3'

    url = f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}'

    while requests.get(url, headers=headers).json()['status'] != 'ready':
        time.sleep(5)

    url = f'https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json'

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()

@tool('search_jobs_glassdoor', description='Search Glassdoor for job listings using parameters (location, keyword, country) based on user input. This function returns all found job listings.')
def search_jobs_on_glassdoor(
        location: str, 
        keyword: str, 
        country: str, 
):

    url = f'https://api.brightdata.com/datasets/v3/trigger'


    headers = {
        "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
        "Content-Type": "application/json",
    }

    params = {
        "dataset_id": "gd_l7j0bx501ockwldaqf",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
        "limit_per_input": "5"
    }

    data = json.dumps({
        "input": [
            {
                "location":location,
                "keyword":keyword,
                "country":country,
            }],
    })

    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_lpfll7v5hcqtkxl6l&notify=false&include_errors=true&type=discover_new&discover_by=keyword",
        headers=headers,
        params=params,
        data=data
    )

    response.raise_for_status()
    
    snapshot_id = response.json()['snapshot_id']
    
    url = f'https://api.brightdata.com/datasets/v3/progress/{snapshot_id}'

    while requests.get(url, headers=headers).json()['status'] != 'ready':
        time.sleep(5)

    url = f'https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json'

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()


def search_jobs_with_agent(prompt: str) -> str:
    agent = create_agent(
        model='gpt-4.1-mini',
        tools=[search_jobs_on_linkedin, search_jobs_on_glassdoor]
    )

    response = agent.invoke({
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant for finding job listings via Linkedin and Glassdoor based on user prompts.'},
            {'role': 'user', 'content': prompt}
        ]
    })

    return response['messages'][-1].content