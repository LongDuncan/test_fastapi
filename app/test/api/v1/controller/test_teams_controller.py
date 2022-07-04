import unittest
from app.main import app
from fastapi.testclient import TestClient
from app.model.teams import Teams
from unittest.mock import patch
from unittest import mock
import json
class TestTeamsApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.data = {
                "receiver": "webhook_test",
                "status": "firing",
                "alerts": [
                    {
                    "status": "firing",
                    "labels": {
                        "alertGroup": "storage",
                        "job": "kubelet",
                        "node": "wroker-1",
                        "severity": "critical"
                    },
                    "annotations": {
                        "description": "bad ingress config - nginx config test failed"
                    },
                    "startsAt": "2022-05-30T06:23:44.87Z",
                    "endsAt": "0001-01-01T00:00:00Z",
                    "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=kubelet_pod_start_duration_seconds_sum+%3E+45&g0.tab=1",
                    "fingerprint": "b18c7a754664e996"
                    },
                    {
                    "status": "firing",
                    "labels": {
                        "alertGroup": "storage",
                        "job": "kubelet",
                        "node": "wroker-2",
                        "severity": "critical"
                    },
                    "annotations": {
                        "description": "bad ingress config - nginx config test failed"
                    },
                    "startsAt": "2022-05-30T06:23:44.87Z",
                    "endsAt": "0001-01-01T00:00:00Z",
                    "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=kubelet_pod_start_duration_seconds_sum+%3E+45&g0.tab=1",
                    "fingerprint": "2cd25fb3cf412b78"
                    }
                ],
                "groupLabels": {
                    "job": "kubelet"
                },
                "commonLabels": {
                    "alertGroup": "storage",
                    "job": "kubelet"
                },
                "commonAnnotations": {
                    "description": "bad ingress config - nginx config test failed"
                },
                "externalURL": "http://prometheus-kube-prometheus-alertmanager.monitoring:9093",
                "version": "4",
                "groupKey": "{}/{alertGroup=~'storage|network'}:{job='kubelet'}",
                "truncatedAlerts": 0
        }
    def tearDown(self) -> None:
        self.client = None

    def test_post_teams_message_bad_format_data(self):
        data = {"test":"test"}
        response = self.client.post("/v1/teams/test1/test1channel222", json=data)
        assert response.status_code == 422

    def test_post_teams_message_bad_alerts_status(self):
        data = self.data
        data["alerts"][0]["status"] = "test"
        response = self.client.post("/v1/teams/test1/test1channel222", json=data)
        assert response.status_code == 422

    def test_post_teams_message_bad_alert_status(self):
        data = self.data
        data["status"] = "test"
        response = self.client.post("/v1/teams/test1/test1channel222", json=data)
        assert response.status_code == 422

    def test_post_teams_message_bad_channel_id(self):
        response = self.client.post("/v1/teams/test1/test1channel222", json=self.data)
        assert response.status_code == 400

    @patch.object(Teams, 'send_channel_message')
    def test_post_teams_message_success(self,mock_send_channel_message):
        mock_send_channel_message.side_effect = mock.Mock(return_value=True)
        response = self.client.post("/v1/teams/test1/test1channel2", json=self.data)
        assert response.status_code == 201
        assert json.loads(response.content) == {"result": "success"}

    @patch.object(Teams, 'send_channel_message')
    def test_post_teams_message_fail(self,mock_send_channel_message):
        mock_send_channel_message.side_effect = mock.Mock(return_value=False)
        response = self.client.post("/v1/teams/test1/test1channel2", json=self.data)
        assert response.status_code == 500
        assert json.loads(response.content)["result"] == "fail"