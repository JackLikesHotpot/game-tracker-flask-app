from dotenv import load_dotenv
import requests
import os
from cachetools import cached, TTLCache

load_dotenv()
CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_ID')

@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_access_token():
    """
    Returns an access token from the Twitch API using a valid Client ID and Client Secret.
    Access token is cached for an hour for reusability.
    """
    response = requests.post(
        "https://id.twitch.tv/oauth2/token",
        params = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        },
        timeout = 15
    )
    response.raise_for_status()
    return response.json()["access_token"]


@cached(cache=TTLCache(maxsize=100, ttl=3600))
def igdb_post(endpoint: str, query: str):
    """
    Takes in input endpoint and query and passes them as parameters into a url template to query IGDB's API.
    Returns a JSON containing the requested information of the query.
    Results are cached for 10 minutes and can hold up to 100 results.
    """
    access_token = get_access_token()
    response = requests.post(
        f"https://api.igdb.com/v4/{endpoint}",
            headers = {
                "Client-ID": CLIENT_ID, 
                "Authorization": f"Bearer {access_token}"},
            data = query,
            timeout = 15
        )
    response.raise_for_status()
    return response.json()
