import requests
from .token import get_token


class ApiPushService:
    base_url = 'https://pushservice.egov.uz/v3/app/mq'

    def __init__(self):
        self.token = get_token()

    def _get_header(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    def create_or_update(self, pk, data: dict, systems:list[str]=None):
        url = self.base_url + "/receive"
        headers = self._get_header()
        json = {
            'correlationId': str(pk),
            'data': data,
            'destinationSubscribers': systems
        }
        return requests.post(url, json=json, headers=headers)

    def get_subscribers(self):
        url = self.base_url + "/publisher/fetch-subscribers"
        headers = self._get_header()
        return requests.get(url, headers=headers)

    def get_statistics(self):
        url = self.base_url + "/publisher/fetch-daily-delivery-statistics"
        headers = self._get_header()
        return requests.get(url, headers=headers)

    def get_statistic_pk(self, pk):
        url = self.base_url + f"publisher/fetch-delivery-detailed-report/{pk}"
        headers = self._get_header()
        return requests.get(url, headers=headers)
