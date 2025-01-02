import requests

import datetime

def parse_pro_matches(data: list[dict]) -> list[tuple[int, datetime.datetime]]:
    result = []
    
    for match in data:
        result.append((
            match["match_id"], datetime.datetime.fromtimestamp(match["start_time"])
        ))

if __name__ == "__main__":
    data = requests.get("https://api.opendota.com/api/proMatches")

    if data.status_code != 200:
        raise Exception(f"[{data.status_code}] {data.content}")

    result = data.json()
