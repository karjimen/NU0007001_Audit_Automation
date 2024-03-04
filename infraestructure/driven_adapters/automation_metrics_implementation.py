import pandas as pd

from domain.models.automation_metrics import AutomationMetrics
from infraestructure.driven_adapters.gestor_elastic_search import ElasticSearchIntegration


class ElasticSearchAutomationMetrics(AutomationMetrics):

    def __init__(self, url_get_data, user, password):
        self.url_get_data = url_get_data
        self.user = user
        self.password = password

    def get_data_by_query(self, payload):
        connection = ElasticSearchIntegration(
            self.url_get_data,
            self.user,
            self.password,
        )
        return connection.get_data_by_query(payload)
