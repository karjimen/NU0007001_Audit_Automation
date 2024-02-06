from abc import ABCMeta, abstractmethod

class AutomationMetrics(metaclass=ABCMeta):

    @abstractmethod
    def get_data_by_query(self, url_get_data, user, password, payload):
        "get data by query"



