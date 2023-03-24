import json
import os 

CONFIG='config.json'
TRIMMED_VALUE_CONSTANT = 0.1

def trim():
    #check if advance_config as well as auto_trim is done
    with open(CONFIG) as f:
        data = json.load(f)
    if data['advance_config'] == False:
        return
    if data['advance_configuration']['auto_trim'] == False:
        return
    bench_value = float(data['advance_configuration']['bench_value'])
    TRIMMED_CNT = int(bench_value*TRIMMED_VALUE_CONSTANT)

    #return if advance_config is not done
    if data['advance_config'] == False:
        return
    
    current_dir = os.getcwd()
    #csv directory
    csv_folder = os.path.join(current_dir, 'Blacklisted_IP')

    for file in os.listdir(csv_folder):
        if file.endswith('.csv'):
            csv_dir = os.path.join(csv_folder, file)

            #Trim csv file
            with open(csv_dir) as f:
                lines = f.readlines()
                lines = lines[:TRIMMED_CNT]

            with open(csv_dir, 'w') as f:
                f.writelines(lines)
