from requests import Session


class BaseSession(Session):

    def __init__(self, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")

    def request(self, method, url, **kwargs):
        return super().request(method, self.base_url + url, **kwargs)
