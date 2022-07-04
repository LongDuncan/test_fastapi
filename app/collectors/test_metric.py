import random
from urllib.request import Request
import time
from prometheus_client.core import REGISTRY, GaugeMetricFamily, CounterMetricFamily
from collections import defaultdict, Counter

rand_total_dict = defaultdict(Counter)

class TestMetric(object):
    def collect(self):

        start = time.time()
        # setup empty prometheus metrics
        self._setup_empty_prometheus_metrics()
        self._get_rand_total()
        self._update_rand_total()
        duration = time.time() - start
        self._prometheus_metrics['scrape_duration_seconds'].add_metric(
            [], duration)
        for metric in self._prometheus_metrics.values():
            yield metric
    def _setup_empty_prometheus_metrics(self):
        """
        The metrics we want to export.
        """
        self._prometheus_metrics = {
            'request_total':
                CounterMetricFamily('test_fastap_request_total',
                                    'Number of operations',
                                    labels=["rand_index",]),
            'scrape_duration_seconds':
                GaugeMetricFamily('test_fastapi_scrape_duration_seconds',
                                  'Ammount of time each scrape takes',
                                  labels=[])
        }

    def _get_rand_total(self):
        import random,time
        rand_index = random.randint(1,2)
        # if rand_index not in rand_total_dict.keys():
        #     rand_total_dict[rand_index] = Counter()
        rand_total_dict[rand_index].update({"key1":1})
        print(dict(rand_total_dict))
    def _update_rand_total(self):
        for rand_index in rand_total_dict:
            self._prometheus_metrics["request_total"].add_metric(([str(rand_index)]),rand_total_dict[rand_index]["key1"])

REGISTRY.register(TestMetric())