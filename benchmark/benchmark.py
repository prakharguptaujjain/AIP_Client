import os
import json
import subprocess

CONFIG='config.json'


def initials():
    #Download Benchmark
    print("Downloading Benchmark. Please wait (this might take a while)")
    exit_code = os.system("bash ./benchmark/installer.sh")
    if exit_code != 0:
        print("Failed to install benchmark.")
        exit(1)
    else:
        print(f"\033[1mBenchmark installed successfully.\033[0m")

    # Do benchmark
    bench_value = subprocess.check_output("sysbench cpu --cpu-max-prime=20000 --time=1 run | grep 'events per second' | awk '   {print $NF}'", shell=True)

    #open config file
    with open(CONFIG) as f:
        data = json.load(f)
        
    # Set benchmark value in config file
    data['advance_configuration']['bench_value'] = bench_value.decode('utf-8').strip()
    with open(CONFIG, 'w') as f:
        json.dump(data, f)
    print(f"\033[1mBenchmark value set to: ", bench_value.decode('utf-8').strip())
