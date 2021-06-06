import requests
import logging


GET = 'GET'
POST = 'POST'
PATCH = 'PATCH'
DELETE = 'DELETE'


class ApiConnectionException(Exception): pass       # NOQA


class Api:

    def __init__(self, api_url, response_status_parameter='success',
                 response_error_parameter='message', good_status=True,
                 result_data_parameter='data', headers=None):
        self.api_url = api_url
        if self.api_url[-1] != '/':
            self.api_url += '/'
        self.response_status_parameter = response_status_parameter
        self.response_error_parameter = response_error_parameter
        self.good_status = good_status
        self.headers = headers
        self.result_data_parameter = result_data_parameter
        self.session = requests.Session()

    def query(self, path: str, method=GET, **kwargs):
        """
        API query
        :param path:  API relative path
        :param method: HTTP method
        :param kwargs: the same as accepts session.request
        :return: dict
        """
        if path[0] == '/':
            path = path[1:]
        if self.headers and 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        url = "{}{}".format(self.api_url, path)
        logging.debug(f"API {method} request '{url}'; {kwargs}")
        try:
            req = self.session.request(method, url, **kwargs)
        except requests.exceptions.ConnectTimeout as ex:
            raise ApiConnectionException(f"Connection timout. "
                                         f"Host: {self.api_url}") from ex

        if req.status_code != requests.codes.ok:
            logging.warning("Bad API request ({}).".format(req.status_code))
            return None
        data = req.json()
        logging.debug(data)
        if data.get(self.response_status_parameter) != self.good_status:
            logging.warning("Request failed. '{}'".format(
                data.get(self.response_error_parameter, 'X')))
            return None
        if self.result_data_parameter and self.result_data_parameter in data:
            return data[self.result_data_parameter]
        return data

    def get(self, path, **kwargs):
        return self.query(path, 'GET', **kwargs)

    def post(self, path, **kwargs):
        return self.query(path, POST, **kwargs)

    def patch(self, path, **kwargs):
        return self.query(path, PATCH, **kwargs)

    def delete(self, path, **kwargs):
        return self.query(path, DELETE, **kwargs)
