
import os, folium


import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from pandas.io.json import json_normalize
from config import wigle_encoded_token, wigle_password, wigle_username

import geoplotlib as gp


class test_wigle:

    def __init__(self, api_username, api_password, encoded_token):
        self.auth = HTTPBasicAuth(api_username, api_password)
        self.encoded_token = encoded_token



    def search(self, ssid, country='US', region=None, city=None):
        payload = {'ssid':ssid, 'region':region, 'api_key':self.encoded_token}
        response = requests.get(url="https://api.wigle.net/api/v2/network/search", params=payload, auth=self.auth).json()
        
        # Extract response as a pandas dataframe to work with
        dataframe = json_normalize(response['results'])

        # Rename Columns for Geoplot Lib
        self.dataframe = dataframe.rename(columns={'trilat': 'lat', 'trilong': 'lon'})


    def geocode(self, code):
        payload = {'first': '0', 'freenet': 'false', 'paynet': 'false', 'addresscode': code, 'api_key':self.encoded_token}
        response = requests.get(url="https://api.wigle.net/api/v2/network/geocode", params=payload, auth=self.auth).json()
        return response

    def show_map(self):
        self.load_points()
        gp.show()
    
    def load_points(self):
        gp.dot(self.dataframe, )
    


temp = test_wigle(wigle_username, wigle_password, wigle_encoded_token)
temp.search('NETGEAR91', 'US', 'AZ')

while True:
    if input("What device would you like to view now?") != '0':
        temp.show_map()
    else:
        break