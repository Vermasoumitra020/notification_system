from abc import ABC, abstractmethod
import requests


class InstanceHandlerStrategy(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def fetch_instance(self, data):
        pass


class UserInstanceHandlerStrategy(InstanceHandlerStrategy):

    '''
    Implements the InstanceHandlerStrategy to get the User data from the data handler service
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fetch_instance(self, data):
        users = []
        for id in data["ids"]:
            res = requests.get(self.url + str(id) + "/")
            if res.status_code == 200:
                response = res.json()
                users.append(response)
            else:
                raise ConnectionRefusedError(f"Failed {res.status_code}")

        return users


class SubscriptionInstanceHandlerStrategy(InstanceHandlerStrategy):
    '''
    Implements the InstanceHandlerStrategy to get the subscription data from the data handler service
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fetch_instance(self, data):
        users = []
        for id in data["ids"]:
            try:
                res = requests.get(self.url + str(id) + "/")
                if res.status_code == 200:
                    response = res.json()
                    print(response)
                    users = response["user"]
                else:
                    raise ConnectionRefusedError(f"Failed {res.status_code}")
            except (ConnectionRefusedError, ConnectionError):
                raise ConnectionError(f"Failed {res.status_code}")

        return users
