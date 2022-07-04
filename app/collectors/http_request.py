import random
import time
import re
from app.main import app as fast_app
from urllib.request import Request
from prometheus_client import Histogram
from fastapi import APIRouter
from starlette.routing import Match
router = APIRouter()
ingnore_request_path = [
    "/docs", "/static/swagger-ui.css", "/openapi.json", "/static/swagger-ui-bundle.js"
]

request_response_buckets = (0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10)
fastapi_http_metric_template = {
    'request_response':
        Histogram(  'test_fastapi_request_response',
                    'Request of response time',
                    ["path", "method", "code"],
                    buckets=request_response_buckets),
}

def _check_is_ignore_request_path(request_path):
    if re.match("^\/(static|openapi|swagger|redoc|docs).*",request_path):
        return True
    return False

def _get_route_name(request:Request):
    # Ref: https://github.com/beniwohli/apm-agent-python/commit/1f56f08a6412bef1697d6f6bcbe715742b3072d3
    route_name = None
    app = request.app
    scope = request.scope
    routes = app.routes
    for route in routes:
        match, _ = route.matches(scope)
        if match == Match.FULL:
            route_name = route.path
            break
        elif match == Match.PARTIAL and route_name is None:
            route_name = route.path
    # Starlette magically redirects requests if the path matches a route name with a trailing slash
    # appended or removed. To not spam the transaction names list, we do the same here and put these
    # redirects all in the same "redirect trailing slashes" transaction name
    if not route_name and app.router.redirect_slashes and scope["path"] != "/":
        redirect_scope = dict(scope)
        if scope["path"].endswith("/"):
            redirect_scope["path"] = scope["path"][:-1]
            trim = True
        else:
            redirect_scope["path"] = scope["path"] + "/"
            trim = False
        for route in routes:
            match, _ = route.matches(redirect_scope)
            if match != Match.NONE:
                route_name = route.path + "/" if trim else route.path[:-1]
                break
    if route_name:
        return route_name.rstrip("/")
    return request.url.path.rstrip("/")

def _get_status_code_group(status_code):
    if re.match("[1]([0-9]){2}",status_code):
        regrex_status_code = "1xx"
    elif re.match("[2]([0-9]){2}",status_code):
        regrex_status_code = "2xx"
    elif re.match("[3]([0-9]){2}",status_code):
        regrex_status_code = "3xx"
    elif re.match("[4]([0-9]){2}",status_code):
        regrex_status_code = "4xx"
    elif re.match("[5]([0-9]){2}",status_code):
        regrex_status_code = "5xx"
    return regrex_status_code

@fast_app.middleware("http")
async def print_console(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time() - start_time
    request_path = request.url.path.rstrip("/")
    request_method = request.method

    if not _check_is_ignore_request_path(request_path):
        status_code = str(response.status_code)
        regrex_status_code = _get_status_code_group(status_code)
        route_name = _get_route_name(request)
        fastapi_http_metric_template["request_response"].labels(route_name,
                                                                request_method,
                                                                regrex_status_code).observe(end_time)
    return response
