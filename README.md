# AIP_Client
This script downloads the latest list of blocked IPs generated by the AIP software and hosted at https://mcfp.felk.cvut.cz/publicDatasets/CTU-AIPP-BlackList/Latest/

## It has two functionalitites
--> It downloads the preferred latest blocklist_ip.csv model, and can set a cron job for the same

--> It also updates the firewall blocklist using the blocklist_ip.csv

-->Has an whitelist_ip.csv to not block user given ip

### Advance Configuration
--> Using benchmark, add only minimal amount of ip according to compute power of cpu

## How to install
First download the repository, Then

```pip install -r requirements.txt```

change directory to inside the downloaded folder

```python3 ./main.py```
