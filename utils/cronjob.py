"""This module is used to create or delete cron jobs for the main.py program."""

import os
import platform
import subprocess
import json

def create_cron(num_days):
    """This module creates a cron job or scheduled task to run the main script at a specified interval."""
    # Get the current working directory
    current_dir = os.getcwd()

    # Ask the user to confirm that the current directory contains the main script
    while True:
        confirm = input(f"The current directory is {current_dir}. Is this the correct location for the main.py script? (y/n): ")
        if confirm.lower() == 'y':
            script_path = os.path.join(current_dir, 'main.py')
            break
        elif confirm.lower() == 'n':
            script_path = input("Please enter the path to the main script: ")
            if not os.path.exists(script_path):
                print("The path you entered is not valid.")
                continue
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    #Check from config file if the user wants to automatically update the firewall rules
        
    # Check the type of OS
    os_name = platform.system()
    if os_name == "Linux":
        # Create a daily cron job on Linux
        command = f'(crontab -l ; echo "0 0 */{num_days} * * python3 {script_path}") | crontab -'
        subprocess.call(command, shell=True)
        print("Cron job created successfully!")
    elif os_name == "Windows":
        # Create a scheduled task on Windows
        command = f'schtasks /create /tn "Python Script Task" /tr "python {script_path}" /sc daily /mo {num_days} /st 00:00'
        subprocess.call(command, shell=True)
        print("Scheduled task created successfully!")
    else:
        print("Unsupported operating system.")
        exit()
    print("Currently the created cronjob cannot update firewall rules, as cron job is not created in administrative mode")

def del_grep_cronjobs():
    """This module greps the cronjobs containing 'main.py' and prints them and asks the user to enter the number of the cronjob to delete"""
    output = os.popen('crontab -l | grep "main.py"').read().strip().split('\n')
    print("Cronjobs containing 'main.py':\n")
    print("No.")
    for i, cronjob in enumerate(output):
        print(f" {i+1}  -> {cronjob}")
    print("To skip deletion select 0 as the number")
    choice = input("Enter the number of the cronjob you want to delete: ")
    if(choice=='0'):
        return
    os.system("crontab -l | sed '{}d' | crontab -".format(choice))
    print("Cronjob deleted successfully!")
