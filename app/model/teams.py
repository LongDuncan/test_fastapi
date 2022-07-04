from app.core.microsoft import graph_client, msal_client
from app.schema.alert_data_structure import Alerts
from app.core.logger import log
from jinja2 import Environment, FileSystemLoader
class Teams:
    def __init__(self, team_id, channel_id):
        self.team_id = team_id
        self.channel_id = channel_id

    def send_channel_message(self, msg) -> bool:
        if isinstance(msg, Alerts):
            env = Environment(loader=FileSystemLoader("app/templates"))
            template = env.get_template("alert.html")
            request_body = template.render(alerts=msg)
            data = {
                "body": {
                    "contentType": "html",
                    "content": request_body
                }
            }
        else:
            data = {
                "body": {
                    "content": msg
                }
            }
        msal_app = msal_client.MSALClient()
        get_access_token_result = msal_app.get_access_token()
        if get_access_token_result and get_access_token_result["result"] == "success":
            graph_app = graph_client.GraphClient(get_access_token_result["access_token"])
            return graph_app.sending_message_in_channel(self.team_id, self.channel_id, str(data))
        else:
            log.error("It's can not get access token from msal client.")
            raise Exception("It's can not get access token from msal client.")