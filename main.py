#!/usr/bin python3

import os
import json
import urllib.request
from bs4 import BeautifulSoup
from utils.initialiser import *
from utils.firewall_integrator import *
from utils.auto_trim_csv_using_bench_value import *
from utils.whitelisted_ip import *

CONFIG='config.json'
URL='https://mcfp.felk.cvut.cz/publicDatasets/CTU-AIPP-BlackList/Latest/'

def failure_config():
    print("\033[1mError: Please delete the config.json file and run the program again\033[0m")
    exit()

def download_file_with_model_name():
    print("Downloading updated blocklists_ip. Please wait (this might take a while)")
    # Open the config file
    with open(CONFIG) as f:
        data = json.load(f)

    #check if it contains model name
    if not data['model to use']:
        failure_config()
    
    # Extract the model name from the config file
    model_name = data['model to use'][0]

    url = URL

    # Fetch the HTML content of the directory
    response = urllib.request.urlopen(url)
    html = response.read().decode()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Filter out only the CSV files
    files = [link['href'] for link in soup.find_all('a') if link['href'].endswith('.csv')]

    # Sort the files in ascending order with respect to filename length (This is done to separate the Alpha from Alpha7, so that substr(Alpha7) is not Alpha)
    files = sorted(files, key=lambda x: len(x))
    
    # Iterate over the files and download the file with the model name
    for file in files:
        if model_name in file:
            if not os.path.exists('Blacklisted_IP'):
                os.makedirs('Blacklisted_IP')
            file_path = 'Blacklisted_IP/' + file
            if os.path.exists(file_path):
                os.remove(file_path)
            urllib.request.urlretrieve(url + file, file_path)
            print(f"\033[1mDownloaded Blocklist_IPS Successfully\033[0m")
            break
def goodbye():
    """This module prints a goodbye message"""
    print("################################")
    print("GOODBYE! (English)")
    print("ADIOS! (Spanish)")
    print("AU REVOIR! (French)")
    print("TCHAU! (Portuguese)")

def text_for_advanced_config():
    print("!!!!!!!!!!!!!!!")
    print("For advance configuration, please run the program",f"\033[1madvance_config.py\033[0m")
    print("!!!!!!!!!!!!!!!")

if __name__ == '__main__':
    # # Check if the user has sudo permissions
    # if os.geteuid() != 0:
    #     print("This script requires sudo permission to create a cron job. Please run this script again with sudo.")
    initialise(CONFIG)
    unblock_ip_firewall(CONFIG)
    download_file_with_model_name()
    whiteliste_ip()
    trim()
    block_ip_firewall(CONFIG)
    text_for_advanced_config()
    goodbye()
    
