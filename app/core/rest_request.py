from app.core.settings import proxies
from app.core.logger import log
import requests
import requests
import functools
import urllib3
urllib3.disable_warnings()

def get_http_client(verify=True, proxies=None, timeout=15):

    http_client = requests.Session()
    http_client.verify = verify
    http_client.proxies = proxies
    # http_client.headers.update({'User-Agent': 'python-requests/2.18.4'})

    # Requests, does not support session - wide timeout
    # But you can patch that (https://github.com/psf/requests/issues/3341):
    http_client.request = functools.partial(
        http_client.request, timeout=timeout)

    # Enable a minimal retry. Better than nothing.
    # https://github.com/psf/requests/blob/v2.25.1/requests/adapters.py#L94-L108
    request_max_retries = requests.adapters.HTTPAdapter(max_retries=1)
    http_client.mount("http://", request_max_retries)
    http_client.mount("https://", request_max_retries)
    return http_client

def send_request(url, method="GET", params=None, data=None, headers=None) -> requests.Response:
    try:
        req = requests.Request(method,  url, data=data, headers=headers)
        http_client = get_http_client(verify=False, proxies=proxies)
        prepped = http_client.prepare_request(req)
        response = http_client.send(prepped,)
        return response
    except requests.exceptions.HTTPError as errh:
        log.error("Http Error: ",errh)
        raise requests.exceptions.HTTPError("Http Error: ",errh)
    except requests.exceptions.ConnectionError as errc:
        log.error("Connection Error: ",errc)
        raise requests.exceptions.ConnectionError("Connection Error: ",errc)
    except requests.exceptions.Timeout as errt:
        log.error("Timeout Error: ",errt)
        raise requests.exceptions.Timeout("Timeout Error: ",errt)
    except requests.exceptions.RequestException as err:
        log.error("Request Exception: ",err)
        raise requests.exceptions.RequestException("Request Exception: ",err)


