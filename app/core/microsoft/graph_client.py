import json
from urllib.parse import urljoin
from app.core.settings import graph_endpoint
from app.core.rest_request import send_request
from app.core.logger import log
class GraphClient:
    def __init__(self, access_token) -> None:
        self.access_token = access_token
    
    def _create_headers(self):
        headers = {}
        headers["Authorization"] = f"Bearer {self.access_token}"
        headers["Content-type"] = "application/json"
        return headers

    def sending_message_in_channel(self, team_id, channel_id, msg):
        sending_message_in_channel_endpoint = urljoin(graph_endpoint, "teams/%s/channels/%s/messages" %(team_id, channel_id))
        headers = self._create_headers()

        graph_data = send_request(
            sending_message_in_channel_endpoint,
            method="POST",
            data = str(msg),
            headers = headers,)
        log.debug("Graph API call result: %s" % json.dumps(graph_data.json(), indent=2))
        if graph_data.status_code == 201:
            return True
        else:
            return False
