import json
import time
import statistics
from collections import Counter
from matplotlib import pyplot as plt

from constants import HISTORY_DAYS

from generic import run_command


def calculate_average_validator_count():
    mock_data = json.loads(open('./mock/validators-mock-data.json').read())
    history = []
    plot_data = []
    for i in range(HISTORY_DAYS):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time() - i * 86400))
        history.append(mock_data.get(date, {}).get("average_count", 0))
        plot_data.append({"Date": date, "Count": mock_data.get(date, {}).get("average_count", 0)})
        
    plt.plot([data["Date"] for data in reversed(plot_data)], [data["Count"] for data in reversed(plot_data)])
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.ylabel("Count")
    plt.title("Average Validators Count")
    plt.savefig('./output/average-validators-count.png')
    plt.close()
        
    return statistics.mean(history)

def get_validator_count():
    resp = run_command("solana validators --output json")
    active_count = sum(1 for validator in resp.get('validators', []) if not validator["delinquent"])
    return active_count

def get_lastest_block():
    resp = run_command("solana slot")
    return resp
    
def get_block_time():
    times = {}
    slot = 0
    
    # wait for the next second to start
    time.sleep(1 - time.time() % 1)

    # Send 100 requests to the block-time endpoint
    for _ in range(100):
        data = run_command(f"solana block-time --output json")
        timestamp = data.get('timestamp', 0)
        # if this is a new slot (so a new block) we increment the count of this timestamp
        if data.get('slot', -1) != slot:
            times[timestamp] = times[timestamp] + 1 if timestamp in times else 1
            slot = data.get('slot', 0)
    
    new_times = times.copy()
     
    # Remove timestamps that only occured once - this means that we hit some kind of rate limiter and we didn't get the full data        
    for key, value in times.items():
        if value == 1:
            del new_times[key]
            
    times = new_times

    # this is the count of timestamps, so seconds            
    count_timestamps = len(times.keys())
    # this is the count of blocks
    count_blocks = sum(times.values())
    
    # average blocks per second, so the block time
    avg = count_timestamps / count_blocks

    return avg
    
def get_average_block_time():
    mock_data = json.loads(open('./mock/block-time-mock-data.json').read())
    history = []
    plot_data = []
    for i in range(HISTORY_DAYS):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time() - i * 86400))
        history.append(mock_data.get(date, {}).get("average_time", 0))
        plot_data.append({"Date": date, "Time": mock_data.get(date, {}).get("average_time", 0)})
        
    plt.plot([data["Date"] for data in reversed(plot_data)], [data["Time"] for data in reversed(plot_data)])
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.ylabel("Time")
    plt.title("Average Block Time")
    plt.savefig('./output/average-block-time.png')
    plt.close()
    
    return statistics.mean(history)

def get_validator_gossip():
    data = run_command("solana gossip --output json")
    if data:
        gossip_info = [(node['identityPubkey'], node['ipAddress']) for node in data if 'ipAddress' in node]
        return gossip_info
    else:
        print("No data received from solana gossip command")
        return None
    
def ip_address_clusters():
    gossip_info = get_validator_gossip()
    ips = [info[1] for info in gossip_info if info[1]]
    ip_clusters = Counter(ips)
    return ip_clusters

def main():
    validator_count = get_validator_count()
    lastest_block = get_lastest_block()
    avg_validator_count = calculate_average_validator_count()
    block_time = get_average_block_time()
    
    ip_clusters = ip_address_clusters()

    
    print(f"Validators: {validator_count}")
    print(f"Lastest block: {lastest_block}")
    print(f"Average validators: {avg_validator_count}")
    print(f"Average Block time: {block_time}")
    print("IP clusters saved to ip-clusters.json")

    with open('./output/ip-clusters.json', 'w') as file:
        json.dump(ip_clusters, file, indent=2)
    