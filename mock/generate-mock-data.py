import datetime
import random
import json
import statistics

mockData = {}

def generate_validators_data():
    for i in range(0, 100):
        date = datetime.datetime.now() - datetime.timedelta(days=i) 
        formated = date.strftime("%Y-%m-%d")
        mockData[formated] = {}
        for j in range(0, 24):
            mockData[formated][f"{j}"] = {
                "validator_count": random.randint(1300, 1529),
            }
            
        mockData[formated]["average_count"] = statistics.mean([mockData[formated][f"{j}"]["validator_count"] for j in range(1, 24)]) 
            
            
    with open("./mock/validators-mock-data.json", "w") as file:
        file.write(json.dumps(mockData, indent=2))
            
def generate_block_time_data():
    for i in range(0, 100):
        date = datetime.datetime.now() - datetime.timedelta(days=i) 
        formated = date.strftime("%Y-%m-%d")
        mockData[formated] = {}
        for j in range(0, 24):
            mockData[formated][f"{j}"] = {
                "block_time": random.randint(3500, 8700) / 10000,
            }
            
        mockData[formated]["average_time"] = statistics.mean([mockData[formated][f"{j}"]["block_time"] for j in range(1, 24)]) 

    with open("./mock/block-time-mock-data.json", "w") as file:
        file.write(json.dumps(mockData, indent=2))
        
        
generate_validators_data()
generate_block_time_data()