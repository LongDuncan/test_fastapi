from app.core.microsoft.graph_client import GraphClient
from unittest.mock import Mock, patch
from unittest import mock
import requests

data = {
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

class TestGraphClient:
    
    @patch("app.core.microsoft.graph_client.send_request")
    def test_send_channel_msg_success(self, mock_send_request):
        def res():
            r = requests.Response()
            r.status_code = 201
            def json_func():
                return data
            r.json = json_func
            return r
        mock_send_request.return_value = res()
        graph_client = GraphClient("access_token")
        assert graph_client.sending_message_in_channel("team_id","channel_id",data) == True
    
    @patch("app.core.microsoft.graph_client.send_request")
    def test_send_channel_msg_fail(self, mock_send_request):
        def res():
            r = requests.Response()
            r.status_code = 302
            def json_func():
                return data
            r.json = json_func
            return r
        mock_send_request.return_value = res()
        graph_client = GraphClient("access_token")
        assert graph_client.sending_message_in_channel("team_id","channel_id",data) == False