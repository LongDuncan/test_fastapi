from pydantic import BaseModel, Field, validator
from typing import Dict, List
from datetime import datetime

class Alert(BaseModel):
    status: str = Field(..., title="status of alert", description="Defines whether or not the alert is resolved or currently firing.")
    labels: Dict[str,str]
    annotations: Dict[str,str]
    startsAt: datetime
    endsAt: datetime
    generatorURL: str
    fingerprint: str

    @validator('status')
    def check_status_value(cls, v):
        if v not in ['firing', 'resolved']:
             raise ValueError('value must be "firing" or "resolved"')
        return v

    class Config:
        schema_extra = {
            "example": {
                "status": "firing",
                "labels": {"alertname": "test","instance": "172.18.0.2:10250","alertGroup":"storage", "job":"kubelet","node": "wroker-1","severity": "critical"},
                "annotations": {"description": "bad ingress config - nginx config test failed"},
                "startsAt": "2022-05-30T06:23:44.87Z",
                "endsAt": "0001-01-01T00:00:00Z",
                "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=kubelet_pod_start_duration_seconds_sum+%3E+45&g0.tab=1",
                "fingerprint": "b18c7a754664e996"
            }
        }

class Alerts(BaseModel):
    receiver: str
    status: str
    alerts: List[Alert]
    groupLabels: Dict[str,str]
    commonLabels: Dict[str,str]
    commonAnnotations: Dict[str,str]
    version: str
    groupKey: str
    externalURL: str
    groupKey: str
    truncatedAlerts: int
    
    @validator('status')
    def check_status_value(cls, v):
        if v not in ['firing', 'resolved']:
            raise ValueError('value must be "firing" or "resolved"')
        return v

    class Config:
        schema_extra = {
            "example": {
                "receiver": "webhook_test",
                "status": "firing",
                "alerts": [{
                                "status": "firing",
                                "labels": {"alertname": "test","instance": "172.18.0.2:10250","alertGroup":"storage", "job":"kubelet","node": "wroker-1","severity": "critical"},
                                "annotations": {"description": "bad ingress config - nginx config test failed",
                                                "value": 50
                                                },
                                "startsAt": "2022-05-30T06:23:44.87Z",
                                "endsAt": "0001-01-01T00:00:00Z",
                                "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=kubelet_pod_start_duration_seconds_sum+%3E+45&g0.tab=1",
                                "fingerprint": "b18c7a754664e996"
                            }, 
                            {
                                "status": "firing",
                                "labels": {"alertname": "test","instance": "172.18.0.3:10250","alertGroup":"storage", "job":"kubelet","node": "wroker-2","severity": "critical"},
                                "annotations": {"description": "bad ingress config - nginx config test failed",
                                                "value": 50
                                                },
                                "startsAt": "2022-05-30T06:23:44.87Z",
                                "endsAt": "0001-01-01T00:00:00Z",
                                "generatorURL": "http://prometheus-kube-prometheus-prometheus.monitoring:9090/graph?g0.expr=kubelet_pod_start_duration_seconds_sum+%3E+45&g0.tab=1",
                                "fingerprint": "2cd25fb3cf412b78"
                            },],
                "groupLabels": {"job": "kubelet"},
                "commonLabels": {"alertGroup":"storage", "job":"kubelet"},
                "commonAnnotations": {"description": "bad ingress config - nginx config test failed"},
                "externalURL": "http://prometheus-kube-prometheus-alertmanager.monitoring:9093",
                "version": "4",
                "groupKey": "{}/{alertGroup=~'storage|network'}:{job='kubelet'}",
                "truncatedAlerts": 0
            }
        }
