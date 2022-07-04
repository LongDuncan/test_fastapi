from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional



class OutResponse(BaseModel):
    result: str
    msg: Optional[str] = ""
    detail: Optional[str] = ""
    class Config:
        schema_extra = {
            "example": {
                "result": "",
                "msg": "",
                "detail":""
            }
        }


response_template = {
    "success": {
            "example": {"result": "success", "msg":"", "detail": ""}        
    },
    "fail": {
            "example": {"result": "fail", "msg":"Some error message", "detail": ""}        
    },
    "422":{
            "example": {
                "detail": [
                    {
                        "loc": [
                        "body",
                        "status"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ],
                "msg": "UNPROCESSABLE_ENTITY",
                "result": "failed"
            }
    },
    "500":{
            "example": {
                "detail": "Traceback error message.",
                "msg": "INTERNAL_SERVER_ERROR",
                "result": "failed"
            }
    },
}