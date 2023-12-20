import socket
import requests
from urllib.parse import urljoin

# def api_get_by_id(id):
#     target_url = "http://localhost:5000/bands/"
#     target_url = target_url + str(id)
#     res = requests.get(target_url)
#     print(res.json())

# for future use
def api_get_by_id(base_url, id):
    target_url = urljoin(base_url, f"bands/{id}")
    print(f'connecting to {target_url}')
    try:
        res = requests.get(target_url)
        res.raise_for_status()  # Raise an HTTPError for bad responses
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        
def get_table(base_url, table_name):
    target_url = urljoin(base_url, f"{table_name}")
    print(f'connecting to {target_url}')
    try:
        res = requests.get(target_url)
        res.raise_for_status()  # Raise an HTTPError for bad responses
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
    
#api_get_by_id(1)