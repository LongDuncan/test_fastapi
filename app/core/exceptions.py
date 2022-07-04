from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status
from app.core.logger import log
import traceback

def init_exceptions(app):

    @app.exception_handler(RequestValidationError)
    async def vaildation_exception_handler(request: Request, exec: RequestValidationError):
        exec_str = f"{exec}".replace("\n"," ").replace("    "," ")
        log.error(exec_str)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail":exec.errors(), "msg": "UNPROCESSABLE_ENTITY", "result":"failed"})
        )

    @app.exception_handler(HTTPException)
    async def all_http_exception_handler(request: Request, exec: HTTPException):
        if exec.status_code==401 and request.url.path == "/docs":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Basic"},
                content=jsonable_encoder({"detail":"Not Authorized"})
            )
        log.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"detail":traceback.format_exc(), "msg": "INTERNAL_SERVER_ERROR", "result":"failed"})
        )