from random import randint
from urllib.request import Request
from fastapi import FastAPI, Response
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import PlainTextResponse
import prometheus_client
from app.api.v1.router import api_router as v1_router
from app.core.logger import log
from app.core.settings import env_list
from app.core.exceptions import init_exceptions
import uvicorn
import secrets, os

security = HTTPBasic()
app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="./app/static/swagger-ui"), name="static")
app.include_router(v1_router, prefix="/v1")
init_exceptions(app)

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def check_env_variable_exist():
    for env_var in env_list:
        if env_var not in os.environ:
            raise Exception("Please check env settings")

@app.on_event("startup")
async def startup_event():
    check_env_variable_exist()

# @app.get("/")
# def read_root():
#     return {"message": "Hello World!"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon-32*32.png",
    )

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon-32*32.png",
        with_google_fonts=False
    )

from app.collectors import http_request
# from app.collectors import test_metric
@app.get('/metrics', include_in_schema=False, response_class=PlainTextResponse)
def metrics():
    from prometheus_client.core import REGISTRY
    return prometheus_client.generate_latest(REGISTRY)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True,debug=True ,log_level="debug", log_config="app/uvicorn_config.json")
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)