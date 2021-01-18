import json
try:
    with open('config.json', 'r') as config_file:
        configdata = json.load(config_file)
        token = configdata["token"]
        prefix = configdata["prefix"]
        mongo_url = configdata["mongo_url"]
except:
    print("Invalid config.json file! Exiting now.")
    exit()