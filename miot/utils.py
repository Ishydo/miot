import requests
import json

def get_short_url(long_url):
    '''This uses bit.ly to get a short url entering in the beacon config'''
    r = requests.get("https://api-ssl.bitly.com/v3/shorten?access_token=39dc2f1fa6804a927dfdbf0a785e80651bd828ed&longUrl={0}".format(long_url))
    response = json.loads(r.text)
    return response["data"]["url"]
