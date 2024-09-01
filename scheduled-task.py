import json
import datetime
import time

from solana import get_validator_count, get_block_time

def add_validator_count():
    with open('./data/validator-data.json', 'r') as file:
        data = json.load(file)
    
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    hour = now.hour
    
    current_data = data.get(date, {})
    
    data[date] = {
        **current_data,
        str(hour): {
            "validator_count": get_validator_count()
        },
        "average_count": 0
    }
    
    data_len = len(data.get(date, {}).keys())
    
    if data_len:
        data[date]["average_count"] = sum(data.get(date).get(str(i), {}).get("validator_count", 0) for i in range(data_len)) / (data_len - 1)


    with open('./data/validator-data.json', 'w') as file:
        json.dump(data, file, indent=2)

def add_block_time_count():
    with open('./data/block-time-data.json', 'r') as file:
        data = json.load(file)
    
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    hour = now.hour
    
    current_data = data.get(date, {})
    
    data[date] = {
        **current_data,
        str(hour): {
            "block_time": get_block_time()
        },
        "average_time": 0
    }
    
    data_len = len(data.get(date, {}).keys())
    
    if data_len:
        data[date]["average_time"] = sum(data.get(date).get(str(i), {}).get("block_time", 0) for i in range(data_len)) / (data_len - 1)


    with open('./data/block-time-data.json', 'w') as file:
        json.dump(data, file, indent=2)


def init():
    add_validator_count()
    add_block_time_count()

    while True:
        next_hour = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
        wait_time = (next_hour - datetime.datetime.now()).total_seconds()
        time.sleep(wait_time)
        add_validator_count()
        add_block_time_count()
        
init()