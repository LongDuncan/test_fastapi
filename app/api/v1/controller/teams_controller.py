from fastapi import APIRouter, HTTPException,Response, status, Request
from fastapi.responses import JSONResponse
from app.schema.alert_data_structure import Alerts
from app.schema.out_response import OutResponse, response_template
from app.core.logger import log
from app.model.teams import Teams as TeamsBackend
from jinja2 import Environment, FileSystemLoader
import json
import urllib.parse
import re
router = APIRouter()

@router.get("")
async def get_teams_users():
    return [{"user": "Tim"},{"user": "Duncan"}]

@router.get("/test")
async def hello(request:Request, name=None):
    try:
        env = Environment(loader=FileSystemLoader("app/templates"))
        template = env.get_template("alert.html")
        data = template.render(name=name)
        print(data)
    except Exception as e:
        raise HTTPException(status_code=500)


@router.get("/test/{test_id}")
async def test_id(request:Request, test_id: str, name=None):
    try:
        import random,time
        rand = random.uniform(0,1)
        time.sleep(rand)
        if rand > 7:
            return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    content = {"result": "failed", "msg": "Duration time over 7 sec."}
                )
        return test_id
    except Exception as e:
        raise HTTPException(status_code=500)

@router.post("/{team_id}/{channel_id}", status_code=201, response_model=OutResponse, responses={
                201: {  "model": OutResponse,
                        "content": {
                            "application/json": response_template["success"]
                        }
                    },
                400: {  "model": OutResponse,
                        "description": "This endpoint raises an bad request error",
                        "content": {
                            "application/json": response_template["fail"]
                        }
                    },
                422: {  "model": OutResponse,
                        "description": "This endpoint raises an unprocessable entity error",
                        "content": {
                            "application/json": response_template["422"]
                        }
                    },
                500: {  "model": OutResponse,
                        "description": "This endpoint raises an internal server error",
                        "content": {
                            "application/json": response_template["500"]
                        }
                    },
                },
                summary="Send a message to teams channel",
                description="Send a message to teams channel",)
async def send_msg_to_teams_channel(request:Request, team_id: str, channel_id: str, alerts: Alerts, response: Response) -> JSONResponse:
    # channel url: /teams/{team-id}/channels/{channel-id}/messages
    # chat url: /chats/{chat-id}/messages
    try:
        with open('app/config/teamid_whitelist.json', 'r') as teamid_allowed_file:
            teamid_allowed_json = json.load(teamid_allowed_file)

            # The channel_id request may contain quote format or not, so we need to force format to include quote
            def channel_id_formatter():
                pattern = "%[A-Z,0-9][A-Z,0-9]"
                new_channel_id_format = urllib.parse.quote_plus(channel_id, encoding="utf-8", safe="%")
                result = set(re.findall(pattern, new_channel_id_format))
                for r in result:
                    new_channel_id_format = new_channel_id_format.replace(r, r.lower())
                return new_channel_id_format

            if team_id not in teamid_allowed_json.keys() or channel_id_formatter() not in teamid_allowed_json[team_id]:
                return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    content = {"result": "failed", "msg": "Please check team id or channel id"}
                )
            else:
                teams_model = TeamsBackend(team_id, channel_id)
                if teams_model.send_channel_message(Alerts(**alerts.dict())):
                    return JSONResponse(
                        status_code = status.HTTP_201_CREATED,
                        content = {"result": "success"}
                    )
                else:
                    return JSONResponse(
                        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content = {"result": "fail", "msg": "Please check logs for more details."}
                    )

    except Exception as e:
        raise HTTPException(status_code=500)

