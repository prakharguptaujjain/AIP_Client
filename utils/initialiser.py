"""This file is used to initialise the program, and to set the model to use, and the update frequency, (THIS IS DONE ONLY ONCE, for the first time the program is run)"""

import json
from utils.cronjob import *
import os
import time

def get_model_choice():
    while True:
        print("Please choose the model to use:")
        print("1. Alpha")
        print("2. Alpha7")
        print("3. Prioritize_Consistent")
        print("4. Prioritize_New")
        model_choice = input("Enter the number of the model you want to use: ")
        if model_choice in ["1", "2", "3", "4"]:
            model_index = int(model_choice) - 1
            models = ["Alpha", "Alpha7", "Prioritize_Consistent", "Prioritize_New"]
            return models[model_index]
        else:
            print("Invalid choice, please choose again.")

def initialise(CONFIG):
    #This code runs only once, so to set the model to use, and to set update frequency

    #Check if the config file exists
    if os.path.exists(CONFIG):
        with open(CONFIG) as f:
            data = json.load(f)
        if data['Initialised']:
            return
        
    print("This is the initialisation part of the program, if you want to reconfigure the program later time, please delete the config.json file and then run the program again")

    if not os.path.exists(CONFIG):
        print("\033[1mWe are intialising the program settings as a completely new one\033[0m")
        print("Do you want to continue? (y/n)")
        confirm = input("Enter your choice: ")
        if confirm.lower() == 'y':
            #delete files inside Blacklisted_IP
            if os.path.exists('Blacklisted_IP'):
                print("Deleting files in Blacklisted_IP directory...")
                for filename in os.listdir('Blacklisted_IP'):
                    file_path = os.path.join('Blacklisted_IP', filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file {filename}: {e}")
                

            print("Do you want to delete the cron job created earlier (if you didn't understand it just choose no)? (y/n)")
            
            confirm = input("Enter your choice: ")
            if confirm.lower() == 'y':
                del_grep_cronjobs()
        else:
            exit()

        #Create CONFIG file
        with open(CONFIG, 'w') as f:
            data = {}
            data['model to use'] = []
            data['Initialised'] = True
            data['auto_update_firewall'] = False
            data['created_cron'] = False
            data['advance_config'] = False

            #current time
            curr_time = time.time()
            data['initialised_time'] = curr_time
            json.dump(data, f)
                
               

    # Ask user for model choice for running the script for only first time
    print()
    model_choice = get_model_choice()

    # Ask user for update frequency in days
    create_cron_job=False
    while True:
        try:
            print("Do you want to create cron (i.e. automatically run the program with certain interval)? (y/n)")
            confirm = input("Enter your choice: ")
            if confirm.lower() == 'y':
                create_cron_job = True
                break
            elif confirm.lower() == 'n':
                create_cron_job = False
                break
        except ValueError:
            print("Invalid input. Please enter 'y' or 'n'.")
    if create_cron_job:
        while True:
            try:
                num_days = int(input("Please enter the update frequency in days: "))
                if num_days <= 0:
                    print("Invalid input. Please enter a positive integer.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

    while True:
        try:
            print("Do you want to automatically update the firewall blocklist using the downloaded blocklist_ips? (y/n)")
            confirm = input("Enter your choice: ")
            if confirm.lower() == 'y':
                auto_update_firewall_value = True
                break
            elif confirm.lower() == 'n':
                auto_update_firewall_value = False
                break
        except ValueError:
            print("Invalid input. Please enter 'y' or 'n'.")

    # Create cron job for main.py
    if create_cron_job:
        create_cron(num_days)


    # Update config file
    with open(CONFIG, 'r+') as f:
        data = json.load(f)
        data['model to use'] = [model_choice]
        data['auto_update_firewall'] = auto_update_firewall_value
        data['Initialised'] = True
        data['created_cron'] = create_cron_job
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()