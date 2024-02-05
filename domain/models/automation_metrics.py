from abc import ABCMeta, abstractmethod
from typing import List, Dict


class AutomationMetrics(metaclass=ABCMeta):

    @abstractmethod
    def get_data_source_domain(self, url_get_data, token, limit, sources) -> List[Dict]:
        "get data source."

    @abstractmethod
    def get_info_index_with_payload(self, payload_input):
        "update index by query"


