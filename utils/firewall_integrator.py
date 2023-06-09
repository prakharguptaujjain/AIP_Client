import csv
import os
import platform
import signal
import json
import time
import subprocess
import re
from tqdm import tqdm
import signal
import sys


def signal_handler(sig, frame):
    """"Signal handler for SIGINT"""
    print("\n\n\033[1mProcess interrupted by user\033[0m")
    sys.exit(0)

def block_ip_firewall(CONFIG):
    """Block the IPs in the firewall using Blacklisted_IP.csv"""
    #whether to use auto_update_firewall
    with open(CONFIG, 'r+') as f:
        data = json.load(f)
        auto_update_firewall_value=data['auto_update_firewall']

    if auto_update_firewall_value == True:
        print("\033[1mPlease enter the password for sudo if prompted, (enter within 30 seconds)\033[0m")
        if os.system("sudo -v") != 0:
            # set a 30-second timeout to wait for user input
            def handler(signum, frame):
                raise Exception("30 seconds elapsed, password not entered")
            
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(30)
            
            try:
                # Ask for sudo password
                os.system("sudo -v")
                
                # Reset the alarm
                signal.alarm(0)
            except Exception as e:
                print(str(e))
                return
        if os.system("sudo -v") != 0:
            print("Run the script with sudo privileges")
            exit()
        print("Updating firewall rules with the latest IPs to be blocked...")

        # Specify the folder to the CSV files containing the IPs to be blocked
        csv_folder = os.path.join(os.getcwd(), 'Blacklisted_IP')
        # Join all the CSV files in the folder into a single CSV file (removing the header row from all thefiles except the first one)
        IP_to_be_blocked = []
        for file in os.listdir(csv_folder):
            if file.endswith('.csv'):
                with open(os.path.join(csv_folder, file), 'r') as infile:
                    reader = csv.reader(infile)
                    if file == os.listdir(csv_folder)[0]:
                        IP_to_be_blocked = [row[0] for row in reader]
                    else:
                        next(reader)  # skip the header row
                        IP_to_be_blocked += [row[0] for row in reader]
        # The name of the firewall chain to add the rules to
        chain_name = 'BLOCK_IPS_AIP'

        # check if the chain not already exists
        current_platform = platform.system()
        chain_name_present = False

        if current_platform == 'Linux':
            # Get all the chain names using the iptables command and regex
            command = "sudo iptables -L -n"
            output = subprocess.check_output(command, shell=True).decode('utf-8')
            chain_names = re.findall(r"Chain\s(\w+)", output)

            # Check if the chain already exists in the list of chain names
            if chain_name in chain_names:
                chain_name_present = True
            else:
                # If the chain name does not exist, create it
                command = f'sudo iptables -N {chain_name}'
                subprocess.call(command, shell=True)
                print(f"Firewall RuleChain-, Chain '{chain_name}' created successfully.")
            
            # Set the signal handler for SIGINT
            signal.signal(signal.SIGINT, signal_handler)

            print(f"Adding rules to firewall chain '{chain_name}'...")
            # Your existing code
            print("\033[1mPlease ignore legacy host/network error, if any\033[0m")
            print("Total rules to be added: ", len(IP_to_be_blocked))
            ETA=round(len(IP_to_be_blocked)/50)
            print(f"This will take a while , between {ETA/4} to {ETA} seconds")
            while True:
                print("Do you want to continue? (y/n)")
                choice=input("Enter your choice: ")
                if choice.lower() == 'n':
                    return
                elif choice.lower() == 'y':
                    break
                else:
                    print("Invalid choice, please enter 'y' or 'n'")
            
            print("\033[1mPlease see the update progress of adding rules to firewall below\033[0m")
            # Loop through the IP addresses and add each one to the firewall chain
            with tqdm(total=len(IP_to_be_blocked)) as pbar:
                for ip_address in IP_to_be_blocked:
                    # Block IPs on Linux-based systems using iptables
                    if current_platform == 'Linux':
                        os.system(f'sudo iptables -A {chain_name} -s {ip_address} -j DROP')
                    # Block IPs on macOS using pfctl
                    elif current_platform == 'Darwin':
                        os.system(f'sudo pfctl -t {chain_name} -T add {ip_address}')
                    # Block IPs on Windows using PowerShell
                    elif current_platform == 'Windows':
                        os.system(f'powershell.exe New-NetFirewallRule -DisplayName "Block {ip_address}" -Direction Inbound             -LocalAddress Any -RemoteAddress {ip_address} -Action Block')
                    else:
                        print(f'Error: Platform "{current_platform}" not supported')
                        sys.exit(1)
                    pbar.update(1)
            print("\033[1mFirewall rules added successfully, please ignore legacy host/network error, if any\033[0m")


def unblock_ip_firewall(CONFIG):
    """Remove the IPs in the firewall using Blacklisted_IP.csv(This is done to remove the IPs which were defined by old Blacklisted_IP.csv)"""
    #Check if the intialised time is less than 2 minute
    with open(CONFIG, 'r+') as f:
        data = json.load(f)
        init_time=data['initialised_time']
        if time.time()-init_time<120:
            return
        

    #whether to use auto_update_firewall
    with open(CONFIG, 'r+') as f:
        data = json.load(f)
        auto_update_firewall_value=data['auto_update_firewall']

    if auto_update_firewall_value == True:
        print("\033[1mPlease enter the password for sudo if prompted, (enter within 30 seconds)\033[0m")
        
        #if sudo is not already cached
        if os.system("sudo -v") != 0:
            # set a 30-second timeout to wait for user input
            def handler(signum, frame):
                raise Exception("30 seconds elapsed, password not entered")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(30)
            try:
                # Ask for sudo password
                os.system("sudo -v")
                # Reset the alarm
                signal.alarm(0)
            except Exception as e:
                print(str(e))
                return
    else:
        return
    
    if os.system("sudo -v") != 0:
        print("Run the script with sudo privileges")
        exit()
    print("Deleting firewall rules of the previous Blocked_IP.csv...")

    # Specify the folder to the CSV files containing the IPs to be unblocked
    csv_folder = os.path.join(os.getcwd(), 'Blacklisted_IP')

    # The name of the firewall chain to add the rules to
    chain_name = 'BLOCK_IPS_AIP'

    # check if the chain not already exists
    current_platform = platform.system()
    chain_name_present = False

    if current_platform == 'Linux':
        # Get all the chain names using the iptables command and regex
        command = "sudo iptables -L -n"
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        chain_names = re.findall(r"Chain\s(\w+)", output)

        # Check if the chain already exists in the list of chain names
        if chain_name in chain_names:
            chain_name_present = True
        else:
            # If the chain name does not exist, create it
            command = f'sudo iptables -N {chain_name}'
            subprocess.call(command, shell=True)
            print(f"Firewall RuleChain-, Chain '{chain_name}' created successfully.")


    # Get the current platform
    current_platform = platform.system()
    # Delete all rules in the chain
    if current_platform == 'Linux':
        os.system(f'sudo iptables -F {chain_name}')
        os.system(f'sudo iptables -X {chain_name}')
    elif current_platform == 'Darwin':
        os.system(f'sudo pfctl -t {chain_name} -T flush')
    elif current_platform == 'Windows':
        os.system(f'powershell.exe Remove-NetFirewallRule -DisplayName "Block all {chain_name}"')
    else:
        print(f'Error: Platform "{current_platform}" not supported')
    print(f"\033[1mAll Firewall rules in {chain_name} chain deleted successfully\033[0m")
