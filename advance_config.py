#!/usr/bin python3

import os
import json
import subprocess
from benchmark.benchmark import initials as bench_initials

CONFIG='config.json'
def save_configuration(advance_configuration):
    with open(CONFIG) as f:
        data = json.load(f)
    data['advance_config'] = True
    #loop over the advance_configuration dictionary and add it to the config file
    for key, value in advance_configuration.items():
        data['advance_configuration'][key] = value
    with open(CONFIG, 'w') as f:
        json.dump(data, f)


def init():
    with open(CONFIG) as f:
        data = json.load(f)
    #check if already configured
    if data['advance_config']==True:
        while True:
            try:
                print("Advance configuration are already done. Do you want to reconfigure advance configurations again(y/n)?")
                confirm = input("Enter your choice(y/n): ")
                if confirm.lower() == 'y':
                    break
                elif confirm.lower() == 'n':
                    exit(0)
            except ValueError:
                print("Invalid input. Please enter 'y' or 'n'.")

    advance_configuration={}
    save_configuration(advance_configuration)

    #ASK FOR AUTO TRIM
    while True:
        try:
            print("Do you want to add the amount of IP depending on your hardware performance? (y/n)")
            confirm = input("Enter your choice(y/n)?: ")
            if confirm.lower() == 'y':
                advance_configuration['auto_trim'] = True
                save_configuration(advance_configuration)
                bench_initials()
                break
            elif confirm.lower() == 'n':
                advance_configuration['auto_trim'] = False
                break
        except ValueError:
            print("Invalid input. Please enter 'y' or 'n'.")

    save_configuration(advance_configuration)


if __name__ == '__main__':
    init()