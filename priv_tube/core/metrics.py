from abc import ABC, abstractmethod
from typing import Any


class MetricsRepository(ABC):
    @abstractmethod
    def record(self, metric_name: str, metric_value: Any, **kwargs):
        pass


class InfluxAdapter(MetricsRepository):
    def record(self, metric_name: str, metric_value: Any, **kwargs):
        pass


adapter = InfluxAdapter()


def record(metric_name, value, tags: dict = None, fields: dict = None):
    pass


def setDefaultAdapter(default_adapter: MetricsRepository):
    adapter = default_adapter
