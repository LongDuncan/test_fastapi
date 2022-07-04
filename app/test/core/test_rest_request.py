from unittest.mock import Mock, patch
from unittest import mock
from app.core.rest_request import send_request
import requests
import pytest
class TestRestQuest:

    def test_send_request_http_error(self):
        def res():
            r = requests.Response()
            r.status_code = 404
            return r
        send_request = mock.Mock(return_value=res())
        res = send_request("http://127.0.0.1:9000/test_post", method="POST", params=None, data="test_data", token="test_token")
        with pytest.raises(requests.exceptions.HTTPError) as err_msg:
            res.raise_for_status()
        assert res.status_code == 404

    def test_send_request_connection_error(self):
        send_request = mock.Mock()
        send_request.side_effect = requests.exceptions.ConnectionError
        with pytest.raises(requests.exceptions.ConnectionError) as error_info:
            send_request("http://127.0.0.1:9000/test_post", method="POST", params=None, data="test_data", token="test_token")
        assert error_info.type == requests.exceptions.ConnectionError
    
    def test_send_request_timeout(self):
        send_request = mock.Mock()
        send_request.side_effect = requests.exceptions.Timeout
        with pytest.raises(requests.exceptions.Timeout) as error_info:
            send_request("http://127.0.0.1:9000/test_post", method="POST", params=None, data="test_data", token="test_token")
        assert error_info.type == requests.exceptions.Timeout

    def test_send_request_request_exception(self):
        send_request = mock.Mock()
        send_request.side_effect = requests.exceptions.RequestException
        with pytest.raises(requests.exceptions.RequestException) as error_info:
            send_request("http://127.0.0.1:9000/test_post", method="POST", params=None, data="test_data", token="test_token")
        assert error_info.type == requests.exceptions.RequestException
