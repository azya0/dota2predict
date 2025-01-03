from opendota.queries.base import requests, get


def get_pro_matches():
    return get("proMatches")


def get_match(id: int) -> requests.Response:
    return get(f"matches/{id}")
