import socket
import requests
from urllib.parse import urljoin

# def api_get_by_id(id):
#     target_url = "http://localhost:5000/bands/"
#     target_url = target_url + str(id)
#     res = requests.get(target_url)
#     print(res.json())

def api_add_entry(base_url, table_url, values):
    url = urljoin(base_url, f"{table_url}")
    print(f"connecting to url: {url}")
    try:
        res = requests.post(url, data=values)
        res.raise_for_status() 
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")

def api_delete_entry_by_id(base_url, table_url, id):
    target_url = urljoin(base_url, f"{table_url}/{id}")
    print(f'connecting to {target_url}')
    try:
        res = requests.delete(target_url)
        res.raise_for_status() 
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")

def api_get_by_id(base_url, id):
    target_url = urljoin(base_url, f"bands/{id}")
    print(f'connecting to {target_url}')
    try:
        res = requests.get(target_url)
        res.raise_for_status() 
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        
def api_get_table(base_url, table_name):
    target_url = urljoin(base_url, f"{table_name}")
    print(f'connecting to {target_url}')
    try:
        res = requests.get(target_url)
        res.raise_for_status()  # Raise an HTTPError for bad responses
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
    
#api_get_by_id(1)