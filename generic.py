import subprocess
import json
import requests

from constants import SOLANA_RPC_URL

from requests.adapters import HTTPAdapter

session = requests.Session()
adapter = HTTPAdapter(max_retries=10)
session.mount("https://", adapter)
session.mount("http://", adapter)


def call_api(method, params=None):
    headers = {
        "Content-Type": "application/json"
    }
    json_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params if params else []
    }
    response = session.post(SOLANA_RPC_URL, json=json_data, headers=headers)
    response.raise_for_status()
    return response.json().get('result', {})


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return json.loads(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        return f"Command '{command}' failed with error code {e.returncode}: {e.stderr.strip()}"
