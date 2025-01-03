import requests

OPENDOTA_URL = "https://api.opendota.com/api"

def get(url: str) -> requests.Response:
    data = requests.get(f"{OPENDOTA_URL}/{url}")

    if data.status_code == 200:
        return data
    
    raise Exception(f"[{data.status_code}] {data.content}")

