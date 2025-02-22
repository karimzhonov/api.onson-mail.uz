import requests
from .token import get_token


class ApiPushService:
    base_url = 'https://pushservice.egov.uz/v3/app/mq'

    def __init__(self, org_sub, private_key):
        self.token = get_token(org_sub, private_key)

    def _get_header(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    def create_or_update(self, cid, data: dict, systems:list[str]=None):
        url = self.base_url + "/receive"
        headers = self._get_header()
        json = {
            'correlationId': cid,
            'data': data,
            'destinationSubscribers': systems
        }
        return requests.post(url, json=json, headers=headers, verify=False)

    def ping(self):
        url = self.base_url + "/ping"
        return requests.get(url, headers=self._get_header(), verify=False).text

    def get_subscribers(self):
        url = self.base_url + "/publisher/fetch-subscribers"
        headers = self._get_header()
        return requests.get(url, headers=headers, verify=False).json()

    def get_statistics(self):
        url = self.base_url + "/publisher/fetch-daily-delivery-statistics"
        headers = self._get_header()
        return requests.get(url, headers=headers, verify=False).json()

    def get_statistic_pk(self, pk):
        url = self.base_url + f"/publisher/fetch-delivery-detailed-report/{pk}"
        headers = self._get_header()
        return requests.get(url, headers=headers, verify=False).json()
