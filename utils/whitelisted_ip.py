import json
import os 


def whiteliste_ip():
    current_dir = os.getcwd()

    #white_listedcsv directory
    WHITE_LIST_IP=[]
    csv_folder = os.path.join(current_dir, 'whitelisted_ip')
    for file in os.listdir(csv_folder):
        if file.endswith('.csv'):
            csv_dir = os.path.join(csv_folder, file)
            with open(csv_dir) as f:
                lines = f.readlines()
                for line in lines:
                    WHITE_LIST_IP.append(line.strip())

    #black_listedcsv directory
    csv_folder = os.path.join(current_dir, 'Blacklisted_IP')

    for file in os.listdir(csv_folder):
        if file.endswith('.csv'):
            csv_dir = os.path.join(csv_folder, file)

            #remove white_listed ip from black_listed ip
            with open(csv_dir) as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() in WHITE_LIST_IP:
                        lines.remove(line)
            
            with open(csv_dir, 'w') as f:
                f.writelines(lines)
