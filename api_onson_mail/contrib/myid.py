import os
import string
import random
import urllib.parse
import requests


class MyId:

    def __init__(self):
        self.base_url = os.getenv('MYID_BASE_URL')
        self.client_id = os.getenv('MYID_CLIENT_ID')
        self.client_secret = os.getenv('MYID_CLIENT_SECRET')

    def get_auth_url(self, redirect_url):
        url = f"{self.base_url}/api/v1/oauth2/authorization?"
        response_type = 'code'
        scope = 'common_data'
        method = 'strong'
        state = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=9))
        return url + urllib.parse.urlencode({
            "redirect_url": redirect_url,
            "client_id": self.client_id,
            "response_type": response_type,
            "scope": scope,
            "method": method,
            "state": state
        })
    
    def get_token(self, code) -> dict:
        url = f"{self.base_url}/api/v1/oauth2/access-token"
        data = {
            "grant_type": 'authorization_code',
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        return requests.post(url, json=data).json()
    
    def _get_header(self, token):
        return {
            'Authorization': f'Bearer {token.get("access_token")}'
        }
    
    def get_data_by_token(self, token: dict, refreshed=False):
        url = f"{self.base_url}/api/v1/users/me"
        headers = self._get_header(token)
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            if refreshed: return None
            token = self.refresh_token(token.get('access_token'))
            return self.get_data_by_token(token, True)
        return response.json()
    
    def get_data_by_code(self, code):
        token = self.get_token(code)
        return self.get_data_by_token(token)
        
    def refresh_token(self, refresh_token):
        url = f"{self.base_url}/api/v1/oauth2/refresh-token"
        data = {
            'client_id': self.client_id,
            'refresh_token': refresh_token
        }
        return requests.post(url, json=data).json()