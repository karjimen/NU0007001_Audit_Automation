from abc import ABCMeta, abstractmethod
from typing import List, Dict


class AutomationMetrics(metaclass=ABCMeta):

    @abstractmethod
    def update_index_by_query(self, url_get_data, user, password, payload):
        "update index by query"


