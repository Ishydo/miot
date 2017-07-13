import requests
import json
from miotProject.settings import MIOT_BITLY

def get_short_url(long_url):
    '''This uses bit.ly to get a short url entering in the beacon config'''
    r = requests.get("https://api-ssl.bitly.com/v3/shorten?access_token={0}&longUrl={1}".format(MIOT_BITLY, long_url))
    response = json.loads(r.text)
    return response["data"]["url"]
