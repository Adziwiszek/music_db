import socket
import requests
from urllib.parse import urljoin


def api_add_entry(base_url, table_url, values):
    '''Api call for add_entry
        Parameters:
        base_url (string): server url
        table_url (string): name of a table, used for choosing table for the action
        values (dict): values of a new entry'''
    url = urljoin(base_url, f"{table_url}")
    print(f"connecting to url: {url}")
    try:
        res = requests.post(url, data=values)
        res.raise_for_status()
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")


def api_delete_entry_by_id(base_url, table_url, id):
    '''Api call for delet_entry_by_id
        Parameters:
        base_url (string): server url
        table_url (string): name of a table, used for choosing table for the action
        id (int): id of entry that will be deleted'''
    target_url = urljoin(base_url, f"{table_url}/{id}")
    print(f'connecting to {target_url}')
    try:
        res = requests.delete(target_url)
        res.raise_for_status()
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")


def api_get_by_id(base_url, table_url, id):
    '''Api call for get_by_id
        Parameters:
        base_url (string): server url
        table_url (string): name of a table, used for choosing table for the action
        id (int): id of the entry
        '''
    target_url = urljoin(base_url, f"{table_url}/{id}")
    print(f'connecting to {target_url}')
    try:
        res = requests.get(target_url)
        res.raise_for_status()
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")


def api_get_table(base_url, table_url):
    '''Api call for get_by_id
        Parameters:
        base_url (string): server url
        table_url (string): name of a table, used for choosing table for the action'''
    target_url = urljoin(base_url, f"{table_url}")
    print(f'connecting to {target_url}')
    try:
        res = requests.get(target_url)
        res.raise_for_status()  # Raise an HTTPError for bad responses
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")


def api_update_entry(base_url, table_url, values):
    '''Api call for get_by_id
        Parameters:
        base_url (string): server url
        table_url (string): name of a table, used for choosing table for the action
        values (dict): values that will be updated'''
    url = urljoin(base_url, f"{table_url}")
    print(f"connecting to url: {url}")
    try:
        res = requests.put(url, data=values)
        res.raise_for_status()
        print(res.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
