import requests
from py_eureka_client import eureka_client


class EurekaClient():
    def __init__(self, remote_service: str):
        self.remote_service = remote_service

    def _call_post_service(self, url: str, /) -> 'EurekaResponse':
        response = requests.post(url, self.data)
        content = response.json()
        return EurekaResponse(response.status_code, content)

    def _call_get_service(self, url: str, /) -> 'EurekaResponse':
        try:
            response = requests.get(url)
            content = response.json()
            return EurekaResponse(response.status_code, content)
        except Exception as e:
            return EurekaResponse(404, {})

    def call_remote_service(self, uri: str, method: str, /):
        MAP_METHODS = {
            'POST': self._call_post_service,
            'GET': self._call_get_service,
        }

        response = eureka_client.walk_nodes(
            app_name=self.remote_service,
            service=uri,
            walker=MAP_METHODS[method]
        )
        return response


class EurekaResponse:
    def __init__(self, status: int, content: dict):
        self.status = status
        self.content = content
